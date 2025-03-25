# Maintainer: Manuel Stoeckl <com dоt mstoeckl аt wppkgb>
# SPDX-License-Identifier: 0BSD
pkgname=swaylock-plugin
pkgver=1.8.2
pkgrel=1
pkgdesc='A fork of the swaylock screen locker for Wayland supporting custom wallpaper drawing programs'
license=('MIT')
arch=('i686' 'x86_64' 'arm' 'armv6h' 'armv7h' 'aarch64')
makedepends=('meson' 'ninja' 'scdoc')
depends=('glibc' 'wayland' 'cairo' 'pam' 'libxkbcommon' 'systemd-libs' 'glib2' 'gdk-pixbuf2' 'swaybg')
optdepends=(
  'mpvpaper: to implement video backgrounds'
  'windowtolayer: to use a terminal as background'
)
url="https://github.com/mstoeckl/swaylock-plugin"
source=("https://github.com/mstoeckl/swaylock-plugin/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=("8ac27f421550169d8d3d9523772d69fb405fedd0e6a73169495d05da8fb6ab47")
build() {
    arch-meson "$pkgname-$pkgver" build
    meson compile -C build
}
package() {
    meson install -C build --destdir "$pkgdir"
    install -Dm644 "$pkgname-$pkgver/LICENSE" "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}

