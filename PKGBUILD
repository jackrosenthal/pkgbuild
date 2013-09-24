# Maintainer: Jan de Groot <jgc@archlinux.org>

pkgbase=gtk2
pkgname=('gtk2' 'gtk-update-icon-cache')
pkgver=2.24.21
pkgrel=1
arch=('i686' 'x86_64')
url="http://www.gtk.org/"
makedepends=('atk' 'pango' 'libxcursor' 'libxinerama' 'libxrandr' 'libxi' 'libxcomposite' 'libxdamage'
             'shared-mime-info' 'cairo' 'libcups' 'gdk-pixbuf2' 'gobject-introspection')
options=('!libtool')
license=('LGPL')
source=(http://ftp.gnome.org/pub/gnome/sources/gtk+/2.24/gtk+-$pkgver.tar.xz
        xid-collision-debug.patch)
sha256sums=('302e9216dd19ec4b5b9e2f77275e23758253f7e86b06287284d8e794ef38dce3'
            'd758bb93e59df15a4ea7732cf984d1c3c19dff67c94b957575efea132b8fe558')

build() {
    cd gtk+-$pkgver
    patch -Np1 -i ../xid-collision-debug.patch

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
    replaces=('gtk2-docs')

    cd gtk+-$pkgver

    make DESTDIR="$pkgdir" install
    sed -i "s#env python#env python2#" $pkgdir/usr/bin/gtk-builder-convert
    mkdir -p "$pkgdir/usr/share/gtk-2.0"
    echo 'gtk-fallback-icon-theme = "gnome"' > "$pkgdir/usr/share/gtk-2.0/gtkrc"
    #split this out to use with gtk3 too
    rm $pkgdir/usr/bin/gtk-update-icon-cache
}
package_gtk-update-icon-cache() {
    pkgdesc="The GTK+ update icon cache tool"
    depends=('gdk-pixbuf2>=2.24.1-3' 'hicolor-icon-theme')
    install=gtk-update-icon-cache.install

    cd gtk+-$pkgver/gtk

    install -D -m755 gtk-update-icon-cache $pkgdir/usr/bin/gtk-update-icon-cache
}
