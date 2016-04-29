# Maintainer: Jan de Groot <jgc@archlinux.org>

pkgname=gtk2
pkgver=2.24.30
pkgrel=2
pkgdesc="GObject-based multi-platform GUI toolkit (legacy)"
arch=(i686 x86_64)
url="http://www.gtk.org/"
depends=(atk pango libxcursor libxinerama libxrandr libxi libxcomposite libxdamage
         shared-mime-info cairo libcups gtk-update-icon-cache librsvg desktop-file-utils)
makedepends=(gobject-introspection python2)
optdepends=('gnome-themes-standard: Default widget theme'
            'adwaita-icon-theme: Default icon theme')
license=(LGPL)
install=gtk2.install
source=(https://download.gnome.org/sources/gtk+/2.24/gtk+-$pkgver.tar.xz
        gtkrc
        gtk-query-immodules-2.0.hook
        xid-collision-debug.patch)
sha256sums=('0d15cec3b6d55c60eac205b1f3ba81a1ed4eadd9d0f8e7c508bc7065d0c4ca50'
            'bc968e3e4f57e818430130338e5f85a5025e21d7e31a3293b8f5a0e58362b805'
            '9656a1efc798da1ac2dae94e921ed0f72719bd52d4d0138f305b993f778f7758'
            'd758bb93e59df15a4ea7732cf984d1c3c19dff67c94b957575efea132b8fe558')

prepare() {
    cd gtk+-$pkgver
    patch -Np1 -i ../xid-collision-debug.patch
    sed -i '1s/python$/&2/' gtk/gtk-builder-convert
}

build() {
    cd gtk+-$pkgver

    CXX=/bin/false ./configure --prefix=/usr \
        --sysconfdir=/etc \
        --localstatedir=/var \
        --with-xinput=yes

    # https://bugzilla.gnome.org/show_bug.cgi?id=655517
    sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0/g' libtool

    make
}

package() {
    cd gtk+-$pkgver
    make DESTDIR="$pkgdir" install

    install -Dm644 ../gtkrc "$pkgdir/usr/share/gtk-2.0/gtkrc"
    install -Dm644 ../gtk-query-immodules-2.0.hook "$pkgdir/usr/share/libalpm/hooks/gtk-query-immodules-2.0.hook"

    rm "$pkgdir/usr/bin/gtk-update-icon-cache"
    rm -r "$pkgdir/usr/share/gtk-doc"
}

# vim:set et sw=4:
