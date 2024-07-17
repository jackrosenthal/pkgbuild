# Maintainer: Raphael Nestler <raphael.nestler@gmail.com>
# Contributor: Sampson Crowley <sampsonsprojects@gmail.com>
# Contributor: Rhys Kenwell <redrield+aur@gmail.com>
# Github Contributors: https://github.com/SampsonCrowley/arch_packages/contributors.md

pkgname=heroku-cli
pkgver=9.0.0
pkgrel=1
pkgdesc="CLI to manage Heroku apps and services with forced auto-update removed"
arch=('any')
url="https://devcenter.heroku.com/articles/heroku-cli"
license=('custom' 'ISC')
depends=('nodejs')
makedepends=('yarn' 'git' 'npm')
optdepends=('git: Deploying to Heroku')
conflicts=('heroku-cli-bin' 'heroku-client-standalone' 'heroku-toolbelt' 'ruby-heroku')
source=("git+https://github.com/heroku/cli.git#commit=v${pkgver}")
sha256sums=('3eea5da64c5cbdd034b2e7eee782337272a7fd2ff32d28c70f82ff199172e7b0')
sha512sums=('5746fa2947f73e08179982d4baa2afc3bef586af2d4f8d0de53d6b875205ad65c3e345905ca1eebdf6d18892ec54ace97dd337bf1dbe062bfbd9212d052776b1')
options=('!strip')
provides=('heroku' 'heroku-cli')

prepare() {
  pushd "$srcdir"

    pushd "cli"
      pushd packages/cli
        # remove forced auto-update plugin
        sed -i "/oclif\/plugin-update/d" ./package.json
        # remove pin to node 16
        sed -i 's/"node": "~16.20.0"/"node": ">=16"/g' ./package.json

        # install dependencies, must be done with yarn as of 7.60
        yarn install

        # create base package
        yarn pack --filename "heroku-v$VERSION-linux-x64.tar.xz"
        tar -xzvf "heroku-v$VERSION-linux-x64.tar.xz" -C "$srcdir/"
      popd
    popd

    # Remove any existing package
    rm -rf heroku/
    # final installation
    mv package heroku
    pushd heroku
      yarn --prod
    popd

    # unneeded compilation files
    for file in *; do
      if [[ "$file" = "heroku" ]]; then
        continue
      else
        rm -rf "$file"
      fi
    done
  popd
}

package() {
  install -dm755 "$pkgdir/usr/lib/heroku"
  install -dm755 "$pkgdir/usr/bin"
  install -dm755 "$pkgdir/usr/share/licenses/$pkgname"

  cp -a "$srcdir/heroku" "$pkgdir/usr/lib"

  # completions
  local autocompletedir="$srcdir/heroku/autocomplete-scripts"
  install -Dm644 "$autocompletedir/bash/heroku.bash" "$pkgdir/usr/share/bash-completion/completions/heroku"
  install -Dm644 "$autocompletedir/zsh/_heroku" "$pkgdir/usr/share/zsh/site-functions/_heroku"

  ln -sf "../../../lib/heroku/LICENSE" "$pkgdir/usr/share/licenses/$pkgname"
  ln -sf "../lib/heroku/bin/run" "$pkgdir/usr/bin/heroku"

  # Remove empty directories
  find "${pkgdir}" -type d -empty -delete
}
