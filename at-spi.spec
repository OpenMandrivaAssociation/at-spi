%define	lib_major	0
%define	lib_name	%mklibname %{name} %{lib_major}
%define	develname	%mklibname -d %{name}

Summary:	Assistive Technology Service Provider Interface
Name:		at-spi
Version:	1.32.0
Release:	6
License:	LGPLv2+
URL:		http://developer.gnome.org/projects/gap/
Group:		Accessibility
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
# Fix a string literal error - AdamW 2008/12
Patch0:		at-spi-1.25.2-literal.patch
Patch1:		at-spi-fix-evolution-crash.patch

BuildRequires:	gtk-doc >= 0.9
BuildRequires:	intltool
BuildRequires:	pkgconfig(atk) >= 1.19.2
BuildRequires:	pkgconfig(bonobo-activation-2.0)
BuildRequires:	pkgconfig(libbonobo-2.0)
BuildRequires:	pkgconfig(gail) >= 1.3.0
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(popt)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	pkgconfig(xevie)
#gw work around libtool dependancy problem
BuildRequires:	pkgconfig(sm)
BuildRequires:	python-devel

# md this is better than having the lib req the main pkg
Requires:	%{lib_name} = %{version}-%{release}

%description
at-spi allows assistive technologies to access GTK-based
applications. Essentially it exposes the internals of applications for
automation, so tools such as screen readers, magnifiers, or even
scripting interfaces can query and interact with GUI controls.

%package -n %{lib_name}
Summary:	GNOME Assistive Technology Service Provider Interface
Group:		System/Libraries
Provides:	lib%{name} = %{version}-%{release}

%description -n %{lib_name}
at-spi allows assistive technologies to access GTK-based
applications. Essentially it exposes the internals of applications for
automation, so tools such as screen readers, magnifiers, or even
scripting interfaces can query and interact with GUI controls.

%package -n %{develname}
Summary:	Development libraries, include files for at-spi
Group:		Development/GNOME and GTK+
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{lib_name} = %{version}-%{release}

%description -n %{develname}
Libraries and header files allowing compilation of apps that use at-spi.

%package -n python-%{name}
Group:		Development/Python
Summary:	Python bindings for AT-SPI
Requires:	%{lib_name} >= %{version}
Conflicts:	python-pyatspi <= 0.3.90

%description -n python-%{name}
Python bindings allowing to use at-spi in python programs.

%prep
%setup -q
%apply_patches

%build
%configure2_5x \
	--enable-gtk-doc=yes \
	--disable-static \
	--enable-relocate

%make

%install
rm -rf %{buildroot} installed-docs

%makeinstall_std

# remove unpackaged files
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%find_lang %{name}

mv %{buildroot}%{_datadir}/doc/%{name}-%{version}/ installed-docs

%preun
%preun_uninstall_gconf_schemas %{name}

%files -f %{name}.lang
%doc README AUTHORS TODO 
%config(noreplace) %{_sysconfdir}/xdg/autostart/at-spi-registryd.desktop
%{_sysconfdir}/gconf/schemas/at-spi.schemas
%{_libexecdir}/at-spi-registryd
%{_libdir}/gtk-2.0/modules/at-spi-corba
%{_libdir}/orbit-2.0/*.so
%{_libdir}/bonobo/servers/*

%files -n %{lib_name}
%{_libdir}/*.so.%{lib_major}*

%files -n %{develname}
%doc %{_datadir}/gtk-doc/html/* 
%doc installed-docs/*
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_datadir}/idl/*

%files -n python-%{name}
%{py_platsitedir}/pyatspi_corba

