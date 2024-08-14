# Maintainer: Lili1228 <aur at lili dot lgbt>
pkgname=86box-roms
pkgver=4.2
pkgrel=1
pkgdesc='ROMs for the 86Box emulator'
arch=('any')
url='https://github.com/86Box/roms'
license=('custom')
options=('!strip')
source=("https://github.com/86Box/roms/archive/refs/tags/v${pkgver}.tar.gz")
sha512sums=('652388640d80ae4a81497419b438026a3173e858c7399ac99631e5f179024fecfa41c6b3cd053522c6c6369a9005247770183285e5711ac3c829353e708f6747')

package() {
    cd "${srcdir}/roms-${pkgver}"
    install -d "$pkgdir/usr/share/86Box/roms"
    cp -R [a-z]* "$pkgdir/usr/share/86Box/roms"
    install -Dm644 LICENSE "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
}
