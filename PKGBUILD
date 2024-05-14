# Maintainer: Giovanni Harting <539@idlegandalf.com>
# Contributor: Marius Lindvall <(firstname) {cat} varden {dog} info>

pkgname=jellyfin-mpv-shim
pkgver=2.7.0
pkgrel=2
pkgdesc='Cast media from Jellyfin Mobile and Web apps to MPV'
arch=(any)
url='https://github.com/jellyfin/jellyfin-mpv-shim'
license=(MIT)
depends=(mpv 'python>=3.6' python-mpv 'python-mpv-jsonipc>=1.1.9' 'python-jellyfin-apiclient>=1.8.1' tk)
makedepends=(python-build python-installer python-wheel gettext python-setuptools)
optdepends=(
  'python-pystray: systray support'
  'python-jinja: display mirroring support'
  'python-pywebview>=3.3.1: display mirroring support'
  'svp: SmoothVideo Project server'
  'mpv-shim-default-shaders: default shader pack'
  'python-pypresence: Discord Rich Presence integration'
)
source=("$pkgname-$pkgver.tar.gz::$url/archive/v$pkgver.tar.gz"
        "shaderpack.patch")
b2sums=('bf43d5094e5f23980e565decfa64cfce597a4ede0b164d179cf2acebc6b0c3794e9289b08a177ee9f828fdba09a2b852f838af2ce1ac32193bdc60e42c10f8dc'
        '864441ed1c42e1521b9e2775ad9a786ca1a3049220e45ac096540dfd7f3e24ac7e75f1f6f55ecb893dca74c61a519c978894543627c770fa32cd23409fc8b9b4')


prepare() {
  cd jellyfin-mpv-shim-$pkgver

  # remove default-shader-pack from packages
  patch -p1 < ../shaderpack.patch
}

build() {
  cd jellyfin-mpv-shim-$pkgver

  find -iname '*.po' | while read -r _file; do
    msgfmt "$_file" -o "${_file%.*}.mo"
  done

  python -m build --wheel --no-isolation
}

package() {
  cd jellyfin-mpv-shim-$pkgver

  install -Dm644 "LICENSE.md" "$pkgdir"/usr/share/licenses/$pkgname/LICENSE

  python -m installer --destdir="$pkgdir" dist/*.whl

  for i in 16 32 48 64 128 256; do
    install -Dvm644 jellyfin_mpv_shim/integration/jellyfin-$i.png "$pkgdir"/usr/share/icons/hicolor/${i}x${i}/apps/com.github.iwalton3.jellyfin-mpv-shim.png
  done

  install -Dm644 jellyfin_mpv_shim/integration/com.github.iwalton3.jellyfin-mpv-shim.desktop "$pkgdir"/usr/share/applications/$pkgname.desktop

  cd "$pkgdir"
  local site_packages=$(python -c "import site; print(site.getsitepackages()[0])")

  ln -s /usr/share/mpv-shim-default-shaders ${site_packages:1}/jellyfin_mpv_shim/default_shader_pack
}

# vim:set ts=2 sw=2 et:
