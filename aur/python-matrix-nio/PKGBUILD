# Maintainer: Matteo Piccinini (loacker) <matteo.piccinini@gmail.com>
# Contributor: Jonas Witschel <diabonas@archlinux.org>

pkgname=python-matrix-nio
pkgver=0.25.0
pkgrel=1
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
source=("$pkgname-$pkgver.tar.gz::https://api.github.com/repos/${pkgname#python-}/${pkgname#python-}/tarball/refs/tags/$pkgver")
b2sums=('45b455c8c2169c0c10f369cfb86bac4e258a8516f9fcaa083839a37dc64df9d749789942bf14881096a0ac771d77e8caac4dd6db2b5431771d184592e80f4f7c')

prepare() {
    tar zxvf "$pkgname-$pkgver.tar.gz" --strip-components=1 --one-top-level
}

build() {
    cd "$pkgname-$pkgver"
    python -m build --wheel --no-isolation
}

check() {
    cd "$pkgname-$pkgver"
    python -m pytest --benchmark-disable
}

package() {
    cd "$pkgname-$pkgver"
    python -m installer --destdir="$pkgdir" dist/*.whl
    install -Dm644 LICENSE.md "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}
