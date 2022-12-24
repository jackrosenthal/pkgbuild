#!/usr/bin/env python3

import concurrent.futures
import dataclasses
import itertools
import json
import logging
import os
import pathlib
import pprint
import re
import shlex
import subprocess
import sys
import tempfile
import threading
import time

import argh
import requests
import tqdm

REPO_NAME = "jmr"
REPO_URL = "https://archlinux-jmr.s3.us-west-004.backblazeb2.com/$repo/$arch"
S3_UPLOADS = f"s3://archlinux-jmr/{REPO_NAME}/x86_64/"
GPG_KEY_ID = "55E00EDED9D418CBACB39CAD184AD86A1B97C873"
git_lock = threading.Lock()

SKIP_CHECK_PKGS = []
ALTERNATIVES = {
    "electron12": "electron12-bin",
}


# Ugly, can we remove the need?
def infer_package_name_from_archive(archive_name):
    m = re.match(
        r"([a-z0-9_-]+)-(?:[0-9]+:)?(?:[0-9]+\.)+[0-9][a-z]*-[0-9]+-[a-z0-9_]+.pkg",
        archive_name,
    )
    return m.group(1)


def make_task(name, commands):
    def shellsafe(command):
        if isinstance(command, str):
            return command
        return " ".join(map(shlex.quote, command))

    if not isinstance(commands, str):
        commands = ";".join(map(shellsafe, commands))

    return {name: commands}


def make_manifest(packages=(), tasks=(), artifacts=()):
    return json.dumps(
        {
            "image": "archlinux",
            "packages": sorted(packages),
            "secrets": [
                "02a0c815-b30f-4ea4-ba07-c5f8f3b63fee",  # PGP signing key
            ],
            "sources": [
                "https://git.sr.ht/~jmr/pkgbuild",
            ],
            "repositories": {
                REPO_NAME: f"{REPO_URL}#{GPG_KEY_ID}",
                "multilib": "http://mirror.rackspace.com/archlinux/$repo/os/$arch#c100346676634e80c940fb9e9c02ff419fecbe16",
            },
            "tasks": list(tasks),
            "artifacts": list(artifacts),
        }
    )


class SourcehutBuildAPI:
    def __init__(self, auth_token):
        if not auth_token:
            auth_token = (pathlib.Path.home() / ".srht_token").read_text().strip()

        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"token {auth_token}"})

    def submit_job(self, manifest):
        r = self.session.post(
            "https://builds.sr.ht/api/jobs",
            json={"manifest": manifest},
        )
        r.raise_for_status()
        job_json = r.json()
        return job_json["id"]

    def get_job_status(self, job_id):
        r = self.session.get(
            f"https://builds.sr.ht/api/jobs/{job_id}",
        )
        r.raise_for_status()
        job_json = r.json()
        return job_json["status"]

    def get_job_artifacts(self, job_id):
        r = self.session.get(
            f"https://builds.sr.ht/api/jobs/{job_id}/artifacts",
        )
        r.raise_for_status()
        paginated_wrapper = r.json()
        return paginated_wrapper["results"]


