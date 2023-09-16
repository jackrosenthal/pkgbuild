# Maintainer:

pkgname=jellyfin-server
_pkgname="${pkgname%-server}"
pkgver=10.8.10
pkgrel=3
pkgdesc='Jellyfin server backend'
arch=('x86_64')
url='https://jellyfin.org'
_url='https://github.com/jellyfin/jellyfin'
license=('GPL2')
_dotnet_ver=6.0
_dotnet_runtime=linux-x64
depends=(
  'bash'
  'ffmpeg'
  'sqlite'
  'fontconfig'
)
makedepends=(
  'git'
  "dotnet-sdk-$_dotnet_ver"
)
optdepends=('jellyfin-web: to run web-app on the same machine')
backup=(
  "etc/$_pkgname/logging.json"
  "etc/$_pkgname/$_pkgname.env"
)
options=('!debug')
_commit='2cd29d1cfd5cb2586aab3862e857dc85e0117ca4'
source=(
  "$pkgname::git+$_url#commit=$_commit"
  'sysusers.conf'
  'tmpfiles.conf'
  'fix-envfile-path.patch'
  'fix-libexec-path.patch'
)
sha512sums=('SKIP'
            '9f62481faa5f6a2fad75b0a5bb727c74f46ada991aff938db225dee0232a2c948ba3e22f56b8fdaf960901b37d8cd6c292665dac1c954c6bc4b5e104da45ef6f'
            '3e12ec3d3fcb15975d5f86bc3ce3363ae89b0e9e0b2580c29fc8a612c0220a74a067138b15c48ae27bb3c5777eca33055f10651949678a1ee7bd094293f6abb6'
            '2b41106056fda917fbbe3411afc4b6c492b380909b54129a4aa0712246a6c991f7706a59a08b88cbb20a70d5a9a72797606189949a840d09b6ec6df1e605c9f5'
            'f652c115f4a14c525ca2f2d9c45add9c4f38bc62acdb22d74faafc76756c54d65d16875a1f4bc8f06c615844f2642e71507d335ec4d03d3b906c4adf3f148009')
b2sums=('SKIP'
        'f73c72e1d66480c410dbe71be1af91a2bd76206dfed76e64b8264ee3537f6eb477bcba905ce69a0ec8b273e33c2e46439b9b32ce21543a48d98d80434a46a781'
        'bc8001cf28ebf76a125e7ab0d9d5a8fcf35e0def5b907dc5fe90e16cdbb3fdf8b7f098779ced9a44e7a3918ee605058b379d445a224178456a32a6a99cd084b4'
        'f1ddd8c2458594de82c185a840dd94a4611d5f3c1ba42a731adc8779764a1ce0509989ccadff7289f9ee173e9bba2dc0ed7f73bb7586808b3cf677c4739a4b31'
        '2450922cfa2553a9fc7cc080ebe610e55611ce6d90307794127981424a4d8d1276a1c76268e9b1ad9d5502759dfd21e48dae173fdb38764fc82d5d48b6a72dba')

pkgver() {
  cd "$pkgname"

  git describe --tags | sed 's/^v//'
}

prepare() {
  cd "$pkgname"

  # fix envfile path in systemd service
  patch -p1 -i "$srcdir/fix-envfile-path.patch"

  # fix path for libexec (/usr/libexec is not used on Arch)
  patch -p1 -i "$srcdir/fix-libexec-path.patch"
}

build(){
  cd "$pkgname"

  # disable dotnet telemetry
  export DOTNET_CLI_TELEMETRY_OPTOUT=1
  export DOTNET_SKIP_FIRST_TIME_EXPERIENCE=1
  export DOTNET_NOLOGO=1

  # force dotnet to use 6.0 (incompatible with 6.0+…)
  dotnet new globaljson --sdk-version "$_dotnet_ver" --roll-forward latestMinor --force

  dotnet \
    publish \
    Jellyfin.Server \
    --configuration Release \
    --self-contained \
    --runtime "$_dotnet_runtime" \
    -p:DebugSymbols=false \
    -p:DebugType=none
}

package() {
  cd "$pkgname"

  # install binaries
  install -vd "$pkgdir/usr/"{lib,bin}
  cp -r "Jellyfin.Server/bin/Release/net$_dotnet_ver/$_dotnet_runtime/publish" "$pkgdir/usr/lib/jellyfin"
  ln -sf /usr/lib/jellyfin/jellyfin "$pkgdir/usr/bin/jellyfin"

  # ensure binaries have correct permissions
  chmod 755 "$pkgdir/usr/lib/$_pkgname/"{jellyfin,createdump}

  # logging configuration
  install -vDm640 \
    Jellyfin.Server/Resources/Configuration/logging.json \
    -t "$pkgdir/etc/$_pkgname"

  cd fedora

  # systemd integration
  install -vDm644 jellyfin.service -t "$pkgdir/usr/lib/systemd/system"
  install -vDm644 "$srcdir/sysusers.conf" "$pkgdir/usr/lib/sysusers.d/$_pkgname.conf"
  install -vDm644 "$srcdir/tmpfiles.conf" "$pkgdir/usr/lib/tmpfiles.d/$_pkgname.conf"
  install -vDm640 jellyfin.env -t "$pkgdir/etc/$_pkgname"

  # firewalld configuration
  install -vDm644 jellyfin-firewalld.xml "$pkgdir/usr/lib/firewalld/services/$_pkgname.xml"

  # admin restart capabilities
  install -vdm750 "$pkgdir/etc/sudoers.d"
  install -vDm600 jellyfin.sudoers "$pkgdir/etc/sudoers.d/jellyfin"
  install -vDm755 restart.sh -t "$pkgdir/usr/lib/$_pkgname"
}

# vim: ts=2 sw=2 et:
