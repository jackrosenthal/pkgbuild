# Maintainer: Joan Figueras <ffigue at gmail dot com>
# Contributor: Black_Codec <orso.f.regna@gmail.com>

pkgname=guacamole-server
pkgver=1.6.0
pkgrel=2
pkgdesc="Guacamole proxy daemon"
arch=('i686' 'x86_64' 'armv7h')
url="http://guacamole.sourceforge.net/"
license=('Apache-2.0')
replaces=('guacd' 'libguac' 'libguac-client-ssh' 'libguac-client-vnc' 'libguac-client-rdp')
depends=('pango' 'openssl' 'libvorbis' 'libwebp' 'ffmpeg4.4')
makedepends=('libpulse' 'libvorbis' 'openssl' 'libssh' 'libvncserver' 'pango' 'libtelnet')
optdepends=('libssh: for ssh protocol support'
'libvncserver: for vnc protocol support'
'freerdp2: for rdp protocol support'
'libpulse: for pulseaudio support'
'libtelnet: for telnet protocol support'
'monospace: any monospace font such as terminus-font, ttf-inconsolata or ttf-fira-mono. Without it, SSH will not work'
'libwebsockets: Support for Kubernetes'
)
install=$pkgname.install

source=("http://apache.org/dyn/closer.cgi?action=download&filename=guacamole/${pkgver}/source/${pkgname}-${pkgver}.tar.gz"
        "guacd.conf")

backup=('etc/guacamole/guacd.conf')

md5sums=('3738aa1137e9af2750a4620c568964d5'
         'ab0ac97ad76d16be73768f89abb6ee7e'
         '4544b6b1e9999b9ef9157c20ef9e173c')

# Patches/Commits/Pull requests
source+=("https://github.com/apache/guacamole-server/pull/591/commits/2e2a33621d673345e7b9d22c9388be80c6d77598.patch")

prepare() {
	cd "$srcdir"/$pkgname-$pkgver
	for patch in ../*patch; do
	    patch -Np1 -i $patch
	done
}

build() {
	cd "$srcdir"/$pkgname-$pkgver
	export PKG_CONFIG_PATH='/usr/lib/ffmpeg4.4/pkgconfig'
	#./configure --prefix=/usr --sbindir=/usr/bin --with-systemd-dir=/usr/lib/systemd/system CPPFLAGS="-Wno-error=pedantic -Wno-error=deprecated-declarations"
	./configure --prefix=/usr --sbindir=/usr/bin --with-systemd-dir=/usr/lib/systemd/system CPPFLAGS="-Wno-error=pedantic"
	make
}
 
package() {
	cd "$srcdir"/$pkgname-$pkgver
	make DESTDIR="$pkgdir" install
	mkdir -p "$pkgdir"/etc/guacamole
	cp -f ../guacd.conf "$pkgdir"/etc/guacamole/
}
