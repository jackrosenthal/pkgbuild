# Maintainer: bemxio <bemxiov at protonmail dot com>
# Maintainer: Joseph Brains <jnbrains at gmail dot com>

_pkgname=android-apktool
pkgname=${_pkgname}-bin

pkgdesc="A tool for reverse engineering Android .apk files"

pkgver=3.0.2
pkgrel=1

arch=(any)

url="https://apktool.org"
license=("Apache-2.0")

depends=("java-runtime>=8")

provides=("${_pkgname}")
conflicts=("${_pkgname}" "${_pkgname}-git")

source=("https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_${pkgver}.jar"
  "apktool")
sha256sums=('eee4669a704a14e0623407e6701b0b91887e61e1e4049cb7a82833e14ae8b5fd'
            '48a5c9d664c88c8beac4a85461e84437d104a42dac6334322a3bafca12b63bae')

noextract=("apktool_${pkgver}.jar")

package() {
  # copy the main .jar file
  install -Dm644 "apktool_${pkgver}.jar" "${pkgdir}/usr/share/java/${_pkgname}/apktool.jar"

  # copy the executable script
  install -Dm755 apktool "${pkgdir}/usr/bin/apktool"
}
