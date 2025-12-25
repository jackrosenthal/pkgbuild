# Maintainer: Lili1228 <aur at lili dot lgbt>
pkgname=86box-roms
pkgver=5.3
pkgrel=1
pkgdesc='ROMs for the 86Box emulator'
arch=('any')
url='https://github.com/86Box/roms'
license=('custom')
options=('!strip')
source=("https://github.com/86Box/roms/archive/refs/tags/v${pkgver}.tar.gz")
sha512sums=('cd0a3602e5a63964517fe3ff421317a7132cbbbb8340cd5fa4ba6ec141b5f6e8edafac94d0c2ba62c40f54625774773992c0267f9b53e2faaac4daf6f3cb7e2f')

package() {
    cd "${srcdir}/roms-${pkgver}"
    install -d "$pkgdir/usr/share/86Box/roms"
    cp -R [a-z]* "$pkgdir/usr/share/86Box/roms"
    install -Dm644 LICENSE "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
}
