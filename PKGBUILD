#
# PKGBUILD for minipro (stable)
#
# Maintainer: uffe _.at._ uffe _.dot._ org
#

pkgname=minipro
pkgver=0.7.1
pkgrel=2

pkg_name_ver="${pkgname}-${pkgver}"
pkgdesc="Open source chip programming utility for autoelectric.cn MiniPro TL866xx series (TL866CS, TL866A, and TL866II+)"

url="https://gitlab.com/DavidGriffith/minipro"
arch=("i686" "x86_64")
license=("GPL-3.0-only")
makedepends=()
depends=("libusb")
optdepends=("srecord: Motorola srecord format")
#source=(${pkgname}.src.tgz::https://gitlab.com/DavidGriffith/minipro/-/archive/${pkgver}/${pkg_name_ver}.tar.gz)
source=(${pkgname}.src.tgz::https://661.org/files/${pkgname}/${pkg_name_ver}.tar.gz)
conflicts=("minipro")
provides=("minipro")
# https://661.org/files/minipro/checksums.txt
sha256sums=('714214fc4e3ee37c36ff3b9ae68f65984cba727110c1151d389559e02603654e')


prepare()
{
  cd "${srcdir}/${pkg_name_ver}"
}

build()
{
  cd "${srcdir}/${pkg_name_ver}"

  # MAKEFLAGS="-j1": temporary hack to prevent parallel compile - see link:  https://gitlab.com/DavidGriffith/minipro/-/commit/b2fd68da00154608bcaacde01845466e51795a7d
  #make PREFIX="/usr" MAKEFLAGS="-j1"
  make PREFIX="/usr"
}

package()
{
  cd "${srcdir}/${pkg_name_ver}"

  make DESTDIR="${pkgdir}" PREFIX="/usr" COMPLETIONS_DIR="/usr/share/bash-completion/completions" install
}

# vim: ts=2 sw=2 et:
#
# EOF
#
