%global    core_plugins    blur clone cube dbus decoration fade ini inotify minimize move place png regex resize rotate scale screenshot switcher video water wobbly zoom fs obs commands wall
 
%global    mate_plugins    annotate mateconf glib svg matecompat
 
%global  plugins_schemas     compiz-annotate compiz-blur compiz-clone compiz-commands compiz-core compiz-cube compiz-dbus compiz-decoration compiz-fade compiz-fs compiz-glib compiz-ini compiz-inotify compiz-matecompat compiz-mateconf compiz-minimize compiz-move compiz-obs compiz-place compiz-png compiz-regex compiz-resize compiz-rotate compiz-scale compiz-screenshot compiz-svg compiz-switcher compiz-video compiz-wall compiz-water compiz-wobbly compiz-zoom gwd
 
# List of plugins passed to ./configure.  The order is important
 
%global    plugins         core,glib,mateconf,dbus,png,svg,video,screenshot,decoration,clone,place,fade,minimize,move,resize,switcher,scale,wall,obs
 
Name:           compiz
URL:            http://www.compiz.org
License:        GPLv2+ and LGPLv2+ and MIT
Group:          User Interface/Desktops
Version:        0.8.8
Release:        10%{?dist}
Epoch:          1
Summary:        OpenGL window and compositing manager
 
# libdrm is not available on these arches
ExcludeArch:   s390 s390x
 
Requires:       system-logos
Requires:       glx-utils
 
BuildRequires: libX11-devel
BuildRequires: libdrm-devel
BuildRequires: libwnck-devel
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
BuildRequires: mate-desktop-devel
BuildRequires: mate-control-center-devel
BuildRequires: mate-conf-devel
BuildRequires: desktop-file-utils
BuildRequires: intltool
BuildRequires: gettext
BuildRequires: dbus-devel
BuildRequires: dbus-glib-devel
BuildRequires: librsvg2-devel
BuildRequires: mate-window-manager-devel
BuildRequires: mesa-libGLU-devel
BuildRequires: fuse-devel
BuildRequires: cairo-devel
BuildRequires: libtool
BuildRequires: libxslt-devel
 
Source0:       http://releases.compiz.org/%{version}/%{name}-%{version}.tar.bz2
Source2:       compiz-mate-gtk
Source3:       compiz-mate-gtk.desktop
Source4:       50-marco-navigation.xml
Source5:       50-marco-system.xml
Source6:       50-marco-windows.xml
 
# fork gnome to mate
Patch0:        comiz_mate_fork.patch
# fix http://forums.mate-desktop.org/viewtopic.php?f=8&t=818
Patch1:        compiz_gtk_window_decoration_button_placement.patch
Patch2:        compiz_windows-decorator.patch
# Patches that are not upstream
Patch3:        composite-cube-logo.patch
Patch4:        fedora-logo.patch
Patch5:        redhat-logo.patch
Patch6:        compiz-0.8.6-wall.patch
Patch7:        compiz-0.8.6-unloadpluginfix.patch
Patch8:        no-more-mate-wm-settings.patch
Patch9:        compiz-0.88_incorrect-fsf-address.patch
Patch10:       compiz-disable-child-window-clipping.patch
Patch11:       compiz-add-cursor-theme-support.patch
Patch12:       compiz-fix-gtk-window-decorator-no-argb-crash.patch
Patch13:       compiz_fix-no-border-window-shadow.patch
Patch14:       compiz_draw_dock_shadows_on_desktop.patch
Patch15:       compiz_optional-fbo.patch
Patch16:       compiz_call_glxwaitx_before_drawing.patch
Patch17:       compiz_always_unredirect_screensaver_on_nvidia.patch
Patch18:       compiz_hide_tooltip_on_decorator.patch
Patch19:       compiz_fullscreen_stacking_fixes.patch
Patch20:       compiz_damage-report-non-empty.patch
Patch21:       compiz_stacking.patch
 
 
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
Requires(pre): mate-conf
Requires(post): mate-conf
Requires(preun): mate-conf
 
%description mate
The compiz-mate package contains gtk-window-decorator,
and other mate integration related stuff.
 
 
%prep
%setup -q
%patch0 -p1 -b .comiz_mate_fork
%patch1 -p1 -b .compiz_gtk_window_decoration_button
%patch2 -p1 -b .compiz_windows-decorator
%patch3 -p1 -b .composite-cube-logo
%if 0%{?fedora}
%patch4 -p1 -b .fedora-logo
%else
%patch5 -p1 -b .redhat-logo
%endif
%patch6 -p1 -b .wall
%patch7 -p1 -b .unloadfix
%patch8 -p1 -b .mate-wm-settings
%patch9 -p1 -b .incorrect-fsf-address
%patch11 -p1 -b .cursor-theme-support
%patch12 -p1 -b .gtk-window-decorator-no-argb-crash
%patch13 -p1 -b .no-border-window-shadow
%patch14 -p1 -b .draw_dock_shadows
%patch15 -p1 -b .fbo
%patch16 -p1 -b .glxwaitx_before_drawing
%patch17 -p1 -b .always_unredirect_screensaver
%patch18 -p1 -b .tooltip_on_decorator
%patch19 -p1 -b .fullscreen_stacking
%patch20 -p1 -b .damage-report
%patch21 -p1 -b .stacking
 
 
%build
 
