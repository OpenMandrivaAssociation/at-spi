%define	lib_major	0
%define	lib_name	%mklibname %{name} %{lib_major}
%define	develname	%mklibname -d %{name}

Summary:	Assistive Technology Service Provider Interface
Name:		at-spi
Version:	1.32.0
Release:	8
License:	LGPLv2+
URL:		http://developer.gnome.org/projects/gap/
Group:		Accessibility
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
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



%changelog
* Tue Nov 15 2011 Matthew Dawkins <mattydaw@mandriva.org> 1.32.0-6
+ Revision: 730784
- rebuild for dropped .la files
  removed unneeded virtual provide
  removed old obsoletes & conflicts
  removed unneeded BR
  converted libbonobo BR to pkgconfig provides

* Thu Nov 10 2011 Matthew Dawkins <mattydaw@mandriva.org> 1.32.0-5
+ Revision: 729910
- fixed dir for python files
- typo fix for macro
- removed old patch
- rebuild
  cleaned up spec
  removed mkrel macro
  remove gconf post; not needed due to trigger
  switch to dbus instead of corba, dropping p1
  remove .la files
  dropped static build
  changed BRs to pkgconfig provides
  dropped bogus req for main pkg by lib
  drooped unneccesary requires for devel pkgs
  converted RPM_BUILD_ROOT buildroot
  dropped obsolete scriptlets
  dropped defattr
  moved pluggin libs to main pkg
  moved schemas file to main pkg
  moved bonobo server to main pkg
  moved at-spi-registryd executable with desktop file in main pkg
  moved idl datadir files to devel (fedora)
  add patch from fedora to avoid evolution crash

* Sun May 22 2011 Funda Wang <fwang@mandriva.org> 1.32.0-4
+ Revision: 677053
- rebuild to add gconf2 as req

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.32.0-3
+ Revision: 662884
- mass rebuild

* Thu Nov 04 2010 Götz Waschk <waschk@mandriva.org> 1.32.0-2mdv2011.0
+ Revision: 593330
- rebuild for new python 2.7

* Mon Sep 27 2010 Götz Waschk <waschk@mandriva.org> 1.32.0-1mdv2011.0
+ Revision: 581235
- update to new version 1.32.0

* Mon Aug 30 2010 Götz Waschk <waschk@mandriva.org> 1.31.91-1mdv2011.0
+ Revision: 574306
- new  version
- drop patch 3
- update file list
- add a conflict with dbus-based python module

* Mon Aug 02 2010 Götz Waschk <waschk@mandriva.org> 1.31.1-1mdv2011.0
+ Revision: 565072
- update build deps
- fix makefile
- new version
- update file list
- rename python module again

* Tue Apr 27 2010 Christophe Fergeau <cfergeau@mandriva.com> 1.30.1-2mdv2010.1
+ Revision: 539611
- rebuild so that shared libraries are properly stripped again

* Mon Apr 26 2010 Götz Waschk <waschk@mandriva.org> 1.30.1-1mdv2010.1
+ Revision: 538844
- update to new version 1.30.1

* Tue Mar 30 2010 Götz Waschk <waschk@mandriva.org> 1.30.0-1mdv2010.1
+ Revision: 528956
- update to new version 1.30.0

* Mon Mar 08 2010 Götz Waschk <waschk@mandriva.org> 1.29.92-1mdv2010.1
+ Revision: 515805
- update build deps
- update to new version 1.29.92

* Tue Feb 09 2010 Götz Waschk <waschk@mandriva.org> 1.29.90-1mdv2010.1
+ Revision: 502697
- new version
- rediff patch 1
- update file list

* Mon Jan 25 2010 Götz Waschk <waschk@mandriva.org> 1.29.6-1mdv2010.1
+ Revision: 495972
- update to new version 1.29.6

* Mon Jan 11 2010 Götz Waschk <waschk@mandriva.org> 1.29.5-1mdv2010.1
+ Revision: 489600
- new version
- update file list

* Sat Jan 09 2010 Götz Waschk <waschk@mandriva.org> 1.29.3-2mdv2010.1
+ Revision: 488017
- enable corba AT-SPI by default

* Wed Dec 09 2009 Götz Waschk <waschk@mandriva.org> 1.29.3-1mdv2010.1
+ Revision: 475517
- new version
- bump atk dep
- update file list

* Wed Oct 21 2009 Frederic Crozat <fcrozat@mandriva.com> 1.28.1-1mdv2010.0
+ Revision: 458603
- Release 1.28.1

* Tue Sep 22 2009 Götz Waschk <waschk@mandriva.org> 1.28.0-1mdv2010.0
+ Revision: 447180
- update to new version 1.28.0

* Mon Sep 07 2009 Götz Waschk <waschk@mandriva.org> 1.27.92-1mdv2010.0
+ Revision: 432541
- update to new version 1.27.92

* Mon Aug 24 2009 Götz Waschk <waschk@mandriva.org> 1.27.91-1mdv2010.0
+ Revision: 420302
- new version
- update file list

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 1.26.0-2mdv2010.0
+ Revision: 413118
- rebuild

