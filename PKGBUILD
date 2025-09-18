# Maintainer: Joao Costa <arch@joaocosta.dev>
pkgname=bambustudio-appimage
_pkgname=BambuStudio
pkgver=2.2.2
pkgrel=2
pkgdesc="PC Software for BambuLab and other 3D printers"
arch=('x86_64')
url="https://github.com/bambulab/BambuStudio"
license=('AGPL-3.0')
provides=('bambustudio')
conflicts=('bambustudio' 'bambustudio-git' 'bambustudio-bin')
source=("${_pkgname}-${pkgver}.AppImage::https://github.com/bambulab/BambuStudio/releases/download/v02.02.02.56/Bambu_Studio_ubuntu-24.04_PR-8184.AppImage"
  "BambuStudio.desktop"
  "BambuStudio.png"
  "LICENSE")
sha256sums=('ce28a910ccf9f251bffaec6e6c2779ddce818c9f56ddda09f7f67c549a7e65ae'
  '574f306d62113d0e4aa155294677486a6a144e45d9bbc61dcf4f4b934dba4d7b'
  '33f8ae4baa84e489b634e8d82a401b8813ce0402124b9041b60cdd9a7044597c'
  '57c8ff33c9c0cfc3ef00e650a1cc910d7ee479a8bc509f6c9209a7c2a11399d6')

package() {
  cd "$srcdir"

  chmod +x "${_pkgname}-${pkgver}.AppImage"
  mkdir -p "$pkgdir/usr/bin/"
  mv "${_pkgname}-${pkgver}.AppImage" "$pkgdir/usr/bin/bambustudio"
  install -Dm644 "BambuStudio.desktop" "$pkgdir/usr/share/applications/BambuStudio.desktop"
  install -Dm644 "BambuStudio.png" "$pkgdir/usr/share/pixmaps/BambuStudio.png"
  install -Dm644 "LICENSE" "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}
