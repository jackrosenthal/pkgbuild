# Maintainer: Joao Costa <arch@joaocosta.dev>
pkgname=bambustudio-appimage
_pkgname=BambuStudio
pkgver=2.2.2
pkgrel=1
pkgdesc="PC Software for BambuLab and other 3D printers"
arch=('x86_64')
url="https://github.com/bambulab/BambuStudio"
license=('AGPL-3.0')
provides=('bambustudio')
conflicts=('bambustudio' 'bambustudio-git' 'bambustudio-bin')
source=("${_pkgname}-${pkgver}.AppImage::https://github.com/bambulab/BambuStudio/releases/download/v02.02.02.56/Bambu_Studio_ubuntu-24.04_PR-8184.AppImage"
  "BambuStudio.desktop")
sha256sums=('ce28a910ccf9f251bffaec6e6c2779ddce818c9f56ddda09f7f67c549a7e65ae'
  '574f306d62113d0e4aa155294677486a6a144e45d9bbc61dcf4f4b934dba4d7b')

package() {
  cd "$srcdir"

  install -Dm755 "${_pkgname}-${pkgver}.AppImage" "$pkgdir/usr/bin/bambustudio"
  install -Dm644 "BambuStudio.desktop" "$pkgdir/usr/share/applications/BambuStudio.desktop"

  chmod +x "${_pkgname}-${pkgver}.AppImage"
  ./"${_pkgname}-${pkgver}.AppImage" --appimage-extract &>/dev/null

  if [ -f "squashfs-root/BambuStudio.png" ]; then
    install -Dm644 "squashfs-root/BambuStudio.png" "$pkgdir/usr/share/pixmaps/BambuStudio.png"
  else
    msg2 "Warning: Could not automatically find an icon file (BambuStudio.png) within the AppImage."
    msg2 "         Desktop entry icon might be missing."
  fi

  find squashfs-root -maxdepth 1 -iname 'LICENSE*' -print -exec install -Dm644 {} "$pkgdir/usr/share/licenses/$pkgname/LICENSE" \; || true

}