* Mon Mar 16 2009 Götz Waschk <waschk@mandriva.org> 1.26.0-1mdv2009.1
+ Revision: 355838
- update to new version 1.26.0

* Mon Mar 02 2009 Götz Waschk <waschk@mandriva.org> 1.25.92-1mdv2009.1
+ Revision: 347360
- update to new version 1.25.92

* Mon Jan 19 2009 Götz Waschk <waschk@mandriva.org> 1.25.5-1mdv2009.1
+ Revision: 331102
- update to new version 1.25.5

* Tue Jan 06 2009 Götz Waschk <waschk@mandriva.org> 1.25.4-1mdv2009.1
+ Revision: 325240
- update to new version 1.25.4

* Sat Dec 27 2008 Adam Williamson <awilliamson@mandriva.org> 1.25.2-5mdv2009.1
+ Revision: 319618
- add literal.patch: fix a string literal error
- rebuild with python 2.6

* Sat Dec 13 2008 Funda Wang <fwang@mandriva.org> 1.25.2-3mdv2009.1
+ Revision: 313959
- fix typo

* Wed Dec 10 2008 Frederic Crozat <fcrozat@mandriva.com> 1.25.2-2mdv2009.1
+ Revision: 312517
- Add missing dependency in devel package

* Tue Dec 02 2008 Götz Waschk <waschk@mandriva.org> 1.25.2-1mdv2009.1
+ Revision: 308987
- update to new version 1.25.2

* Sat Nov 08 2008 Oden Eriksson <oeriksson@mandriva.com> 1.25.1-2mdv2009.1
+ Revision: 301020
- rebuilt against new libxcb

* Tue Nov 04 2008 Götz Waschk <waschk@mandriva.org> 1.25.1-1mdv2009.1
+ Revision: 299717
- update to new version 1.25.1

* Mon Sep 22 2008 Götz Waschk <waschk@mandriva.org> 1.24.0-1mdv2009.0
+ Revision: 286518
- new version
- update build deps
- add gconf schema file

* Mon Sep 08 2008 Götz Waschk <waschk@mandriva.org> 1.23.92-1mdv2009.0
+ Revision: 282531
- new version

* Mon Sep 01 2008 Götz Waschk <waschk@mandriva.org> 1.23.91-1mdv2009.0
+ Revision: 278456
- new version
- drop patch

