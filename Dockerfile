FROM archlinux
WORKDIR /pkgbuild
RUN useradd -Um build
COPY --chown=build:build . /pkgbuild
COPY pacman.conf /etc/pacman.conf
RUN pacman-key --init
RUN pacman-key --populate
RUN pacman-key -r 55E00EDED9D418CBACB39CAD184AD86A1B97C873
RUN pacman-key --lsign-key 55E00EDED9D418CBACB39CAD184AD86A1B97C873
RUN pacman -Syu --needed --noconfirm base base-devel python-argh python-requests python-tqdm
