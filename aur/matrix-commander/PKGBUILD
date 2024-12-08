# Maintainer: Mark Collins <tera_1225 hat hotmail.com>
pkgname=matrix-commander
pkgver=8.0.4
pkgrel=1
pkgdesc="Simple CLI-based Matrix client"
arch=('any')
url="https://github.com/8go/matrix-commander"
license=('GPL-3.0-or-later')
makedepends=(
  "python-build"
  "python-installer"
  "python-wheel"
)
depends=(
  "bash"
  "python"
  "python-aiohttp"
  "python-async-timeout"
  "python-aiofiles"
  "python-emoji"
  "python-markdown"
  "python-matrix-nio" # AUR
  "python-pillow"
  "python-setuptools"
  "python-magic"
  "python-pyxdg"
  "python-atomicwrites"
  "python-cachetools"
  "python-olm"
  "python-peewee"
)
optdepends=(
  "python-notify2: needed for notifications on desktop systems"
)
provides=()
conflicts=()
source=("${pkgname}-${pkgver}::https://files.pythonhosted.org/packages/source/${pkgname::1}/${pkgname}/${pkgname/-/_}-${pkgver}.tar.gz")
sha256sums=('464f7a4e3a632f5f13f831b882484d91552e3868292a63b9671cc1562f513fef')

build() {
  cd "${srcdir}/${pkgname/-/_}-${pkgver}"
  python -m build --wheel --no-isolation
}

package() {
  cd "${srcdir}/${pkgname/-/_}-$pkgver"
  python -m installer --destdir="$pkgdir" dist/*.whl
}

