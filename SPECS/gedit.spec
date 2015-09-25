Summary:	Text editor for the GNOME desktop
Name:		gedit
Version:	3.18.0
Release:	1%{?dist}
License:	GPLv2+ and GFDL
Group:		Applications/Editors
#VCS: git:git://git.gnome.org/gedit
Source0:	http://download.gnome.org/sources/gedit/3.18/gedit-%{version}.tar.xz

URL:		http://projects.gnome.org/gedit/

Requires(post):         desktop-file-utils >= %{desktop_file_utils_version}
Requires(postun):       desktop-file-utils >= %{desktop_file_utils_version}

BuildRequires: gtksourceview3-dev
BuildRequires: libpeas-dev
Requires: gtksourceview3
Requires: libpeas

%description
gedit is a small, but powerful text editor designed specifically for
the GNOME desktop. It has most standard text editor functions and fully
supports international text in Unicode. Advanced features include syntax
highlighting and automatic indentation of source code, printing and editing
of multiple documents in one window.

gedit is extensible through a plugin system, which currently includes
support for spell checking, comparing files, viewing CVS ChangeLogs, and
adjusting indentation levels. Further plugins can be found in the
gedit-plugins package.

%package devel
Summary: Support for developing plugins for the gedit text editor
Group: Development/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}

%description devel
gedit is a small, but powerful text editor for the GNOME desktop.
This package allows you to develop plugins that add new functionality
to gedit.

Install gedit-devel if you want to write plugins for gedit.

%prep
%setup -q

autoreconf -i -f
intltoolize -f

%build
%configure \
	--disable-gtk-doc \
	--enable-introspection=yes \
	--enable-python=yes \
	--disable-updater \
	--enable-gvfs-metadata
make %{_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT

## clean up all the static libs for plugins (workaround for no -module)
/bin/rm -f `find $RPM_BUILD_ROOT%{_libdir} -name "*.a"`
/bin/rm -f `find $RPM_BUILD_ROOT%{_libdir} -name "*.la"`

%find_lang %{name} --with-gnome

%check
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/org.gnome.gedit.desktop

%post
touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :

%postun
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas >&/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas >&/dev/null || :

%files -f %{name}.lang
%doc README COPYING AUTHORS
%{_datadir}/gedit
%{_datadir}/applications/org.gnome.gedit.desktop
%{_mandir}/man1/*
%{_libexecdir}/gedit
%{_libdir}/gedit/girepository-1.0
%{_libdir}/python3.3/site-packages/gi/overrides/Gedit.py
%dir %{_libdir}/gedit
%dir %{_libdir}/gedit/plugins
%{_libdir}/gedit/libgedit.so
%{_libdir}/gedit/plugins/docinfo.plugin
%{_libdir}/gedit/plugins/libdocinfo.so
%{_libdir}/gedit/plugins/filebrowser.plugin
%{_libdir}/gedit/plugins/libfilebrowser.so
%{_libdir}/gedit/plugins/modelines.plugin
%{_libdir}/gedit/plugins/libmodelines.so
%{_libdir}/gedit/plugins/externaltools.plugin
%{_libdir}/gedit/plugins/externaltools
%{_libdir}/gedit/plugins/pythonconsole.plugin
%{_libdir}/gedit/plugins/pythonconsole
%{_libdir}/gedit/plugins/quickopen.plugin
%{_libdir}/gedit/plugins/quickopen
%{_libdir}/gedit/plugins/snippets.plugin
%{_libdir}/gedit/plugins/snippets
%{_libdir}/gedit/plugins/sort.plugin
%{_libdir}/gedit/plugins/libsort.so
%{_libdir}/gedit/plugins/spell.plugin
%{_libdir}/gedit/plugins/libspell.so
%{_libdir}/gedit/plugins/time.plugin
%{_libdir}/gedit/plugins/libtime.so
%{_bindir}/*
%{_datadir}/appdata/org.gnome.gedit.appdata.xml
%{_datadir}/GConf/gsettings
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.externaltools.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.pythonconsole.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.filebrowser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.filebrowser.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.time.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.time.enums.xml
%{_datadir}/dbus-1/services/org.gnome.gedit.service


%files devel
%{_includedir}/gedit-3.14
%{_libdir}/pkgconfig/gedit.pc
%{_datadir}/gtk-doc
%{_datadir}/vala/

%changelog
* Mon Mar 30 2015 Alexander Larsson <alexl@redhat.com> - 3.16.0-1
- Initial
