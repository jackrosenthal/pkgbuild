# Maintainer: Owen Trigueros <owentrigueros@gmail.com>

pkgname=httpdirfs
pkgver=1.2.11
pkgrel=1
pkgdesc="A filesystem which allows you to mount HTTP directory listings"
arch=('x86_64')
url="https://github.com/fangfufu/httpdirfs"
license=('GPL')
depends=('gumbo-parser' 'fuse3' 'curl' 'expat' 'util-linux-libs' 'openssl')
makedepends=('meson' 'help2man' 'doxygen' 'graphviz')
source=("$pkgname-$pkgver.tar.gz::https://github.com/fangfufu/$pkgname/archive/$pkgver.tar.gz")
md5sums=("6a0f00154d3c20ec03363be7abe200f9")

build() {
  arch-meson "$pkgname-$pkgver" build -Dc_args="-std=gnu17"
  meson compile -C build
}

package() {
  meson install -C build --destdir "$pkgdir"
}
