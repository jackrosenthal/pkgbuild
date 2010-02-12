# Maintainer: Jan de Groot <jgc@archlinux.org>

pkgname=gtk2
pkgver=2.19.5
pkgrel=1
pkgdesc="The GTK+ Toolkit (v2)"
arch=(i686 x86_64)
url="http://www.gtk.org/"
install=gtk2.install
depends=('atk>=1.29.4' 'pango>=1.26.2' 'libxcursor' 'libxinerama' 'libxrandr>=1.3.0' 'libxi>=1.2.1' 'libxcomposite' 'libxdamage' 'heimdal>=1.3.1' 'gnutls>=2.8.3' 'shared-mime-info' 'cairo>=1.8.8-2' 'libtiff>=3.9.2-2' 'libcups>=1.4.2-3')
makedepends=('pkgconfig' 'gtk-doc')
replaces=('gtkprint-cups' 'gail')
conflicts=('gtkprint-cups' 'gail')
provides=('gail=1.22.3')
options=('!libtool' '!docs')
backup=(etc/gtk-2.0/gtkrc)
license=('LGPL')
source=(http://ftp.gnome.org/pub/gnome/sources/gtk+/2.19/gtk+-${pkgver}.tar.bz2
        xid-collision-debug.patch)
sha256sums=('dd90ea32cfce0337e91af9fef738e7cc6e894e8825287b6048068551e0749481'
            'd758bb93e59df15a4ea7732cf984d1c3c19dff67c94b957575efea132b8fe558')

build() {
  cd "${srcdir}/gtk+-${pkgver}"
  patch -Np1 -i "${srcdir}/xid-collision-debug.patch" || return 1

  CXX=/bin/false ./configure --prefix=/usr --sysconfdir=/etc \
      --localstatedir=/var --with-xinput=yes \
      --without-libjasper \
      --with-included-loaders=png || return 1
  make || return 1
  make DESTDIR="${pkgdir}" install || return 1

  echo 'gtk-fallback-icon-theme = "gnome"' > "${pkgdir}/etc/gtk-2.0/gtkrc" || return 1
}
