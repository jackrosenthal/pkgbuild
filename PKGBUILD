# Maintainer: Morten Linderud <foxboron@archlinux.org>
# Contributor: Alad Wenter <alad@archlinux.org>
# Contributor: Matthew McGinn <mamcgi@gmail.com>
# Contributor: Gryffyn
# Contributor: Tetsumi

pkgname=python-pygame
pkgver=2.6.1
pkgrel=1
pkgdesc="Python game library"
arch=('x86_64')
url="http://www.pygame.org"
license=('LGPL')
depends=('glibc' 'libpng' 'python' 'sdl2' 'sdl2_mixer' 'sdl2_ttf' 'sdl2_image' 'portmidi')
makedepends=('python-build' 'python-installer' 'python-setuptools' 'python-wheel' 'sdl2')
optdepends=(
    'python-numpy: for examples'
)
source=("https://pypi.io/packages/source/p/pygame/pygame-$pkgver.tar.gz")
sha256sums=('56fb02ead529cee00d415c3e007f75e0780c655909aaa8e8bf616ee09c9feb1f')
b2sums=('d4f32e2777c9b6e52e61849e816eb0092b10c7e01ba484499a167e4bfa5a7e2bec3ac103815d686a66f77eb74bf558d59f271e566bedc35210d104f69d925d87')

build() {
    cd pygame-"$pkgver"
    python -m build --wheel --no-isolation
}

package() {
    cd pygame-"$pkgver"
    python -m installer --destdir="$pkgdir" dist/*.whl
}
