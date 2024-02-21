FROM archlinux
WORKDIR /pkgbuild
RUN useradd -Um build
RUN echo "build ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
COPY --chown=build:build . /pkgbuild
RUN chown build:build /pkgbuild
COPY pacman.conf /etc/pacman.conf
COPY .s3cfg /root/.s3cfg
RUN pacman-key --init
RUN pacman-key --populate
RUN pacman-key -r 55E00EDED9D418CBACB39CAD184AD86A1B97C873
RUN pacman-key --lsign-key 55E00EDED9D418CBACB39CAD184AD86A1B97C873
RUN pacman -Syu --needed --noconfirm base base-devel python-argh python-tqdm s3cmd
RUN rm -rf /var/cache/pacman/pkg
