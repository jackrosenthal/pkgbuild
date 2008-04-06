# $Id: PKGBUILD,v 1.109 2008/03/12 21:06:10 jgc Exp $
# Maintainer: Jan de Groot <jgc@archlinux.org>

pkgname=gtk2
pkgver=2.12.9
pkgrel=1
pkgdesc="The GTK+ Toolkit (v2)"
arch=(i686 x86_64)
url="http://www.gtk.org/"
install=gtk2.install
depends=('atk>=1.22.0' 'pango>=1.20.0' 'libxcursor' 'libxinerama' 'libxrandr>=1.2.1' 'libxi' 'libcups>=1.3.6' 'libxcomposite' 'libxdamage' 'glib2>=2.16.1')
makedepends=('pkgconfig')
replaces=('gtkprint-cups')
conflicts=('gtkprint-cups')
options=('!libtool')
backup=(etc/gtk-2.0/gtkrc)
license=('LGPL')
source=(http://ftp.gnome.org/pub/gnome/sources/gtk+/2.12/gtk+-${pkgver}.tar.bz2
	gtkclipboard-check.patch)
md5sums=('33499772fdc3bea569c6d5673e5831b4'
         '4025d3c15d6c6f73a032f403ffd4ff1c')

build() {
  cd ${startdir}/src/gtk+-${pkgver}
  # Workaround patch for flash
  patch -Np1 -i ${startdir}/src/gtkclipboard-check.patch || return 1

  ./configure --prefix=/usr --sysconfdir=/etc \
              --localstatedir=/var --with-xinput=xfree \
	      --with-included-loaders=png || return 1
  make || return 1
  make DESTDIR=${startdir}/pkg install || return 1

  echo 'gtk-fallback-icon-theme = "gnome"' > ${startdir}/pkg/etc/gtk-2.0/gtkrc || return 1
}
