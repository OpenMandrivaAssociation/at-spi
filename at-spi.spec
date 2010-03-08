%define lib_major	0
%define lib_name	%mklibname %{name} %{lib_major}
%define develname	%mklibname -d %{name}

Summary: Assistive Technology Service Provider Interface
Name: at-spi
Version: 1.29.92
Release: %mkrel 1
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
# Fix a string literal error - AdamW 2008/12
Patch0: at-spi-1.25.2-literal.patch
#gw: asked for by guillomovitch on IRC. We enable this (the old CORBA based
# AT-SPI intrastructure) for now. Remove once DBUS infrastructure is done
Patch1: at-spi-1.29.90-enable-corba-at-spi.patch
License: LGPLv2+
Url: http://developer.gnome.org/projects/gap/
Group: Accessibility
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	gtk-doc >= 0.9
Buildrequires:	libbonobo2_x-devel >= 1.107.0
BuildRequires:  atk-devel >= 1.19.2
BuildRequires:	libgail-devel >= 1.3.0
BuildRequires:	libGConf2-devel
BuildRequires:	python-devel
BuildRequires:  intltool
BuildRequires:	libxtst-devel
BuildRequires:  libxevie-devel
#gw work around libtool dependancy problem
BuildRequires:	libsm-devel

%description
at-spi allows assistive technologies to access GTK-based
applications. Essentially it exposes the internals of applications for
automation, so tools such as screen readers, magnifiers, or even
scripting interfaces can query and interact with GUI controls.

%package -n %{lib_name}
Summary:	GNOME Assistive Technology Service Provider Interface
Group:		System/Libraries

Provides:	lib%{name} = %{version}-%{release}
Requires:	%{name} >= %{version}-%{release}
Conflicts:	at-spi < 1.7.14-3mdv

%description -n %{lib_name}
at-spi allows assistive technologies to access GTK-based
applications. Essentially it exposes the internals of applications for
automation, so tools such as screen readers, magnifiers, or even
scripting interfaces can query and interact with GUI controls.

%package -n %develname
Summary:	Static libraries, include files for at-spi
Group:		Development/GNOME and GTK+
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Requires:	%{lib_name} = %{version}-%{release}
Requires:   libbonobo2_x-devel
Requires:   libgail-devel
Requires:   libxtst-devel
Obsoletes: %mklibname -d %{name} 0

%description -n %develname
Libraries and header files allowing compilation of apps that use at-spi.

%package -n python-%name
Group: Development/Python
Summary: Python bindings for AT-SPI
Requires: %{lib_name} >= %{version}

%description -n python-%name
Python bindings allowing to use at-spi in python programs.

%prep
%setup -q
%patch0 -p1 -b .literal
%patch1 -p1

%build

%configure2_5x --enable-gtk-doc=yes

%make

%install
rm -rf $RPM_BUILD_ROOT installed-docs

%makeinstall_std

# remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/*.la \
  $RPM_BUILD_ROOT%{_libdir}/orbit-2.0/*.la

%find_lang %name

mv %buildroot%_datadir/doc/%name-%version/ installed-docs

%clean
rm -rf $RPM_BUILD_ROOT

%post
%post_install_gconf_schemas at-spi
%preun
%preun_uninstall_gconf_schemas at-spi

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif
  
%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%files -f %name.lang
%defattr(-,root,root)
%doc README AUTHORS TODO 
%config(noreplace) %_sysconfdir/xdg/autostart/at-spi-registryd.desktop
%{_datadir}/idl/*
%_sysconfdir/gconf/schemas/at-spi.schemas

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/*.so.%{lib_major}*
%{_libexecdir}/at-spi-registryd
%{_libdir}/gtk-2.0/modules/libatk-bridge.so
%{_libdir}/orbit-2.0/*.so
%{_libdir}/bonobo/servers/*

%files -n %develname
%defattr(-,root,root)
%doc %{_datadir}/gtk-doc/html/* 
%doc installed-docs/*
%{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/*
%{_libdir}/pkgconfig/*

%files -n python-%{name}
%defattr(-,root,root)
%py_platsitedir/pyatspi
