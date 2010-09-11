# Maintainer: Jan de Groot <jgc@archlinux.org>

pkgname=gtk2
pkgver=2.21.7
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
        xid-collision-debug.patch
        gobject-introspection-0.9.5.patch
        display_struct_duplicate_fix1.patch
        display_struct_duplicate_fix2.patch)
sha256sums=('d55fdc6638d2b9df3867346da0afe142475fe8a1d9b6ef3910dacedb8af427d2'
            'd758bb93e59df15a4ea7732cf984d1c3c19dff67c94b957575efea132b8fe558'
            'e9acf1b02cc3f04135bb524e2a66568373ee899cc5d6887a5668de2d813447d4'
            '6ec6d16a2e7ecbe356941e5b5f54197757afc873f29a56796760de15356fa327'
            '22bba430e309cc2f14efaf1ceebf443a463f4f333625a1fae3424195a8acc522')

build() {
  cd "${srcdir}/gtk+-${pkgver}"
  patch -Np1 -i "${srcdir}/xid-collision-debug.patch"
  patch -Np1 -i "${srcdir}/gobject-introspection-0.9.5.patch"
  patch -Np1 -i "${srcdir}/display_struct_duplicate_fix1.patch"
  patch -Np1 -i "${srcdir}/display_struct_duplicate_fix2.patch"

  autoreconf -fi

  CXX=/bin/false ./configure --prefix=/usr \
      --sysconfdir=/etc \
      --localstatedir=/var \
      --with-xinput=yes
  make
  make DESTDIR="${pkgdir}" install

  echo 'gtk-fallback-icon-theme = "gnome"' > "${pkgdir}/etc/gtk-2.0/gtkrc"
}
