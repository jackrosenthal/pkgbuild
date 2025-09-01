# Maintainer: Lili1228 <aur at lili dot lgbt>
pkgname=86box-roms
pkgver=5.0
pkgrel=1
pkgdesc='ROMs for the 86Box emulator'
arch=('any')
url='https://github.com/86Box/roms'
license=('custom')
options=('!strip')
source=("https://github.com/86Box/roms/archive/refs/tags/v${pkgver}.tar.gz")
sha512sums=('79cca126a6e8374a95df8d7f71dfdeb333d67e0aff5e2fc9eb863ceddfc7ca88af168f0cada67e34b4252c32a9ec56579b5a0c6641829a306a75e213a3e8575a')

package() {
    cd "${srcdir}/roms-${pkgver}"
    install -d "$pkgdir/usr/share/86Box/roms"
    cp -R [a-z]* "$pkgdir/usr/share/86Box/roms"
    install -Dm644 LICENSE "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
}
