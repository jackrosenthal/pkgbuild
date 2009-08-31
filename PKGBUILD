# Maintainer: Jan de Groot <jgc@archlinux.org>

pkgname=gtk2
pkgver=2.16.6
pkgrel=1
pkgdesc="The GTK+ Toolkit (v2)"
arch=(i686 x86_64)
url="http://www.gtk.org/"
install=gtk2.install
depends=('atk>=1.26.0' 'pango>=1.24.4' 'libxcursor' 'libxinerama' 'libxrandr>=1.3.0' 'libxi>=1.2.1' 'libcups>=1.3.10-3' 'libxcomposite' 'libxdamage' 'heimdal>=1.2.1' 'gnutls>=2.8.3' 'shared-mime-info')
makedepends=('pkgconfig')
replaces=('gtkprint-cups' 'gail')
conflicts=('gtkprint-cups' 'gail')
provides=('gail=1.22.3')
options=('!libtool' '!docs')
backup=(etc/gtk-2.0/gtkrc)
license=('LGPL')
source=(http://ftp.gnome.org/pub/gnome/sources/gtk+/2.16/gtk+-${pkgver}.tar.bz2
        libjpeg-7.patch)
sha256sums=('18e0f9792028e6cc5108447678f17d396f9a2cdfec1e6ab5dca98cb844f954af'
            '977ba13f3e2778cb82aadfd5e27fc4a8b715346e30e1cd1e6e76bec30079bf99')

build() {
  cd "${srcdir}/gtk+-${pkgver}"
  patch -Np1 -i "${srcdir}/libjpeg-7.patch" || return 1
  
  ./configure --prefix=/usr --sysconfdir=/etc \
      --localstatedir=/var --with-xinput=yes \
      --without-libjasper \
      --with-included-loaders=png || return 1
  make || return 1
  make DESTDIR="${pkgdir}" install || return 1

  echo 'gtk-fallback-icon-theme = "gnome"' > "${pkgdir}/etc/gtk-2.0/gtkrc" || return 1
}
