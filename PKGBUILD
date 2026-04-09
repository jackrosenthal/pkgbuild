# Maintainer: Raphael Nestler <raphael.nestler@gmail.com>
# Contributor: Chloe Colman <chloe.colman7@gmail.com>
# Contributor: Sampson Crowley <sampsonsprojects@gmail.com>
# Contributor: Rhys Kenwell <redrield+aur@gmail.com>
# Github Contributors: https://github.com/SampsonCrowley/arch_packages/contributors.md

pkgname=heroku-cli
pkgver=11.2.0
pkgrel=1
pkgdesc="CLI to manage Heroku apps and services with forced auto-update removed"
arch=('any')
url="https://devcenter.heroku.com/articles/heroku-cli"
license=('ISC')
depends=('nodejs>=22.22' 'nodejs<23')
makedepends=('git' 'npm')
optdepends=('git: Deploying to Heroku')
conflicts=('heroku-cli-bin' 'heroku-client-standalone' 'heroku-toolbelt' 'ruby-heroku')
source=("git+https://github.com/heroku/cli.git#commit=v${pkgver}")
sha256sums=('9203198f84faa714788da7123225a26ef6f50825fa60e58449448fe9043622b8')
sha512sums=('9c527883cc0b4723c52d5c6405506dc35e59c824f9fe94cee3f62f947d6fb477d8887945c4df6e9542d72cd347440953fc0bd1c976cb43bddf045ab190410051')
options=('!strip')
provides=('heroku' 'heroku-cli')

prepare() {
  pushd "$srcdir"

    pushd "cli"
      # remove forced auto-update plugin
      sed -i "/oclif\/plugin-update/d" ./package.json

      # install dependencies, must be done with npm again as of 11.0
      npm install

      # create base package
      npm run build
      npm prune --production
    popd
}

package() {
  local _installdir="$pkgdir/usr/lib/heroku"
  install -dm755 "$_installdir"
  install -dm755 "$pkgdir/usr/bin"

  cp -r "$srcdir/cli/package.json" "$srcdir/cli/node_modules" "$srcdir/cli/bin" "$srcdir/cli/dist" "$_installdir/"

  # completions
  local autocompletedir="$srcdir/cli/autocomplete-scripts"
  install -Dm644 "$autocompletedir/bash/heroku.bash" "$pkgdir/usr/share/bash-completion/completions/heroku"
  install -Dm644 "$autocompletedir/zsh/_heroku" "$pkgdir/usr/share/zsh/site-functions/_heroku"

  ln -sf "../lib/heroku/bin/run" "$pkgdir/usr/bin/heroku"

  # Remove empty directories
  find "${pkgdir}" -type d -empty -delete
}
