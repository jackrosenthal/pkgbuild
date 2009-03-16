# Maintainer: Jan de Groot <jgc@archlinux.org>

pkgname=gtk2
pkgver=2.16.0
pkgrel=1
pkgdesc="The GTK+ Toolkit (v2)"
arch=(i686 x86_64)
url="http://www.gtk.org/"
install=gtk2.install
depends=('atk>=1.26.0' 'pango>=1.23.0' 'libxcursor' 'libxinerama' 'libxrandr>=1.3.0' 'libxi>=1.2.1' 'libcups>=1.3.9' 'libxcomposite' 'libxdamage' 'heimdal>=1.2.1' 'gnutls>=2.6.4' 'shared-mime-info')
makedepends=('pkgconfig')
replaces=('gtkprint-cups' 'gail')
conflicts=('gtkprint-cups' 'gail')
provides=('gail=1.22.3')
options=('!libtool' '!docs')
backup=(etc/gtk-2.0/gtkrc)
license=('LGPL')
source=(http://ftp.gnome.org/pub/gnome/sources/gtk+/2.16/gtk+-${pkgver}.tar.bz2
	gtkclipboard-check.patch)
md5sums=('139528802794287427fd4d18875b5cf5'
         '4025d3c15d6c6f73a032f403ffd4ff1c')

build() {
  cd "${srcdir}/gtk+-${pkgver}"
  # Workaround patch for flash
  patch -Np1 -i "${srcdir}/gtkclipboard-check.patch" || return 1

  ./configure --prefix=/usr --sysconfdir=/etc \
              --localstatedir=/var --with-xinput=yes \
	      --without-libjasper \
	      --with-included-loaders=png || return 1
  make || return 1
  make DESTDIR="${pkgdir}" install || return 1

  echo 'gtk-fallback-icon-theme = "gnome"' > "${pkgdir}/etc/gtk-2.0/gtkrc" || return 1
}