def pacman_db_has_version_or_newer(package_name, version_str):
    result = subprocess.run(
        ["pacman", "-S", "--print", f"{package_name}>={version_str}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


@dataclasses.dataclass
class PkgBase:
    name: str
    pkgver: str = ""
    pkgrel: int = 0
    epoch: int = 0
    depends: set = dataclasses.field(default_factory=set)
    makedepends: set = dataclasses.field(default_factory=set)
    checkdepends: set = dataclasses.field(default_factory=set)
    aursrc: str = ""
    packages: list = dataclasses.field(default_factory=list)
    path: pathlib.Path = dataclasses.field(default_factory=pathlib.Path)
    path_abs: pathlib.Path = dataclasses.field(default_factory=pathlib.Path)

    def get_build_dependencies(self, check=True):
        pkgs = set()

        pkgs.update(self.depends)
        pkgs.update(self.makedepends)
        if check:
            pkgs.update(self.checkdepends)

        for pkg in self.packages:
            pkgs.update(pkg.depends)
            pkgs.update(pkg.makedepends)
            if check:
                pkgs.update(pkg.checkdepends)

        return {ALTERNATIVES.get(pkg, pkg) for pkg in pkgs}

    def fmt_version(self):
        version = f"{self.pkgver}-{self.pkgrel}"
        if self.epoch:
            version = f"{self.epoch}:{version}"
        return version

    def needs_update(self):
        version_str = self.fmt_version()
        for pkg in self.packages:
            if not pacman_db_has_version_or_newer(pkg.name, version_str):
                return True
        return False

    def get_artifact_names(self):
        result = subprocess.run(
            ["makepkg", "--packagelist"],
            stdout=subprocess.PIPE,
            cwd=self.path_abs,
            check=True,
            encoding="utf-8",
        )
        lines = result.stdout.splitlines()
        return [line.rstrip().split("/")[-1] for line in lines]


@dataclasses.dataclass
class Package:
    name: str
    depends: set = dataclasses.field(default_factory=set)
    makedepends: set = dataclasses.field(default_factory=set)
    checkdepends: set = dataclasses.field(default_factory=set)


def parse_srcinfo(content):
    pkgbase = None
    section = None
    for line in content.splitlines():
        line, _, _ = line.partition("#")
        line = line.strip()
        if not line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()

        if key.endswith("_x86_64"):
            key = key[: -len("_x86_64")]

        if key == "pkgbase":
            pkgbase = PkgBase(name=value)
            section = pkgbase
        elif key == "pkgname":
            pkg = Package(name=value)
            pkgbase.packages.append(pkg)
            section = pkg
        elif key == "pkgver":
            pkgbase.pkgver = value
        elif key == "pkgrel":
            pkgbase.pkgrel = int(value)
        elif key == "epoch":
            pkgbase.epoch = int(value)
        elif key in ("depends", "makedepends", "checkdepends"):
            pkgs = getattr(section, key)
            pkgs.add(value)
    return pkgbase


def load_package_from_dir(path):
    path = path.resolve()
    srcinfo = path / ".SRCINFO"
    if srcinfo.is_file():
        srcinfo_contents = srcinfo.read_text()
    else:
        result = subprocess.run(
            ["makepkg", "--printsrcinfo"],
            cwd=path,
            check=True,
            stdout=subprocess.PIPE,
            encoding="utf-8",
        )
        srcinfo_contents = result.stdout
    pkgbase = parse_srcinfo(srcinfo_contents)
    pkgbase.path_abs = path
    try:
        pkgbase.path = path.relative_to(pathlib.Path(__file__).parent)
    except ValueError:
        pkgbase.path = path
    if path.parent.name == "aur":
        pkgbase.aursrc = f"https://aur.archlinux.org/{pkgbase.name}"
    return pkgbase


def find_packages():
    here = pathlib.Path(__file__).parent
    for pkgbuild in here.rglob("PKGBUILD"):
        pkgpath = pkgbuild.parent
        if not (pkgpath / ".buildbot_disable").is_file():
            yield load_package_from_dir(pkgpath)


@dataclasses.dataclass
class DepgraphEntry:
    pkgbase: PkgBase
    graphdepends: list
    otherdepends: set

    def get_graphdepends_urls(self, url_dict):
        result = []
        for other_pkgbase, other_pkg in self.graphdepends:
            result.append(url_dict[other_pkg.name])
        return result

    def extend(self, other):
        if not self.otherdepends:
            return False
        rv = False
        for pkg in other.pkgbase.packages:
            if pkg.name in self.otherdepends:
                self.otherdepends.remove(pkg.name)
                self.otherdepends.update(other.depends)
                self.otherdepends.update(pkg.depends)
                self.graphdepends.append((other, pkg))
                rv = True
        return rv


def get_depgraph(packages, check=True):
    # Initial first level
    depgraph = []

    for pkgbase in packages:
        check_this_pkg = check
        if pkgbase.name in SKIP_CHECK_PKGS:
            check_this_pkg = False
        dep_names = pkgbase.get_build_dependencies(check=check_this_pkg)
        graphdepends = []
        for other_pkgbase in packages:
            if not dep_names:
                break
            if other_pkgbase is pkgbase:
                continue
            for other_pkg in other_pkgbase.packages:
                if other_pkg.name in dep_names:
                    dep_names.update(other_pkgbase.depends)
                    graphdepends.append((other_pkgbase, other_pkg))
                    dep_names.remove(other_pkg.name)
                if not dep_names:
                    break
        depgraph.append(
            DepgraphEntry(
                pkgbase=pkgbase,
                graphdepends=graphdepends,
                otherdepends=dep_names,
            )
        )

    while True:
        any_extensions_made = False

        for de1 in depgraph:
            for de2 in depgraph:
                if de1 is de2:
                    continue
                if de1.extend(de2):
                    any_extensions_made = True

        if not any_extensions_made:
            return depgraph


def orchestrate(
    rebuild_all: bool = False, check: bool = True, sourcehut_token: str = ""
):
    logger = logging.getLogger(__name__)
    pkgs = []
    for pkg in find_packages():
        if rebuild_all or pkg.needs_update():
            pkgs.append(pkg)

    if not pkgs:
        logger.info("Nothing to do!")
        return

    logger.info("Packages to build: %s", pprint.pformat(pkgs))

    build_api = SourcehutBuildAPI(sourcehut_token)
    pending_packages = list(get_depgraph(pkgs))
    running_builds = []
    finished_urls = {}
    signature_urls = set()
    failed_package_names = set()

    def mark_pkgbase_failed(pkgbase):
        logger.error("Build failed: %s", pkgbase.name)
        for package in pkgbase.packages:
            failed_package_names.add(package.name)

    def job_success(pkgbase, job_id):
        artifacts = build_api.get_job_artifacts(job_id)
        for artifact in artifacts:
            name = artifact["name"]
            url = artifact["url"]

            if url.endswith(".sig"):
                signature_urls.add(url)
                continue

            if len(pkgbase.packages) == 1:
                pkgname = pkgbase.packages[0].name
            else:
                pkgname = infer_package_name_from_archive(name)

            finished_urls[pkgname] = url

    def queue_build(depgraph_entry, urls_to_install):
        tasks = []
        pkgdir = f"pkgbuild/{depgraph_entry.pkgbase.path}"

        if urls_to_install:
            steps = ["mkdir -p ~/depgraph_install && cd ~/depgraph_install"]
            filenames = []
            for url in urls_to_install:
                _, _, name = url.rpartition("/")
                filenames.append(name)
                steps.append(["curl", "-f", "-o", name, url])
            steps.append(["sudo", "pacman", "--noconfirm", "-U", *filenames])
            tasks.append(make_task("install-depgraph-artifacts", steps))

        check_this_pkg = check
        if depgraph_entry.pkgbase.name in SKIP_CHECK_PKGS:
            check_this_pkg = False

        tasks.append(
            make_task(
                "makepkg",
                [
                    ["cd", pkgdir],
                    [
                        "makepkg",
                        "--skippgpcheck",
                        "--check" if check_this_pkg else "--nocheck",
                        "--sign",
                        "--key",
                        GPG_KEY_ID,
                    ],
                ],
            )
        )

        artifacts = []
        for name in depgraph_entry.pkgbase.get_artifact_names():
            artifacts.append(f"{pkgdir}/{name}")
            artifacts.append(f"{pkgdir}/{name}.sig")

        manifest = make_manifest(
            packages=depgraph_entry.otherdepends,
            tasks=tasks,
            artifacts=artifacts,
        )
        job_id = build_api.submit_job(manifest)
        running_builds.append((depgraph_entry.pkgbase, job_id, "queued"))
        logging.info("Job %s submitted", job_id)

    while pending_packages or running_builds:
        logger.debug("pending_packages=%s", pprint.pformat(pending_packages))
        logger.debug("running_builds=%s", pprint.pformat(running_builds))
        new_running_builds = []
        for pkgbase, job_id, last_status in running_builds:
            status = build_api.get_job_status(job_id)
            if status != last_status:
                logger.info(
                    "Job %s to build %s is now %s (was %s).",
                    job_id,
                    pkgbase.name,
                    status,
                    last_status,
                )
                if status in ("failed", "cancelled"):
                    mark_pkgbase_failed(pkgbase)
                elif status == "success":
                    job_success(pkgbase, job_id)
                else:
                    new_running_builds.append((pkgbase, job_id, status))
            else:
                new_running_builds.append((pkgbase, job_id, status))

        running_builds = new_running_builds

        new_pending_packages = []
        for dge in pending_packages:
            for _, pkg in dge.graphdepends:
                if pkg.name in failed_package_names:
                    mark_pkgbase_failed(dge.pkgbase)
                    break
            else:
                try:
                    graphdepends_urls = dge.get_graphdepends_urls(finished_urls)
                except KeyError:
                    logger.debug(
                        "%s not scheduled due to missing graphdepends",
                        pprint.pformat(dge),
                    )
                    new_pending_packages.append(dge)
                    continue
                queue_build(dge, graphdepends_urls)

        pending_packages = new_pending_packages

        time.sleep(5)

    if finished_urls:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = pathlib.Path(tmpdir)

            filenames = []

            for url in itertools.chain(finished_urls.values(), signature_urls):
                _, _, filename = url.rpartition("/")
                filenames.append(filename)
                subprocess.run(
                    ["curl", "-f", "-o", filename, url],
                    check=True,
                    cwd=tmp_path,
                )

            repo_db_path = f"{REPO_NAME}.db.tar.xz"
            repo_db_remote = f"{S3_UPLOADS}{REPO_NAME}.db"
            subprocess.run(
                ["s3cmd", "get", repo_db_remote, repo_db_path],
                check=True,
                cwd=tmp_path,
            )
            subprocess.run(
                [
                    "repo-add",
                    "--sign",
                    "--key",
                    GPG_KEY_ID,
                    repo_db_path,
                    *(name for name in filenames if not name.endswith(".sig")),
                ],
                check=True,
                cwd=tmp_path,
            )
            subprocess.run(
                [
                    "s3cmd",
                    "put",
                    "-F",
                    f"{REPO_NAME}.db",
                    f"{REPO_NAME}.db.sig",
                    *filenames,
                    S3_UPLOADS,
                ],
                check=True,
                cwd=tmp_path,
            )

    if failed_package_names:
        logger.error(
            "Failed to build packages: %s", " ".join(sorted(failed_package_names))
        )
        sys.exit(1)


def aur_merge(remote):
    here = pathlib.Path(__file__).parent

    with tempfile.TemporaryDirectory() as tmp_git:
        tmp_git = pathlib.Path(tmp_git)
        subprocess.run(
            ["git", "clone", remote, tmp_git],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        pkgbase = load_package_from_dir(tmp_git)
        dirname = f"aur/{pkgbase.name}"

        subtree_cmd = "pull"
        if not (here / dirname).is_dir():
            subtree_cmd = "add"

        with git_lock:
            subprocess.run(
                ["git", "subtree", subtree_cmd, f"--prefix={dirname}", tmp_git, "HEAD"],
                check=True,
                cwd=here,
                env={
                    **os.environ,
                    "GIT_EDITOR": "/bin/true",
                },
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
            )


def import_from_aur(*pkgnames):
    for name in pkgnames:
        remote = f"https://aur.archlinux.org/{name}"
        aur_merge(remote)


def update(jobs=8):
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as executor:
        futures = []
        for package in find_packages():
            if package.aursrc:
                futures.append(executor.submit(aur_merge, package.aursrc))
        for future in tqdm.tqdm(futures):
            future.result()


def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = argh.ArghParser()
    parser.add_commands([orchestrate, import_from_aur, update])

    parser.dispatch()


if __name__ == "__main__":
    main()
