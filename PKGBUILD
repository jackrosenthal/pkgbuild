# SPDX-License-Identifier: 0BSD
# Maintainer: M Stoeckl <com dоt mstoeckl аt code>
pkgname=windowtolayer
pkgver=0.2.0
pkgrel=1
pkgdesc='Modify existing Wayland clients using xdg-shell to draw as a wallpaper instead'
license=('GPL-3.0-or-later')
makedepends=('rust' 'cargo')
url='https://gitlab.freedesktop.org/mstoeckl/windowtolayer'
source=("https://gitlab.freedesktop.org/mstoeckl/$pkgname/-/archive/v$pkgver/$pkgname-v$pkgver.tar.gz")
sha256sums=('5bc3357aac0988f128503700d4e11ddd4aab0e730f8280630eab912210fbaa38')
arch=('i686' 'x86_64' 'arm' 'armv6h' 'armv7h' 'aarch64')

prepare() {
	cd "$pkgname-v$pkgver"
	cargo fetch --locked --target "$(rustc -vV | sed -n 's/host: //p')"
}

build() {
	cd "$pkgname-v$pkgver"
	CARGO_INCREMENTAL=0 cargo build --release --locked --offline
}

package() {
	cd "$pkgname-v$pkgver"
	install -D -m755 "target/release/windowtolayer" "$pkgdir/usr/bin/windowtolayer"
	install -Dm644 "COPYING" "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}