libtoolize
aclocal
autoconf
automake
%configure \
    --enable-mateconf \
    --enable-dbus \
    --enable-librsvg \
    --enable-gtk \
    --enable-marco \
    --enable-mate \
    --with-default-plugins=%{plugins} \
    --enable-mate-keybindings \
    --disable-kde \
    --disable-kde4 \
    --disable-kconfig         \
    --disable-mate-keybindings
 
make %{?_smp_mflags} imagedir=%{_datadir}/pixmaps
 
 
%install
export MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make DESTDIR=$RPM_BUILD_ROOT install || exit 1
unset MATECONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
 
install %SOURCE2 $RPM_BUILD_ROOT%{_bindir}
 
desktop-file-install --vendor="" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  %SOURCE3
 
rm $RPM_BUILD_ROOT%{_datadir}/compiz/kconfig.xml
rm $RPM_BUILD_ROOT%{_sysconfdir}/mateconf/schemas/compiz-kconfig.schemas
 
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} ';'
 
# create compiz keybindings file based on the marco ones
# lifted straight from Ubuntu, as long as installation of the upstream
# ones is broken at least (I've reported this upstream)
#mkdir -p $RPM_BUILD_ROOT/%{_datadir}/mate-control-center/keybindings
#sed 's/wm_name=\"Marco\" package=\"marco\"/wm_name=\"Compiz\" package=\"compiz\"/'  /usr/share/mate-control-center/keybindings/50-marco-desktop-key.xml > $RPM_BUILD_ROOT/%{_datadir}/mate-control-center/keybindings/50-compiz-desktop-key.xml
#sed 's/wm_name=\"Marco\" package=\"marco\"/wm_name=\"Compiz\" package=\"compiz\"/'  /usr/share/mate-control-center/keybindings/50-marco-key.xml > $RPM_BUILD_ROOT/%{_datadir}/mate-control-center/keybindings/50-compiz-key.xml
 
#cp %SOURCE4 $RPM_BUILD_ROOT%{_datadir}/mate-control-center/keybindings/50-compiz-navigation.xml
#cp %SOURCE5 $RPM_BUILD_ROOT%{_datadir}/mate-control-center/keybindings/50-compiz-system.xml
#cp %SOURCE6 $RPM_BUILD_ROOT%{_datadir}/mate-control-center/keybindings/50-compiz-windows.xml
 
#sed -i 's#key=\"/apps/marco/general/num_workspaces\" comparison=\"gt\"##g' $RPM_BUILD_ROOT/%{_datadir}/mate-control-center/keybindings/50-compiz-desktop-key.xml
#sed -i 's#key=\"/apps/marco/general/num_workspaces\" comparison=\"gt\"##g' $RPM_BUILD_ROOT/%{_datadir}/mate-control-center/keybindings/50-compiz-key.xml
 
%find_lang %{name}
 
cat %{name}.lang > core-files.txt
 
for f in %{core_plugins}; do
  echo %{_libdir}/compiz/lib$f.so
  echo %{_datadir}/compiz/$f.xml
done >> core-files.txt
 
for f in %{mate_plugins}; do
  echo %{_libdir}/compiz/lib$f.so
  echo %{_datadir}/compiz/$f.xml
done >> mate-files.txt
 
 
%check
desktop-file-validate $RPM_BUILD_ROOT/%{_datadir}/applications/compiz-mate-gtk.desktop
 
 
%post -p /sbin/ldconfig
 
%postun -p /sbin/ldconfig
 
%post mate
%mateconf_schema_upgrade %{plugins_schemas}
 
%pre mate
%mateconf_schema_prepare %{plugins_schemas}
%mateconf_schema_obsolete compiz-kconfig
 
%preun mate
%mateconf_schema_remove %{plugins_schemas}
 
 
%files -f core-files.txt
%doc AUTHORS ChangeLog COPYING.GPL COPYING.LGPL README TODO NEWS
%{_bindir}/compiz
%{_libdir}/libdecoration.so.*
%dir %{_libdir}/compiz
%dir %{_datadir}/compiz
%{_datadir}/compiz/*.png
%{_datadir}/compiz/core.xml
 
%files mate -f mate-files.txt
%{_bindir}/compiz-mate-gtk
%{_bindir}/gtk-window-decorator
#%{_datadir}/mate-control-center/keybindings/50-compiz-desktop-key.xml
#%{_datadir}/mate-control-center/keybindings/50-compiz-key.xml
#%{_datadir}/mate-control-center/keybindings/50-compiz-navigation.xml
#%{_datadir}/mate-control-center/keybindings/50-compiz-system.xml
#%{_datadir}/mate-control-center/keybindings/50-compiz-windows.xml
%{_datadir}/applications/compiz-mate-gtk.desktop
%exclude %{_datadir}/applications/compiz.desktop
%config(noreplace) %{_sysconfdir}/mateconf/schemas/*.schemas
 
 
%files devel
%{_libdir}/pkgconfig/compiz.pc
%{_libdir}/pkgconfig/libdecoration.pc
%{_libdir}/pkgconfig/compiz-cube.pc
%{_libdir}/pkgconfig/compiz-mateconf.pc
%{_libdir}/pkgconfig/compiz-scale.pc
%{_datadir}/compiz/schemas.xslt
%{_includedir}/compiz/
%{_libdir}/libdecoration.so

%changelog
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

