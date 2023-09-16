# Maintainer:

pkgname=jellyfin-web
pkgver=10.8.10
pkgrel=3
pkgdesc='Web client for Jellyfin'
arch=('any')
url='https://jellyfin.org'
_url='https://github.com/jellyfin/jellyfin-web'
license=('GPL2')
makedepends=('git' 'nodejs' 'npm')
_commit='55714d5341d6bbfdb4d8b0b4c9b6955d4db14f34'
source=("$pkgname::git+$_url#commit=$_commit")
b2sums=('SKIP')

pkgver() {
  cd "$pkgname"

  git describe --tags | sed 's/^v//'
}

prepare() {
  cd "$pkgname"

  # download dependencies
  npm ci --no-audit --no-fund --no-update-notifier
}

build() {
  cd "$pkgname"

  npm run build:production
}

package() {
  cd "$pkgname"

  install -vd "$pkgdir/usr/share/$pkgname"
  cp -vr dist/* "$pkgdir/usr/share/$pkgname"
}

# vim: ts=2 sw=2 et:
