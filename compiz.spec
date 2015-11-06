%global    core_plugins    blur clone cube decoration fade ini inotify minimize move place png regex resize rotate scale screenshot switcher video water wobbly zoom fs obs commands wall annotate svg matecompat
 
# List of plugins passed to ./configure.  The order is important
 
%global    plugins         core,png,svg,video,screenshot,decoration,clone,place,fade,minimize,move,resize,switcher,scale,wall,obs


Name:           compiz
URL:            https://github.com/raveit65/compiz
License:        GPLv2+ and LGPLv2+ and MIT
Group:          User Interface/Desktops
Version:        0.8.9
Release:        1%{?dist}
Epoch:          1
Summary:        OpenGL window and compositing manager
 
# libdrm is not available on these arches
ExcludeArch:   s390 s390x
 
# github does not create xz tarballs, so i decided to release at fedorapeople
Source0: https://raveit65.fedorapeople.org/compiz/SOURCE/%{version}/%{name}-%{version}.tar.xz

# fedora specific
Patch0:        compiz_fedora-logo.patch

BuildRequires: libX11-devel
BuildRequires: libdrm-devel
BuildRequires: libwnck-devel
BuildRequires: libXcursor-devel
BuildRequires: libXfixes-devel
BuildRequires: libXrandr-devel
BuildRequires: libXrender-devel
BuildRequires: libXcomposite-devel
BuildRequires: libXdamage-devel
BuildRequires: libXext-devel
BuildRequires: libXt-devel
BuildRequires: libSM-devel
BuildRequires: libICE-devel
BuildRequires: libXmu-devel
BuildRequires: desktop-file-utils
BuildRequires: intltool
BuildRequires: gettext
BuildRequires: librsvg2-devel
BuildRequires: mesa-libGLU-devel
BuildRequires: fuse-devel
BuildRequires: cairo-devel
BuildRequires: libtool
BuildRequires: libjpeg-turbo-devel
BuildRequires: libxslt-devel
BuildRequires: marco-devel

Requires:       fedora-logos
Requires:       glx-utils

# obsolete old subpackges
Obsoletes: %{name}-xfce < %{epoch}:%{version}-%{release}
Obsoletes: %{name}-lxde < %{epoch}:%{version}-%{release}


%description
Compiz is one of the first OpenGL-accelerated compositing window
managers for the X Window System. The integration allows it to perform
compositing effects in window management, such as a minimization
effect and a cube work space. Compiz is an OpenGL compositing manager
that use Compiz use EXT_texture_from_pixmap OpenGL extension for
binding redirected top-level windows to texture objects.
 
%package devel
Summary: Development packages for compiz
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires: pkgconfig
Requires: libXcomposite-devel libXfixes-devel libXdamage-devel libXrandr-devel
Requires: libXinerama-devel libICE-devel libSM-devel libxml2-devel
Requires: libxslt-devel startup-notification-devel
 
%description devel
The compiz-devel package includes the header files,
and developer docs for the compiz package.
Install compiz-devel if you want to develop plugins for the compiz
windows and compositing manager.

%package mate
Summary: Compiz mate integration bits
Group: User Interface/Desktops
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
 
%description mate
The compiz-mate package contains the matecompat plugin
and start scripts to start Compiz with emerald and
gtk-windows-decorator.

 
%prep
%setup -q

%patch0 -p1 -b .fedora-logo
 
%build
%configure \
    --enable-librsvg \
    --enable-gtk \
    --enable-marco \
    --enable-mate \
    --with-default-plugins=%{plugins}
 
make %{?_smp_mflags} imagedir=%{_datadir}/pixmaps
 
 
%install
%{make_install}

desktop-file-install                              \
    --delete-original                             \
    --dir=$RPM_BUILD_ROOT%{_datadir}/applications \
$RPM_BUILD_ROOT%{_datadir}/applications/*.desktop

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} ';'

%find_lang %{name}
 
cat %{name}.lang > core-files.txt
 
for f in %{core_plugins}; do
  echo %{_libdir}/compiz/lib$f.so
  echo %{_datadir}/compiz/$f.xml
done >> core-files.txt
 

%post
/sbin/ldconfig
/bin/touch --no-create %{_datadir}/compiz &>/dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
 
%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/compiz &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/compiz &>/dev/null || :
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/compiz &>/dev/null || :
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%post mate -p /sbin/ldconfig

%postun mate -p /sbin/ldconfig

 
 
%files -f core-files.txt
%doc AUTHORS ChangeLog COPYING.GPL COPYING.LGPL README TODO NEWS
%{_bindir}/compiz
%{_bindir}/gtk-window-decorator
%{_libdir}/libdecoration.so.*
%dir %{_libdir}/compiz
%dir %{_datadir}/compiz
%{_datadir}/compiz/*.png
%{_datadir}/compiz/core.xml
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/icons/hicolor/*/apps/*.png

%files mate
%{_bindir}/gtk-window-decorator
%{_bindir}/compiz-mate-gtk
%{_bindir}/compiz-decorator-gtk
%{_datadir}/applications/compiz-mate-gtk.desktop
%{_datadir}/applications/gtk-decorator.desktop

%files devel
%{_libdir}/pkgconfig/compiz.pc
%{_libdir}/pkgconfig/libdecoration.pc
%{_libdir}/pkgconfig/compiz-cube.pc
%{_libdir}/pkgconfig/compiz-scale.pc
%{_includedir}/compiz/
%{_libdir}/libdecoration.so


%changelog
* Fri Nov 06 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.9-1
- update to 0.8.9
- new upstream is at https://github.com/raveit65/compiz
- remove upstreamed patches
- move emerald scripts to emerald
- no xfce/lxde subpackages anymore
- remove runtime requires emerald and hicolors
- use runtime require fedora-logos for the cube plugin
- remove external matecompat logo, it's in the tarball now
- remove mate gwd scripts, they are in the tarball now
- remove old obsoletes for f15/16
- some spec file cleanup
- add desktop-file-install scriptlet
- update build requires
- move gtk-window-decorator to main package

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.8-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 18 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-29
- rebuild for f22

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.8-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.8-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Feb 16 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-26
- change BR to marco-devel for f21
- rework remove-keybindings-and-mate-windows-settings-files patch
- rework remove-kde patch
- rwork compiz_remove_mateconf_dbus_glib.patch
- rework compiz_remove_old_metacity_checks.patch
- compiz_cube-set-opacity-during-rotation-to-70-as-default.patch
- switch to libwnck for f21

* Thu Aug 15 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-25
- obsolete old compiz versions from f15/f16, rhbz (#997557)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.8-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 03 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-23
- fix windows-decorator scripts and desktop files

* Sun May 26 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-22
- add patch to speed up start
- remove --sm-disable --ignore-desktop-hints from start scipts
- fix build for aarch64
- add xfce subpackage again with start script and desktop file
- move matecompat plugin to main package
- add requires hicolor-icon-theme
- add scripts and desktop files for switch the windows-decorator to
- mate subpackage
- remove useless compiz_new_add-cursor-theme-support.patch
- complete removal of gconf
- clean up patches
- rename patches and add more descriptions to spec file
- remove unnecessary desktop-file-validate checks
- update icon-cache scriptlets

* Wed May 08 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-21
- remove compiz-lxde-gtk script and desktop file

* Tue May 07 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-20
- DISABLE XFCE SUPPORT
- remove xfce subpackage
- move gwd decorator to a subpackage

* Mon Apr 29 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-19
- remove compiz-xfce-gtk start script

* Mon Apr 29 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-18
- rename compiz_disable_gtk_disable_deprecated.patch

* Mon Apr 29 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-17
- remove compiz-xfce-gtk.desktop

* Wed Apr 24 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-16
- enable gtk-windows-decorator based on marco (mate-window-manager)
- add compiz_disable_gdk_gtk_disable_deprecated patch
- remove dbus
- remove glib
- remove mateconf
- remove kde
- remove keybindings
- add start scripts for gtk-windows-decorator
- update start scripts for emerald
- add ldconfig scriptlet for mate subpackage
- using libmatewnck instead of libwnck

* Wed Feb 13 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-15
- fix primary-is-control in wall patch

* Sun Feb 10 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-14
- add compiz_primary-is-control.patch
- this will set all default configurations to pimary key
- change compiz-wall.patch for set primary is control key
- fix (#909657)

* Fri Jan 04 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-13
- add require emerald again

* Tue Dec 25 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-12
- remove require emerald until it is in fedora stable

* Sat Dec 22 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-11
- do some major changes
- disable mateconf and use libini text file configuration backend
- remove mateconf from scriptlet section
- move glib annotate svg plugins to core package
- disable gtk-windows-decorator
- drop compiz-mate-gtk compiz session script
- disable gtk-windows-decorator patches
- disable marco/metacity
- disable mate/gnome
- disable mate/gnome keybindings
- insert compiz-mate-emerald compiz session script
- insert compiz-xfce-emerald compiz session script
- insert compiz-lxde-emerald compiz session script
- add emerald as require
- add matecompat icon
- add icon cache scriptlets 


* Sun Dec 02 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-10
- add %%global  plugins_schemas again

* Sun Dec 02 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-9
- revert scriptlet change

* Sun Dec 02 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-8
- add %%global  plugins_schemas
- change mateconf scriptlets
- remove (Requires(post): desktop-file-utils)
- add some patches from Jasmine Hassan jasmine.aura@gmail.com
- remove (noreplace) from mateconf schema directory
- add desktop-file-validate
- disable mate keybindings for the moment

* Fri Oct 05 2012 Leigh Scott <leigh123linux@googlemail.com> - 1:0.8.8-7
- remove and obsolete compiz-kconfig schema

* Fri Oct 05 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.8-6
- remove update update-desktop-database from %%post mate
- remove (noreplace) from mateconf schema dir
- remove Requires(post): desktop-file-utils
- add epoch tags

* Wed Sep 26 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.8-5
- change compiz-0.88_incorrect-fsf-address.patch

* Wed Sep 26 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.8-4
- remove upstreamed patches
- own include dir
- add compiz-mate-gtk source and compiz-mate-gtk.desktop file
- add keybinding sources
- change %%define to %%global entries
- rename no-more-gnome-wm-settings.patch to no-more-mate-wm-settings.patch
- add compiz-0.88_incorrect-fsf-address.patch
- clean up build section

* Sun Sep 16 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.8-3
- add isa tags
- remove kde stuff
- remove obsolete beryl stuff
- add comiz_mate_fork.patch
- remove %%defattr(-, root, root)
- add compiz_gtk_window_decoration_button_placement.patch
- enable some compiz keybindings

* Tue May 15 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.8-2
- add compiz_mate_fix.patch

* Tue May 15 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.8-1
- build for mate

* Sun May 06 2012 Andrew Wyatt <andrew@fuduntu.org> - 0.8.8-1
- Update to latest stable release

* Tue Nov 30 2010 leigh scott <leigh123linux@googlemail.com> - 0.8.6-6
- add more upstream gdk fixes