* Fri Aug 22 2008 Frederic Crozat <fcrozat@mandriva.com> 1.23.6-2mdv2009.0
+ Revision: 275123
- Patch0 (Fedora): Performance improvement for FF3 (GNOME bug #350552)
- Fix python package dependencies, ensuring AT registry is correctly pulled

* Mon Aug 04 2008 Götz Waschk <waschk@mandriva.org> 1.23.6-1mdv2009.0
+ Revision: 263077
- new version

* Mon Jul 21 2008 Götz Waschk <waschk@mandriva.org> 1.23.5-2mdv2009.0
+ Revision: 239390
- bump
- new version

* Thu Jul 03 2008 Götz Waschk <waschk@mandriva.org> 1.23.3-1mdv2009.0
+ Revision: 231016
- new version
- update buildrequires
- update license

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Wed Apr 09 2008 Götz Waschk <waschk@mandriva.org> 1.22.1-1mdv2009.0
+ Revision: 192456
- new version

* Sun Mar 23 2008 Emmanuel Andry <eandry@mandriva.org> 1.22.0-2mdv2008.1
+ Revision: 189623
- Fix lib group

* Mon Mar 10 2008 Götz Waschk <waschk@mandriva.org> 1.22.0-1mdv2008.1
+ Revision: 183414
- new version

* Mon Feb 25 2008 Götz Waschk <waschk@mandriva.org> 1.21.92-2mdv2008.1
+ Revision: 174650
- new version
- drop patch

* Fri Feb 15 2008 Frederic Crozat <fcrozat@mandriva.com> 1.21.5-2mdv2008.1
+ Revision: 168955
- Patch0 (SVN): add new API/fixes for accerciser

* Mon Jan 14 2008 Götz Waschk <waschk@mandriva.org> 1.21.5-1mdv2008.1
+ Revision: 151192
- new version

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Dec 04 2007 Götz Waschk <waschk@mandriva.org> 1.21.3-1mdv2008.1
+ Revision: 115241
- new version

* Mon Oct 29 2007 Götz Waschk <waschk@mandriva.org> 1.21.1-1mdv2008.1
+ Revision: 103021
- new version

* Mon Oct 15 2007 Götz Waschk <waschk@mandriva.org> 1.20.1-1mdv2008.1
+ Revision: 98505
- new version

* Mon Sep 17 2007 Götz Waschk <waschk@mandriva.org> 1.20.0-1mdv2008.0
+ Revision: 88986
- new version
- drop merged patch
- new devel name

* Thu Aug 02 2007 Frederic Crozat <fcrozat@mandriva.com> 1.19.5-2mdv2008.0
+ Revision: 58025
- Patch0 (SVN):  fix locking (GNOME bug #462412)

* Tue Jul 10 2007 Götz Waschk <waschk@mandriva.org> 1.19.5-1mdv2008.0
+ Revision: 50884
- new version

* Thu Jun 07 2007 Götz Waschk <waschk@mandriva.org> 1.19.3-1mdv2008.0
+ Revision: 36461
- fix docs installation
- fix python directory
- new version

* Tue Apr 17 2007 Götz Waschk <waschk@mandriva.org> 1.18.1-1mdv2008.0
+ Revision: 13870
- new version


* Mon Mar 19 2007 Thierry Vignaud <tvignaud@mandriva.com> 1.18.0-2mdv2007.1
+ Revision: 146571
- do not package big ChangeLog

* Mon Mar 12 2007 Götz Waschk <waschk@mandriva.org> 1.18.0-1mdv2007.1
+ Revision: 141740
- new version

* Wed Feb 28 2007 Götz Waschk <waschk@mandriva.org> 1.17.2-1mdv2007.1
+ Revision: 126865
- new version

* Mon Feb 26 2007 Götz Waschk <waschk@mandriva.org> 1.17.1-1mdv2007.1
+ Revision: 125766
- new version

* Mon Feb 12 2007 Götz Waschk <waschk@mandriva.org> 1.17.0-1mdv2007.1
+ Revision: 118934
- new version

* Mon Jan 22 2007 Götz Waschk <waschk@mandriva.org> 1.7.16-1mdv2007.1
+ Revision: 111825
- new version

* Mon Jan 08 2007 Götz Waschk <waschk@mandriva.org> 1.7.15-1mdv2007.1
+ Revision: 105952
- new version

* Fri Dec 29 2006 Frederic Crozat <fcrozat@mandriva.com> 1.7.14-3mdv2007.1
+ Revision: 102442
- Fix biarch
- Add conflicts to ease upgrade

* Thu Dec 28 2006 Frederic Crozat <fcrozat@mandriva.com> 1.7.14-2mdv2007.1
+ Revision: 102260
- Patch0 (CVS): fix crash in preferences dialog

* Mon Dec 18 2006 Götz Waschk <waschk@mandriva.org> 1.7.14-1mdv2007.1
+ Revision: 98490
- new version

* Tue Nov 28 2006 Götz Waschk <waschk@mandriva.org> 1.7.13-2mdv2007.1
+ Revision: 87924
- spec fix
- new version

* Fri Oct 13 2006 Götz Waschk <waschk@mandriva.org> 1.7.12-3mdv2006.0
+ Revision: 63781
- rebuild
- fix buildrequires
- Import at-spi

* Wed Oct 04 2006 Götz Waschk <waschk@mandriva.org> 1.7.12-1mdv2007.0
- New version 1.7.12

* Wed Aug 23 2006 Götz Waschk <waschk@mandriva.org> 1.7.11-1mdv2007.0
- New release 1.7.11

* Wed Jul 26 2006 Götz Waschk <waschk@mandriva.org> 1.7.10-1
- New release 1.7.10

* Tue Jul 18 2006 Frederic Crozat <fcrozat@mandriva.com> 1.7.9-4mdv2007.0
- Rebuild again with latest libgail

* Sat Jul 15 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 1.7.9-3
- add BuildRequires: libxtst-devel

* Fri Jul 14 2006 Frederic Crozat <fcrozat@mandriva.com> 1.7.9-2mdv2007.0
- Rebuild with latest libgail

* Fri Jul 14 2006 Götz Waschk <waschk@mandriva.org> 1.7.9-1
- New release 1.7.9

* Tue Jul 11 2006 G�tz Waschk <waschk@mandriva.org> 1.7.8-1mdv2007.0
- bump  deps
- New release 1.7.8

* Thu Apr 27 2006 Nicolas L�cureuil <neoclust@mandriva.org> 1.7.7-2mdk
- Fix  BuildRequires using perl policy

* Wed Apr 19 2006 Frederic Crozat <fcrozat@mandriva.com> 1.7.7-1mdk
- Release 1.7.7

* Fri Feb 24 2006 Frederic Crozat <fcrozat@mandriva.com> 1.6.6-3mdk
- Use mkrel

* Sat Jan 07 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 1.6.6-2mdk
- Rebuild

* Fri Oct 07 2005 Frederic Crozat <fcrozat@mandriva.com> 1.6.6-1mdk
- Release 1.6.6

* Thu May 12 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 1.6.4-1mdk
- New release 1.6.4

* Fri Dec 10 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 1.6.2-1mdk
- New release 1.6.2

* Tue Nov 09 2004 G�tz Waschk <waschk@linux-mandrake.com> 1.6.0-1mdk
- New release 1.6.0

* Fri Sep 03 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 1.4.2-3mdk
- Enable libtoolize

* Fri Apr 23 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 1.4.2-2mdk
- Fix Buildrequires

* Wed Apr 21 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 1.4.2-1mdk
- New release 1.4.2

* Wed Apr 07 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 1.4.0-1mdk
- New release 1.4.0

