# Maintainer: Manuel Stoeckl <com dоt mstoeckl аt wppkgb>
# SPDX-License-Identifier: 0BSD
pkgname=swaylock-plugin
pkgver=1.8.1
pkgrel=1
pkgdesc='A fork of the swaylock screen locker for Wayland supporting custom wallpaper drawing programs'
license=('MIT')
arch=('i686' 'x86_64' 'arm' 'armv6h' 'armv7h' 'aarch64')
makedepends=('meson' 'ninja' 'scdoc')
depends=('glibc' 'wayland' 'cairo' 'pam' 'libxkbcommon' 'systemd-libs' 'glib2' 'gdk-pixbuf2')
optdepends=(
  'mpvpaper: to implement video backgrounds'
  'windowtolayer: to use a terminal as background'
)
url="https://github.com/mstoeckl/swaylock-plugin"
source=("https://github.com/mstoeckl/swaylock-plugin/archive/refs/tags/v1.8.1.tar.gz")
sha256sums=("d02d540305944b350b21d2875d891a2d6288a059c70312ad0aca43d91bfc8cfb")
build() {
    arch-meson "$pkgname-$pkgver" build
    meson compile -C build
}
package() {
    meson install -C build --destdir "$pkgdir"
    install -Dm644 "$pkgname-$pkgver/LICENSE" "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}

