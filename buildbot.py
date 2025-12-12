#!/usr/bin/env python3

import concurrent.futures
import dataclasses
import json
import logging
import os
import pathlib
import shlex
import subprocess
import tempfile
import threading
from pathlib import Path

import argh
import tqdm

AUR_GITHUB_MIRROR = "https://github.com/archlinux/aur.git"
REPO_NAME = "jmr"
REPO_URL = "https://archlinux-jmr.s3.us-west-004.backblazeb2.com/$repo/$arch"
S3_UPLOADS = f"s3://archlinux-jmr/{REPO_NAME}/x86_64/"
GPG_KEY_ID = "55E00EDED9D418CBACB39CAD184AD86A1B97C873"
git_lock = threading.Lock()

SKIP_CHECK_PKGS = []
ALTERNATIVES = {
    "cargo": "rust",
}

logger = logging.getLogger(__name__)


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
    aur: bool = False
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

        # If a package depends on other packages provided by this pkgbase, we
        # don't need it for building purposes.
        for pkg in self.packages:
            pkgs.discard(pkg.name)
            pkgs.discard(f"{pkg.name}={self.pkgver}")
            pkgs.discard(f"{pkg.name}={self.pkgver}-{self.pkgrel}")
            pkgs.discard(f"{pkg.name}={self.epoch}:{self.pkgver}")
            pkgs.discard(f"{pkg.name}={self.epoch}:{self.pkgver}-{self.pkgrel}")

        # Empty package specified by amdgpu-pro-installer.
        pkgs.discard("")

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
        # Not sure where these -debug packages came from.  They don't exist.
        return [line.rstrip().split("/")[-1] for line in lines if "-debug-" not in line]


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
        pkgbase.aur = True
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


def generate_dockerfile(
    pkgbase, artifacts=None, base_image: str = "docker.io/library/pkgbuild:latest"
):
    if not artifacts:
        artifacts = pkgbase.get_artifact_names()

    def _lines():
        yield f"FROM {base_image}"
        build_deps = sorted(pkgbase.get_build_dependencies(check=False))
        if build_deps:
            pkgs_quoted = " ".join(shlex.quote(x) for x in build_deps)
            yield f"RUN pacman -S --needed --noconfirm {pkgs_quoted}"
        yield f"WORKDIR /pkgbuild/{pkgbase.path}"
        yield "USER build"
        yield 'ENV PATH="/pkgbuild/bin:$PATH"'
        yield "RUN makepkg --skippgpcheck --nocheck --nosign --holdver"
        artifacts_quoted = " ".join(shlex.quote(x) for x in artifacts)
        yield "USER root"
        yield f"RUN tar cf /pkgbuild/binpkgs.tar {artifacts_quoted}"

    return "".join(f"{x}\n" for x in _lines())


def dockerbuild(
    pkg_dir: str,
    output_dir: str = "/tmp",
    plan: str = "",
    base_image: str = "docker.io/library/pkgbuild:latest",
):
    artifacts = None
    if plan:
        plan_dict = json.loads(plan)
        artifacts = plan_dict["artifacts"]
    pkgbase = load_package_from_dir(Path(pkg_dir))
    tag = f"makepkg-{pkgbase.name}:latest"
    subprocess.run(
        ["docker", "buildx", "build", "--pull=false", "-t", tag, "--load", "-"],
        input=generate_dockerfile(pkgbase, artifacts=artifacts, base_image=base_image),
        check=True,
        encoding="utf-8",
    )
    with open(f"/tmp/{pkgbase.name}-binpkgs.tar", "wb") as output_file:
        subprocess.run(
            ["docker", "run", "--rm", tag, "cat", "/pkgbuild/binpkgs.tar"],
            stdout=output_file,
            check=True,
        )


def plan_builds(rebuild_all: bool = False):
    pkgs = []
    for pkg in find_packages():
        if rebuild_all or pkg.needs_update():
            pkgs.append(pkg)

    depgraph = get_depgraph(pkgs)

    with_graphdepends = []
    no_graphdepends = []

    for dge in depgraph:
        if dge.graphdepends:
            with_graphdepends.append(dge)
        else:
            no_graphdepends.append(dge)

    result = []
    for dge in no_graphdepends:
        artifacts = dge.pkgbase.get_artifact_names()
        result.append(
            {
                "pkgbase": dge.pkgbase.name,
                "subdir": str(dge.pkgbase.path),
                "version": dge.pkgbase.fmt_version(),
                "packages": [x.name for x in dge.pkgbase.packages],
                "artifacts": artifacts,
                "artifacts_path_expr": f"/tmp/{dge.pkgbase.name}-binpkgs.tar",
            }
        )

    print(f"builds={json.dumps(result, sort_keys=True)}")


