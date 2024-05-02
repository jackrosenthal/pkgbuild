# Maintainer: Rafael Fontenelle <rafaelff@gnome.org>
# Contributor: Konstantin Gizdov <arch at kge dot pw>
# Contributor: Achilleas Pipinellis <axilleas at archlinux dot gr>

pkgname=vale
pkgver=3.4.2
pkgrel=1
pkgdesc="A customizable, syntax-aware linter for prose"
arch=('i686' 'x86_64')
url="https://github.com/errata-ai/vale"
license=('MIT')
makedepends=('go' 'rsync')
source=("${pkgname}-${pkgver}.tar.gz::${url}/archive/v${pkgver}.tar.gz")
sha256sums=('e1696739f13c8b579d96a9e4df4592f0bbda167aa74872eede6cc9482374d32b')

build() {
    cd ${pkgname}-${pkgver}
    export CGO_CPPFLAGS="${CPPFLAGS}"
    export CGO_CFLAGS="${CFLAGS}"
    export CGO_CXXFLAGS="${CXXFLAGS}"
    export CGO_LDFLAGS="${LDFLAGS}"
    export GOFLAGS="-buildmode=pie -trimpath -ldflags=-linkmode=external -mod=readonly -modcacherw"
    go build -ldflags="-s -w -X main.version=${pkgver}" -o bin/vale ./cmd/vale
}

check() {
  cd ${pkgname}-${pkgver}
  go test ./cmd/vale
}

package() {
    cd ${pkgname}-${pkgver}
    install -vDm755 bin/vale  "${pkgdir}/usr/bin/vale"
    install -vDm644 README.md "${pkgdir}/usr/share/doc/vale/README.md"
    install -vDm644 LICENSE   "${pkgdir}/usr/share/licenses/vale/LICENSE"
}
