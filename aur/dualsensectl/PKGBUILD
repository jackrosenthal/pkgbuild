# Maintainer:

_pkgname="dualsensectl"
pkgname="$_pkgname"
pkgver=0.7
pkgrel=2
pkgdesc='Tool for controlling Sony PlayStation 5 DualSense controller on Linux'
url='https://github.com/nowrep/dualsensectl'
license=('GPL-2.0-or-later')
arch=('x86_64')

depends=(
  'dbus'
  'hidapi'
  'systemd-libs'
)
makedepends=(
  'meson'
)

_pkgsrc="$_pkgname-$pkgver"
_pkgext="tar.gz"
source=("$_pkgsrc.$_pkgext"::"$url/archive/refs/tags/v${pkgver}.$_pkgext")
sha256sums=('a615304596925738b12d0a499f31e1fe0cc3653da230edfe7c68637098ce6b72')

build() {
  arch-meson "$_pkgsrc" build
  meson compile -C build
}

package() {
  meson install -C build --destdir "$pkgdir"
  install -Dm644 "$_pkgsrc"/completion/dualsensectl -t "$pkgdir/usr/share/bash-completion/completions/"
  install -Dm644 "$_pkgsrc"/completion/_dualsensectl -t "$pkgdir/usr/share/zsh/site-functions/"
}
