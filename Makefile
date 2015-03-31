SRCDIR=`pwd`

all: org.gnome.Builder org.gnome.gedit org.freedesktop.glxgears

repo:
	ostree  init --mode=archive-z2 --repo=repo

gnome-builder:
	git clone git://git.gnome.org/gnome-builder


org.gnome.Builder: repo gnome-builder
	gnome-sdk-bundles/install-rpms gnome-builder.appbuild org.gnome.Sdk org.gnome.Sdk 3.16 libgit2-glib-dev gtksourceview3-dev devhelp-dev
	mkdir -p gnome-builder.appbuild/files/dest

	gnome-sdk-bundles/install-rpms gnome-builder.app org.gnome.Sdk org.gnome.Sdk 3.16 libgit2-glib devhelp-libs gtksourceview3
	ln -s `pwd`/gnome-builder.app/files gnome-builder.appbuild/files/dest/self

	cd gnome-builder && \
	xdg-app build ../gnome-builder.appbuild ./autogen.sh --prefix=/self && \
	xdg-app build ../gnome-builder.appbuild make && \
	xdg-app build ../gnome-builder.appbuild make install DESTDIR=/self/dest

	rm -rf gnome-builder.appbuild

# We need to make the app icon have the right prefix so it can be exported
	sed -i s/Icon=builder/Icon=org.gnome.Builder/ gnome-builder.app/files/share/applications/org.gnome.Builder.desktop
	for i in gnome-builder.app/files/share/icons/hicolor/*/apps/builder.png; do mv $$i `dirname $$i`/org.gnome.Builder.png; done

# Turns out builder really depends on the gedit schema...
	cp org.gnome.gedit.gschema.xml gnome-builder.app/files/share//glib-2.0/schemas

# Run various triggers
	xdg-app build gnome-builder.app glib-compile-schemas /self/share/glib-2.0/schemas
	xdg-app build gnome-builder.app strip /self/bin/gnome-builder

	xdg-app build-finish --allow=ipc --allow=network --allow=x11 --allow=x11 --allow=wayland --allow=session-dbus --allow=host-fs gnome-builder.app

# A bunch of non-prefixed files should not be exported (build-finish should handle this!)
	rm gnome-builder.app/export/share/icons/hicolor/scalable/*/*.svg

	xdg-app build-export repo gnome-builder.app org.gnome.Builder
	rm -rf gnome-builder.app

SOURCES/gedit-3.16.0.tar.xz:
	wget -P SOURCES http://download.gnome.org/sources/gedit/3.16/gedit-3.16.0.tar.xz


RPMS/x86_64/gedit-3.16.0-1.sdk.x86_64.rpm: SOURCES/gedit-3.16.0.tar.xz
	gnome-sdk-bundles/install-rpms gedit.appbuild org.gnome.Sdk org.gnome.Platform 3.16 libpeas-dev gtksourceview3-dev
	xdg-app build gedit.appbuild rpmbuild --define "_topdir ${SRCDIR}" --clean -bb gedit.spec
	rm -rf gedit.appbuild

org.gnome.gedit: repo gedit.spec RPMS/x86_64/gedit-3.16.0-1.sdk.x86_64.rpm
	gnome-sdk-bundles/install-rpms gedit.app org.gnome.Sdk org.gnome.Platform 3.16 libpeas gtksourceview3
	xdg-app build gedit.app rpm -Uvh RPMS/x86_64/gedit-3.16.0-1.sdk.x86_64.rpm

	xdg-app build-finish --allow=ipc --allow=network --allow=x11 --allow=x11 --allow=wayland --allow=session-dbus --allow=host-fs gedit.app

# A bunch of non-prefixed files should not be exported (build-finish should handle this!)
	rm gedit.app/export/share/icons/hicolor/*/actions/libpeas-plugin.png gedit.app/export/share/icons/hicolor/scalable/actions/libpeas-plugin.svg

	xdg-app build-export repo gedit.app org.gnome.gedit
	rm -rf gedit.app

SOURCES/mesa-demos-8.2.0.tar.bz2:
	wget -P SOURCES ftp://ftp.freedesktop.org/pub/mesa/demos/8.2.0/mesa-demos-8.2.0.tar.bz2

RPMS/x86_64/mesa-demos-8.2.0-1.sdk.x86_64.rpm: SOURCES/mesa-demos-8.2.0.tar.bz2
	gnome-sdk-bundles/install-rpms mesa-demos.appbuild org.freedesktop.Sdk org.freedesktop.Platform 1.0 freeglut-dev libGLU-dev glew-dev
	xdg-app build mesa-demos.appbuild rpmbuild --define "_topdir ${SRCDIR}" --clean -bb mesa-demos.spec
	rm -rf mesa-demos.appbuild

org.freedesktop.glxgears: repo mesa-demos.spec RPMS/x86_64/mesa-demos-8.2.0-1.sdk.x86_64.rpm
	gnome-sdk-bundles/install-rpms glxgears.app org.freedesktop.Sdk org.freedesktop.Platform 1.0 libGLU libGLEW freeglut
	xdg-app build glxgears.app rpm -Uvh RPMS/x86_64/glx-utils-8.2.0-1.sdk.x86_64.rpm

	xdg-app build-finish --allow=ipc --allow=x11 --allow=x11 --allow=wayland --allow=dri glxgears.app

	xdg-app build-export repo glxgears.app org.freedesktop.glxgears
	rm -rf glxgears.app
