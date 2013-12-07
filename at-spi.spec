%define url_ver %(echo %{version}|cut -d. -f1,2)

%define	major	0
%define	libspi	%mklibname spi %{major}
%define	libcspi	%mklibname cspi %{major}
%define	liblog	%mklibname loginhelper %{major}
%define	devname	%mklibname -d %{name}

Summary:	Assistive Technology Service Provider Interface
Name:		at-spi
Version:	1.32.0
Release:	10
License:	LGPLv2+
Group:		Accessibility
Url:		http://developer.gnome.org/projects/gap/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/at-spi/%{url_ver}/%{name}-%{version}.tar.bz2
# Fix a string literal error - AdamW 2008/12
Patch0:		at-spi-1.25.2-literal.patch
Patch1:		at-spi-fix-evolution-crash.patch

BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	pkgconfig(atk) >= 1.19.2
BuildRequires:	pkgconfig(bonobo-activation-2.0)
BuildRequires:	pkgconfig(libbonobo-2.0)
BuildRequires:	pkgconfig(gail) >= 1.3.0
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(popt)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	pkgconfig(xevie)

%description
at-spi allows assistive technologies to access GTK-based
applications. Essentially it exposes the internals of applications for
automation, so tools such as screen readers, magnifiers, or even
scripting interfaces can query and interact with GUI controls.

%package -n %{libspi}
Summary:	GNOME Assistive Technology Service Provider Interface
Group:		System/Libraries
Obsoletes:	%{_lib}at-spi0

%description -n %{libspi}
This package contains a shared library for %{name}.

%package -n %{libcspi}
Summary:	GNOME Assistive Technology Service Provider Interface
Group:		System/Libraries
Conflicts:	%{_lib}at-spi0

%description -n %{libcspi}
This package contains a shared library for %{name}.

%package -n %{liblog}
Summary:	GNOME Assistive Technology Service Provider Interface
Group:		System/Libraries
Conflicts:	%{_lib}at-spi0

%description -n %{liblog}
This package contains a shared library for %{name}.

%package -n %{devname}
Summary:	Development libraries, include files for at-spi
Group:		Development/GNOME and GTK+
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libspi} >= %{version}
Requires:	%{libcspi} >= %{version}
Requires:	%{liblog} >= %{version}

%description -n %{devname}
Libraries and header files allowing compilation of apps that use at-spi.

%package -n python-%{name}
Group:		Development/Python
Summary:	Python bindings for AT-SPI
Requires:	%{libspi} >= %{version}
Requires:	%{libcspi} >= %{version}
Requires:	%{liblog} >= %{version}

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
%makeinstall_std

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

%files -n %{libspi}
%{_libdir}/libspi.so.%{major}*

%files -n %{libcspi}
%{_libdir}/libcspi.so.%{major}*

%files -n %{liblog}
%{_libdir}/libloginhelper.so.%{major}*

%files -n %{devname}
%doc %{_datadir}/gtk-doc/html/*
%doc installed-docs/*
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_datadir}/idl/*

%files -n python-%{name}
%{py_platsitedir}/pyatspi_corba

