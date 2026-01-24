# Maintainer: Raphael Nestler <raphael.nestler@gmail.com>
# Contributor: Chloe Colman <chloe.colman7@gmail.com>
# Contributor: Sampson Crowley <sampsonsprojects@gmail.com>
# Contributor: Rhys Kenwell <redrield+aur@gmail.com>
# Github Contributors: https://github.com/SampsonCrowley/arch_packages/contributors.md

pkgname=heroku-cli
pkgver=10.16.0
pkgrel=1
pkgdesc="CLI to manage Heroku apps and services with forced auto-update removed"
arch=('any')
url="https://devcenter.heroku.com/articles/heroku-cli"
license=('custom' 'ISC')
depends=('nodejs>=20.18' 'nodejs<23')
makedepends=('yarn' 'git' 'npm')
optdepends=('git: Deploying to Heroku')
conflicts=('heroku-cli-bin' 'heroku-client-standalone' 'heroku-toolbelt' 'ruby-heroku')
source=("git+https://github.com/heroku/cli.git#commit=v${pkgver}")
sha256sums=('76c3007ec5a8e00354e505ac9dda648519f779c9ec0365f37f7c1410f41dcfd6')
sha512sums=('dcd018cab54f1013f9deff04f82118ec074ab160fd909fe8213953ec88c09f649e8075aab641daf6f7e137ba00007b8e80ba2900ba9a68ec0c2082610e7b1a31')
options=('!strip')
provides=('heroku' 'heroku-cli')

prepare() {
  pushd "$srcdir"

    pushd "cli"
      pushd packages/cli
        # remove forced auto-update plugin
        sed -i "/oclif\/plugin-update/d" ./package.json

        # Allow to use nodejs 22
        sed -i 's/"node": "20.x"/"node": ">=20 <23"/g' ./package.json

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
