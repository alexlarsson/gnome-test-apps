Summary: Mesa demos
Name: mesa-demos
Version: 8.2.0
Release: 1%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.mesa3d.org
Source0: ftp://ftp.freedesktop.org/pub/mesa/demos/8.2.0/%{name}-%{version}.tar.bz2

BuildRequires: freeglut-dev
BuildRequires: libGLU-dev
BuildRequires: glew-dev
Group: Development/Libraries

%description
This package provides some demo applications for testing Mesa.

%package -n glx-utils
Summary: GLX utilities
Group: Development/Libraries

%description -n glx-utils
The glx-utils package provides the glxinfo and glxgears utilities.

%prep
%setup -q -n %{name}-%{version} 

%build
autoreconf -i
%configure --bindir=%{_libdir}/mesa --with-system-data-files
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_bindir}
make install DESTDIR=%{buildroot}

install -m 0755 src/xdemos/glxgears %{buildroot}%{_bindir}
install -m 0755 src/xdemos/glxinfo %{buildroot}%{_bindir}

%check

%files
%{_libdir}/mesa
%{_datadir}/%{name}/

%files -n glx-utils
%{_bindir}/glxinfo
%{_bindir}/glxgears

%changelog
* Mon Mar 30 2015 Alexander Larsson <alexl@redhat.com> - 8.2.0-1
- Initial
