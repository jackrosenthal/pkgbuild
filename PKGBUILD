# Maintainer: bemxio <bemxiov at protonmail dot com>
# Maintainer: Joseph Brains <jnbrains at gmail dot com>

_pkgname=android-apktool
pkgname=${_pkgname}-bin

pkgdesc="A tool for reverse engineering Android .apk files"

pkgver=3.0.0
pkgrel=1

arch=(any)

url="https://github.com/iBotPeaches/Apktool"
license=("Apache-2.0")

depends=("java-runtime>=8")

provides=("${_pkgname}")
conflicts=("${_pkgname}" "${_pkgname}-git")

source=("https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_${pkgver}.jar"
  "apktool")
sha256sums=('06fed946b272eb777fdb6dc0bbef0e13e0d393144ee367a510acba18b41597b9'
  '48a5c9d664c88c8beac4a85461e84437d104a42dac6334322a3bafca12b63bae')

noextract=("apktool_${pkgver}.jar")

package() {
  # copy the main .jar file
  install -Dm644 "apktool_${pkgver}.jar" "${pkgdir}/usr/share/java/${_pkgname}/apktool.jar"

  # copy the executable script
  install -Dm755 apktool "${pkgdir}/usr/bin/apktool"
}
