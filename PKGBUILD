# Author:         David Rosca   <nowrep@gmail.com>
# Maintainer:  Martin Stibor <martin.von.reichenberg@gmail.com>

pkgname=dualsensectl
pkgver=0.7
pkgrel=3
pkgdesc='Tool for controlling SONY PlayStation DualSense gamepad on Linux'
arch=('x86_64' 'aarch64' 'riscv64' 'loong64')
url='https://github.com/nowrep/dualsensectl'
license=('GPL-2.0-only')
depends=('dbus' 'hidapi' 'libusb')
makedepends=('git' 'gcc' 'meson')
source=("${pkgname}-${pkgver}.tar.gz::${url}/archive/v${pkgver}.tar.gz")
sha256sums=('a615304596925738b12d0a499f31e1fe0cc3653da230edfe7c68637098ce6b72')

build() {
    cd "${srcdir}/${pkgname}-${pkgver}"
    arch-meson build
    meson compile -C build
}

package() {
    cd "${srcdir}/${pkgname}-${pkgver}"
    meson install -C build --destdir "${pkgdir}"

    install -Dm644 "${srcdir}/${pkgname}-${pkgver}/completion/dualsensectl" \
                -t            "${pkgdir}/usr/share/bash-completion/completions/"

    install -Dm644 "${srcdir}/${pkgname}-${pkgver}/completion/_dualsensectl" \
                -t            "${pkgdir}/usr/share/zsh/site-functions/"
}
