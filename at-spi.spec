%define lib_major	0
%define lib_name	%mklibname %{name} %{lib_major}
%define develname	%mklibname -d %{name}

Summary: GNOME Assistive Technology Service Provider Interface
Name: at-spi
Version: 1.20.0
Release: %mkrel 1
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
License: LGPL
Url: http://developer.gnome.org/projects/gap/
Group: Accessibility
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	gtk-doc >= 0.9
Buildrequires:	libbonobo2_x-devel >= 1.107.0
BuildRequires:  atk-devel >= 1.12.0
BuildRequires:	libgail-devel >= 1.3.0
BuildRequires:	python-devel
BuildRequires:  perl-XML-Parser
BuildRequires:	libxtst-devel
#gw work around libtool dependancy problem
BuildRequires:	libsm-devel

%description
This is the Early Access Release of the Gnome Accessibility Project's
Assistive Technology Service Provider Interface.

%package -n %{lib_name}
Summary:	GNOME Assistive Technology Service Provider Interface
Group:		%{group}

Provides:	lib%{name} = %{version}-%{release}
Requires:	%{name} >= %{version}-%{release}
Conflicts:	at-spi < 1.7.14-3mdv

%description -n %{lib_name}
This is the Early Access Release of the Gnome Accessibility Project's
Assistive Technology Service Provider Interface.

%package -n %develname
Summary:	Static libraries, include files for at-spi
Group:		Development/GNOME and GTK+
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Requires:	%{lib_name} = %{version}-%{release}
Requires:   libbonobo2_x-devel
Requires:   libgail-devel
Obsoletes: %mklibname -d %{name} 0

%description -n %develname
This is the Early Access Release of the Gnome Accessibility Project's
Assistive Technology Service Provider Interface.

%package -n python-%name
Group: Development/Python
Summary: Python bindings for AT-SPI
%description -n python-%name
This is the Early Access Release of the Gnome Accessibility Project's
Assistive Technology Service Provider Interface. 

Install this package to use AT-SPI from Python.


%prep
%setup -q

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

%post -n %{lib_name} -p /sbin/ldconfig
  
%postun -n %{lib_name} -p /sbin/ldconfig

%files -f %name.lang
%defattr(-,root,root)
%doc README AUTHORS TODO 
%{_datadir}/idl/*

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/*.so.%{lib_major}*
%{_libexecdir}/at-spi-registryd
%{_libdir}/gtk-2.0/modules/*.so
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
%py_platsitedir/pyatspi/
