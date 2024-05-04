# Maintainer: Matteo Piccinini (loacker) <matteo.piccinini@gmail.com>
# Contributor:

pkgname=python-matrix-nio
_name=${pkgname#python-}
pkgver=0.24.0
pkgrel=3
pkgdesc="Python Matrix client library, designed according to sans I/O principles"
arch=("any")
url="https://github.com/matrix-nio/matrix-nio"
license=("ISC")
depends=('python'
         'python-aiohttp'
         'python-aiofiles'
         'python-h11'
         'python-h2'
         'python-jsonschema'
         'python-unpaddedbase64'
         'python-pycryptodome'
         'python-aiohttp-socks')
makedepends=('python-build'
         'python-installer'
         'python-poetry-core')
checkdepends=('python-pytest'
              'python-pytest-isort'
              'python-pytest-cov'
              'python-hyperframe'
              'python-hypothesis'
              'python-hpack'
              'python-faker'
              'mypy'
              'python-pytest-aiohttp'
              'python-aioresponses'
              'python-pytest-benchmark'
              'python-pytest-asyncio'
              'python-ruff'
              'python-olm'
              'python-peewee'
              'python-cachetools'
              'python-atomicwrites')
optdepends=('python-olm: end-to-end encryption support'
            'python-peewee: end-to-end encryption support'
            'python-cachetools: end-to-end encryption support'
            'python-atomicwrites: end-to-end encryption support')
provides=("$pkgname")
changelog="CHANGELOG.md"
source=("$_name-$pkgver.tar.gz::https://github.com/$_name/$_name/archive/refs/tags/$pkgver.tar.gz")
b2sums=('f4ff411701701d44082e452428e0866eb579ecdf833586d5524c77e3a3f0335c8af2af4f0ebd5a8f943986eb41b6e611293d9e2916da33d034ed6cc455df38b5')

build() {
    cd "$_name-$pkgver"
    python -m build --wheel --no-isolation
}

check() {
    cd "$_name-$pkgver"
    python -m pytest --benchmark-disable
}

package() {
    cd "$_name-$pkgver"
    python -m installer --destdir="$pkgdir" dist/*.whl
    install -Dm644 LICENSE.md "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}
