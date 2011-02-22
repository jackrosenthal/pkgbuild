# Maintainer: Jan de Groot <jgc@archlinux.org>

pkgbase=gtk2
pkgname=('gtk2' 'gtk-update-icon-cache')
pkgver=2.24.1
pkgrel=1
arch=('i686' 'x86_64')
url="http://www.gtk.org/"
makedepends=('atk' 'pango' 'libxcursor' 'libxinerama' 'libxrandr' 'libxi' 'libxcomposite' 'libxdamage' 'heimdal' 'gnutls'
             'shared-mime-info' 'cairo' 'libcups' 'gdk-pixbuf2' 'gobject-introspection' 'gtk-doc' 'namcap')
options=('!libtool' '!docs')
license=('LGPL')
source=(http://ftp.gnome.org/pub/gnome/sources/gtk+/2.24/gtk+-${pkgver}.tar.bz2
        xid-collision-debug.patch old-icon-symlinks.patch)
sha256sums=('0e2f94dfeb82ffb73640e17a411b9d62851dc4b2e147d90a24f94c1bfc0491ed'
            'd758bb93e59df15a4ea7732cf984d1c3c19dff67c94b957575efea132b8fe558'
            '1298e4103f71d0304378f1e7503011150f6f68398ae8ebae5522a48feaea7c0d')

build() {
    cd "${srcdir}/gtk+-${pkgver}"
    patch -Np1 -i "${srcdir}/xid-collision-debug.patch"
    patch -Np1 -i "${srcdir}/old-icon-symlinks.patch"

    CXX=/bin/false ./configure --prefix=/usr \
        --sysconfdir=/etc \
        --localstatedir=/var \
        --with-xinput=yes
    make
}
package_gtk2() {
    pkgdesc="The GTK+ Toolkit (v2)"
    install=gtk2.install
    depends=('atk' 'pango' 'libxcursor' 'libxinerama' 'libxrandr' 'libxi' 'libxcomposite' 'libxdamage' 'heimdal' 'gnutls' 'shared-mime-info' 'cairo' 'libcups' 'gtk-update-icon-cache')
    backup=(etc/gtk-2.0/gtkrc)

    cd "${srcdir}/gtk+-${pkgver}"

    make DESTDIR="${pkgdir}" install
    sed -i "s#env python#env python2#" $pkgdir/usr/bin/gtk-builder-convert
    echo 'gtk-fallback-icon-theme = "gnome"' > "${pkgdir}/etc/gtk-2.0/gtkrc"
    #split this out to use with gtk3 too
    rm ${pkgdir}/usr/bin/gtk-update-icon-cache
}
package_gtk-update-icon-cache() {
    pkgdesc="The GTK+ update icon cache tool"
    depends=('gdk-pixbuf2')

    cd "${srcdir}/gtk+-${pkgver}/gtk"

    install -D -m755 gtk-update-icon-cache ${pkgdir}/usr/bin/gtk-update-icon-cache
}
