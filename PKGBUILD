# Maintainer: Jan de Groot <jgc@archlinux.org>

pkgname=gtk2
pkgver=2.14.4
pkgrel=1
pkgdesc="The GTK+ Toolkit (v2)"
arch=(i686 x86_64)
url="http://www.gtk.org/"
install=gtk2.install
depends=('atk>=1.24.0' 'pango>=1.22.0' 'libxcursor' 'libxinerama' 'libxrandr>=1.2.1' 'libxi' 'libcups>=1.3.8-2' 'libxcomposite' 'libxdamage' 'heimdal>=1.2' 'gnutls>=2.4.1' 'glib2>=2.18.2')
makedepends=('pkgconfig')
replaces=('gtkprint-cups' 'gail')
conflicts=('gtkprint-cups' 'gail')
provides=('gail=1.22.3')
options=('!libtool' '!docs')
backup=(etc/gtk-2.0/gtkrc)
license=('LGPL')
source=(http://ftp.gnome.org/pub/gnome/sources/gtk+/2.14/gtk+-${pkgver}.tar.bz2
	gtkclipboard-check.patch)
md5sums=('72bf65a54d2d29a6644dc0d28313ee67'
         '4025d3c15d6c6f73a032f403ffd4ff1c')

build() {
  cd ${startdir}/src/gtk+-${pkgver}
  # Workaround patch for flash
  patch -Np1 -i ${startdir}/src/gtkclipboard-check.patch || return 1

  ./configure --prefix=/usr --sysconfdir=/etc \
              --localstatedir=/var --with-xinput=yes \
	      --without-libjasper \
	      --with-included-loaders=png || return 1
  make || return 1
  make DESTDIR=${startdir}/pkg install || return 1

  echo 'gtk-fallback-icon-theme = "gnome"' > ${startdir}/pkg/etc/gtk-2.0/gtkrc || return 1
}
