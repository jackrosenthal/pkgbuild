# Maintainer: Lili1228 <aur at lili dot lgbt>
pkgname=86box-roms
pkgver=6.0
pkgrel=1
pkgdesc='ROMs for the 86Box emulator'
arch=('any')
url='https://github.com/86Box/roms'
license=('custom')
options=('!strip')
source=("https://github.com/86Box/roms/archive/refs/tags/v${pkgver}.tar.gz")
sha512sums=('66a07b45d9f785322e71a0e3cb52eb9020c7d02dd3ca5945e463bf78b484911ea55779fdb676d5f754a70cbf5a54d3afdc574168098de44470fad6409871d3b5')

package() {
    cd "${srcdir}/roms-${pkgver}"
    install -d "$pkgdir/usr/share/86Box/roms"
    cp -R [a-z]* "$pkgdir/usr/share/86Box/roms"
    install -Dm644 LICENSE "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
}
