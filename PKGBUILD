# Maintainer: Jan de Groot <jgc@archlinux.org>

pkgbase=gtk2
pkgname=('gtk2' 'gtk-update-icon-cache')
pkgver=2.24.9
pkgrel=3
arch=('i686' 'x86_64')
url="http://www.gtk.org/"
makedepends=('atk' 'pango' 'libxcursor' 'libxinerama' 'libxrandr' 'libxi' 'libxcomposite' 'libxdamage'
             'shared-mime-info' 'cairo' 'libcups' 'gdk-pixbuf2' 'gobject-introspection')
options=('!libtool' '!docs')
license=('LGPL')
source=(http://ftp.gnome.org/pub/gnome/sources/gtk+/2.24/gtk+-$pkgver.tar.xz
        xid-collision-debug.patch cups-custom-print.patch)
sha256sums=('84204bf24cac739fd979943127e7b29cb46b1017684aa24dce630faa01bcb61d'
            'd758bb93e59df15a4ea7732cf984d1c3c19dff67c94b957575efea132b8fe558'
            '9535c9df19338cbea98ec4b2b5c8e4cef718455938f05c9cf8a08a3805d6b85d')

build() {
    cd "$srcdir/gtk+-$pkgver"
    patch -Np1 -i "$srcdir/xid-collision-debug.patch"

    # https://bugzilla.gnome.org/show_bug.cgi?id=543520
    patch -Rp1 -i "$srcdir/cups-custom-print.patch"

    CXX=/bin/false ./configure --prefix=/usr \
        --sysconfdir=/etc \
        --localstatedir=/var \
        --with-xinput=yes

    # https://bugzilla.gnome.org/show_bug.cgi?id=655517
    sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0/g' libtool

    make
}

package_gtk2() {
    pkgdesc="GTK+ is a multi-platform toolkit (v2)"
    install=gtk2.install
    depends=('atk' 'pango' 'libxcursor' 'libxinerama' 'libxrandr' 'libxi' 'libxcomposite' 'libxdamage' 'shared-mime-info' 'cairo' 'libcups' 'gtk-update-icon-cache')
    backup=(etc/gtk-2.0/gtkrc)

    cd "$srcdir/gtk+-$pkgver"

    make DESTDIR="$pkgdir" install
    sed -i "s#env python#env python2#" $pkgdir/usr/bin/gtk-builder-convert
    echo 'gtk-fallback-icon-theme = "gnome"' > "$pkgdir/etc/gtk-2.0/gtkrc"
    #split this out to use with gtk3 too
    rm $pkgdir/usr/bin/gtk-update-icon-cache
}
package_gtk-update-icon-cache() {
    pkgdesc="The GTK+ update icon cache tool"
    depends=('gdk-pixbuf2>=2.24.1-3')

    cd "$srcdir/gtk+-$pkgver/gtk"

    install -D -m755 gtk-update-icon-cache $pkgdir/usr/bin/gtk-update-icon-cache
}
