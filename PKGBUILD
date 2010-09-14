# Maintainer: Jan de Groot <jgc@archlinux.org>

pkgname=gtk2
pkgver=2.21.8
pkgrel=1
pkgdesc="The GTK+ Toolkit (v2)"
arch=('i686' 'x86_64')
url="http://www.gtk.org/"
install=gtk2.install
depends=('atk>=1.30.0' 'pango>=1.28.0' 'libxcursor' 'libxinerama' 'libxrandr>=1.3.0' 'libxi>=1.3' 'libxcomposite' 'libxdamage' 'heimdal>=1.3.2' 'gnutls>=2.8.6' 'shared-mime-info' 'cairo>=1.10.0' 'libcups>=1.4.4' 'gdk-pixbuf2>=2.21.7')
makedepends=('pkgconfig' 'gtk-doc' 'gobject-introspection')
replaces=('gtkprint-cups' 'gail')
conflicts=('gtkprint-cups' 'gail')
provides=('gail=1.22.3')
options=('!libtool' '!docs')
backup=(etc/gtk-2.0/gtkrc)
license=('LGPL')
source=(http://ftp.gnome.org/pub/gnome/sources/gtk+/2.21/gtk+-${pkgver}.tar.bz2
        xid-collision-debug.patch)
sha256sums=('f17ce48b3a896dc35bf70f22a18c868d06fca526f024396473e227ea30c32cc8'
            'd758bb93e59df15a4ea7732cf984d1c3c19dff67c94b957575efea132b8fe558')

build() {
  cd "${srcdir}/gtk+-${pkgver}"
  patch -Np1 -i "${srcdir}/xid-collision-debug.patch"

  CXX=/bin/false ./configure --prefix=/usr \
      --sysconfdir=/etc \
      --localstatedir=/var \
      --with-xinput=yes
  make
  make DESTDIR="${pkgdir}" install

  echo 'gtk-fallback-icon-theme = "gnome"' > "${pkgdir}/etc/gtk-2.0/gtkrc"
}
