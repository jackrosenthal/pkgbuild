# Maintainer: Matteo Piccinini (loacker) <matteo.piccinini@gmail.com>
# Contributor:

pkgname=python-matrix-nio
_name=${pkgname#python-}
pkgver=0.24.0
pkgrel=4
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
changelog="CHANGELOG.md"
source=("$_name-$pkgver.tar.gz::https://api.github.com/repos/$_name/$_name/tarball/refs/tags/$pkgver")
b2sums=('c93bdf9c5944c36aaeb5560600c99daf3a45f77291c655c2baaf5ac48e3d630cc85c42505aea89d2ff46d647a89736481883182d9b9f6c4c8284914e8463a36e')

prepare() {
    tar zxvf "$_name-$pkgver.tar.gz" --strip-components=1 --one-top-level
}

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