def s3cmd(argv, cwd):
    access_key = os.environ["S3_ACCESS_KEY"]
    secret_key = os.environ["S3_SECRET_KEY"]
    subprocess.run(
        ["s3cmd", "--access_key", access_key, "--secret_key", secret_key, *argv],
        check=True,
        cwd=cwd,
    )


def publish(workdir: str):
    workdir = Path(workdir)

    for tarpath in workdir.glob("*-binpkgs.tar"):
        subprocess.run(["tar", "xf", tarpath], check=True, cwd=workdir)
        tarpath.unlink()

    packages = list(workdir.glob("*.pkg.tar.zst"))

    logger.info("Workdir: %s", workdir)
    logger.info("Workdir listing: %s", list(workdir.iterdir()))

    if not packages:
        logger.warning("No packages to publish... exiting!")
        return 0

    signatures = []

    subprocess.run(
        ["gpg", "--import"],
        input=os.environ["GPG_PRIVATE_KEY"],
        encoding="utf-8",
    )

    for pkg_path in packages:
        sig_path = f"{pkg_path}.sig"
        signatures.append(sig_path)
        subprocess.run(
            [
                "gpg",
                "--detach-sign",
                "--batch",
                "--passphrase",
                "",
                "--output",
                sig_path,
                "--sign",
                pkg_path,
            ],
            check=True,
            cwd=workdir,
        )

    repo_db_path = f"{REPO_NAME}.db.tar.xz"
    repo_db_remote = f"{S3_UPLOADS}{REPO_NAME}.db"
    s3cmd(["get", repo_db_remote, repo_db_path], cwd=workdir)
    subprocess.run(
        [
            "repo-add",
            "--sign",
            "--key",
            GPG_KEY_ID,
            repo_db_path,
            *packages,
        ],
        check=True,
        cwd=workdir,
    )
    s3cmd(
        [
            "put",
            "-F",
            f"{REPO_NAME}.db",
            f"{REPO_NAME}.db.sig",
            *packages,
            *signatures,
            S3_UPLOADS,
        ],
        cwd=workdir,
    )


def aur_merge(name):
    here = pathlib.Path(__file__).parent

    with tempfile.TemporaryDirectory() as tmp_git:
        tmp_git = pathlib.Path(tmp_git)
        subprocess.run(
            ["git", "clone", "--branch", name, "--single-branch", AUR_GITHUB_MIRROR, tmp_git],
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
        remote = f"https://aur.archlinux.org/{name}.git"
        aur_merge(remote)


def update(jobs=8):
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as executor:
        futures = []
        for package in find_packages():
            if package.aur:
                futures.append(executor.submit(aur_merge, package.name))
        for future in tqdm.tqdm(futures):
            future.result()


def depgraph():
    """Print a dependency graph starting from packages nothing depends on."""
    packages = list(find_packages())

    # Build dependency map: package -> set of packages it depends on (within tree)
    pkg_deps = {}
    all_local_pkgs = set()

    for pkgbase in packages:
        for pkg in pkgbase.packages:
            all_local_pkgs.add(pkg.name)

    for pkgbase in packages:
        build_deps = pkgbase.get_build_dependencies(check=True)
        # Filter to only dependencies that are in our local tree
        local_deps = build_deps & all_local_pkgs

        for pkg in pkgbase.packages:
            pkg_deps[pkg.name] = set(local_deps)

    def get_transitive_deps(pkg_name, visited=None):
        """Get all transitive dependencies of a package."""
        if visited is None:
            visited = set()
        if pkg_name in visited:
            return set()
        visited.add(pkg_name)

        result = set()
        for dep in pkg_deps.get(pkg_name, set()):
            result.add(dep)
            result.update(get_transitive_deps(dep, visited.copy()))
        return result

    def get_minimal_deps(deps):
        """Filter out transitive dependencies, keeping only minimal set."""
        minimal_deps = set(deps)
        for dep in deps:
            minimal_deps -= get_transitive_deps(dep)
        return minimal_deps

    def print_tree(pkgs, indent=0, visited=None):
        """Recursively print packages and their dependencies."""
        if visited is None:
            visited = set()

        minimal_pkgs = sorted(get_minimal_deps(pkgs) - visited)

        for pkg in minimal_pkgs:
            visited.add(pkg)
            print("\t" * indent + pkg)
            print_tree(pkg_deps.get(pkg, set()), indent + 1, visited.copy())

    print_tree(set(pkg_deps.keys()))


def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = argh.ArghParser()
    parser.add_commands([import_from_aur, update, plan_builds, dockerbuild, publish, depgraph])

    parser.dispatch()


if __name__ == "__main__":
    main()
