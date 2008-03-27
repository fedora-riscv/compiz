%define		dialogversion	0.7.17
%define 	kde_dialogversion 0.0.5

%define		core_plugins	blur clone cube dbus decoration fade ini inotify minimize move place plane png regex resize rotate scale screenshot switcher video water wobbly zoom fs

%define		gnome_plugins	annotate gconf glib svg

# List of plugins passed to ./configure.  The order is important

%define		plugins		core,glib,gconf,dbus,png,svg,video,screenshot,decoration,clone,place,fade,minimize,move,resize,switcher,scale,plane

Name:           compiz
URL:            http://www.go-compiz.org
License:        X11/MIT/GPL
Group:          User Interface/Desktops
Version:        0.7.2
Release:        3%{?dist}

Summary:        OpenGL window and compositing manager
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# libdrm is not available on these arches
ExcludeArch:   	s390 s390x ppc64

Requires:	xorg-x11-server-Xorg >= 1.3.0.0-19.fc8
Requires:	mesa-libGL >= 7.0.1-2.fc8
Requires:      system-logos

Requires(post): desktop-file-utils

BuildRequires:  libX11-devel, libdrm-devel, libwnck-devel
BuildRequires:  libXfixes-devel, libXrandr-devel, libXrender-devel
BuildRequires:  libXcomposite-devel, libXdamage-devel, libXext-devel
BuildRequires:  libXt-devel, libXmu-devel, libICE-devel, libSM-devel
BuildRequires:  gnome-desktop-devel, control-center-devel, GConf2-devel
BuildRequires:  desktop-file-utils
BuildRequires:  intltool >= 0.35
BuildRequires:  gettext
BuildRequires:  dbus-devel
BuildRequires:  librsvg2-devel
BuildRequires:  metacity-devel >= 2.18
BuildRequires:  mesa-libGLU-devel
BuildRequires:  kdebase-workspace-devel
BuildRequires:  dbus-qt-devel
BuildRequires:  fuse-devel

Source0:       http://releases.compiz-fusion.org/compiz/%{version}/%{name}-%{version}.tar.bz2
Source1:	desktop-effects-%{dialogversion}.tar.bz2
Source2:	kde-desktop-effects-%{kde_dialogversion}.tar.bz2

# Make sure that former beryl users still have bling
Obsoletes: beryl-core

# Patches that are not upstream
Patch103: composite-cube-logo.patch
Patch105: fedora-logo.patch
Patch106: redhat-logo.patch
#Patch110: scale-key.patch
Patch111: gconf-core-plugin-loopfix.patch

%description
Compiz is one of the first OpenGL-accelerated compositing window
managers for the X Window System. The integration allows it to perform
compositing effects in window management, such as a minimization
effect and a cube workspace.  Compiz is an OpenGL compositing manager
that use Compiz use EXT_texture_from_pixmap OpenGL extension for
binding redirected top-level windows to texture objects.

%package devel
Summary: Development packages for compiz
Group: Development/Libraries
Requires: compiz = %{version}-%{release}
Requires: pkgconfig
Requires: libXcomposite-devel libXfixes-devel libXdamage-devel libXrandr-devel
Requires: libXinerama-devel libICE-devel libSM-devel libxml2-devel
Requires: libxslt-devel startup-notification-devel

%description devel
The compiz-devel package includes the header files,
and developer docs for the compiz package.

Install compiz-devel if you want to develop plugins for the compiz
windows and compositing manager.

%package gnome
Summary: Compiz gnome integration bits
Group: User Interface/Desktops
Requires: gnome-session >= 2.19.6-5
Requires: metacity >= 2.18
Requires: libwnck >= 2.15.4
Requires: %{name} = %{version}
Requires(pre): GConf2
Requires(post): GConf2
Requires(preun): GConf2
Obsoletes: compiz < 0.5.2-8
Obsoletes: beryl-gnome

%description gnome
The compiz-gnome package contains gtk-window-decorator,
and other gnome integration related stuff.

%package kde
Summary: Compiz kde integration bits
Group: User Interface/Desktops
Requires: %{name} = %{version}
Requires: compiz-manager
Obsoletes: beryl-kde

%description kde
The compiz-kde package contains kde-window-decorator,
and other kde integration related stuff.


%prep
%setup -q -T -b1 -n desktop-effects-%{dialogversion}
%setup -q -T -b2 -n kde-desktop-effects-%{kde_dialogversion}
%setup -q 

%patch103 -p1 -b .composite-cube-logo
%if 0%{?fedora}
%patch105 -p1 -b .fedora-logo
%else
%patch106 -p1 -b .redhat-logo
%endif
#%patch110 -p1 -b .scale-key
%patch111 -p1 -b .gconf-core-loop


%build
rm -rf $RPM_BUILD_ROOT

CPPFLAGS="$CPPFLAGS -I$RPM_BUILD_ROOT%{_includedir}"
export CPPFLAGS

#needed to find kde4 libs
LDFLAGS="$LDFLAGS -L%{_libdir}/kde4/devel"
export LDFLAGS


%configure 					\
	--enable-gconf 				\
	--enable-dbus 				\
	--enable-place 				\
	--enable-librsvg 			\
	--enable-gtk 				\
	--enable-metacity 			\
	--enable-gnome				\
	--with-default-plugins=%{plugins}	\
	--enable-gnome-keybindings		\
	--enable-kde4

make %{?_smp_mflags} imagedir=%{_datadir}/pixmaps

# desktop-effects
cd ../desktop-effects-%{dialogversion}
%configure 


%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make DESTDIR=$RPM_BUILD_ROOT install || exit 1
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

echo INSTALLING DESKTOP EFFECTS
pushd ../desktop-effects-%{dialogversion}
make DESTDIR=$RPM_BUILD_ROOT install || exit 1
desktop-file-install --vendor redhat --delete-original      \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications             \
  $RPM_BUILD_ROOT%{_datadir}/applications/desktop-effects.desktop
popd

# kde-desktop-effects
echo INSTALLING KDE DESKTOP EFFECTS
pushd ../kde-desktop-effects-%{kde_dialogversion}
cp -a kde-desktop-effects.sh $RPM_BUILD_ROOT/%{_bindir}/
mkdir -p $RPM_BUILD_ROOT/%{_docdir}/compiz-kde-%{version}
cp -a ChangeLog COPYING README $RPM_BUILD_ROOT/%{_docdir}/compiz-kde-%{version}

iconlist="16 24 32 36 48 96"
for i in $iconlist; do
 mkdir -p $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/$i\x$i/apps/
 cp -p ../desktop-effects-%{dialogversion}/desktop-effects$i.png $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/$i\x$i/apps/kde-desktop-effects.png
done

desktop-file-install --vendor=""           \
--dir=%{buildroot}%{_datadir}/applications/kde       \
kde-desktop-effects.desktop
popd


find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} ';'


%find_lang compiz
%find_lang desktop-effects

cat compiz.lang > core-files.txt
cat desktop-effects.lang > gnome-files.txt

for f in %{core_plugins}; do
  echo %{_libdir}/compiz/lib$f.so
  echo %{_datadir}/compiz/$f.xml
done >> core-files.txt

for f in %{gnome_plugins}; do
  echo %{_libdir}/compiz/lib$f.so
  echo %{_datadir}/compiz/$f.xml
done >> gnome-files.txt


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post gnome
update-desktop-database -q %{_datadir}/applications

export GCONF_CONFIG_SOURCE=`/usr/bin/gconftool-2 --get-default-source`
for f in %{core_plugins} %{gnome_plugins} core; do
  gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/compiz-$f.schemas >& /dev/null || :
done
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/gwd.schemas >& /dev/null || :

touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
	/usr/bin/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi


%pre gnome
if [ "$1" -gt 1 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  for f in %{core_plugins} %{gnome_plugins} core; do
    gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/compiz-$f.schemas >& /dev/null || :
  done
  gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/gwd.schemas >& /dev/null || :
fi


%preun gnome
if [ "$1" -eq 0 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  for f in %{core_plugins} %{gnome_plugins} core; do
    gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/compiz-$f.schemas >& /dev/null || :
  done
  gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/gwd.schemas >& /dev/null || :
fi


%postun gnome
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
	/usr/bin/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi

%post kde
update-desktop-database -q %{_datadir}/applications/kde
touch --no-create %{_datadir}/icons/hicolor

%postun kde
touch --no-create %{_datadir}/icons/hicolor


%clean
rm -rf $RPM_BUILD_ROOT


%files -f core-files.txt
%defattr(-, root, root)
%doc AUTHORS ChangeLog COPYING* README TODO
%{_bindir}/compiz
%{_libdir}/libdecoration.so.*
%dir %{_libdir}/compiz
%dir %{_datadir}/compiz
%{_datadir}/compiz/*.png
%{_datadir}/compiz/core.xml


%files gnome -f gnome-files.txt
%defattr(-, root, root)
%{_bindir}/gtk-window-decorator
%{_bindir}/desktop-effects
%{_libdir}/window-manager-settings/libcompiz.so
%{_datadir}/gnome/wm-properties/compiz.desktop
%{_datadir}/gnome-control-center/keybindings/50-compiz-desktop-key.xml
%{_datadir}/gnome-control-center/keybindings/50-compiz-key.xml
%{_datadir}/compiz/desktop-effects.glade
%{_datadir}/applications/redhat-desktop-effects.desktop
%{_datadir}/icons/hicolor/16x16/apps/desktop-effects.png
%{_datadir}/icons/hicolor/24x24/apps/desktop-effects.png
%{_datadir}/icons/hicolor/32x32/apps/desktop-effects.png
%{_datadir}/icons/hicolor/36x36/apps/desktop-effects.png
%{_datadir}/icons/hicolor/48x48/apps/desktop-effects.png
%{_datadir}/icons/hicolor/96x96/apps/desktop-effects.png
%{_sysconfdir}/gconf/schemas/*.schemas


%files kde
%defattr(-, root, root)
%{_bindir}/kde4-window-decorator
%{_docdir}/compiz-kde-%{version}
%{_bindir}/kde-desktop-effects.sh
%{_datadir}/applications/kde/kde-desktop-effects.desktop
%{_datadir}/icons/hicolor/*/apps/kde-desktop-effects.png
%{_datadir}/compiz/kconfig.xml

%files devel
%defattr(-, root, root)
%{_libdir}/pkgconfig/compiz.pc
%{_libdir}/pkgconfig/libdecoration.pc
%{_libdir}/pkgconfig/compiz-cube.pc
%{_libdir}/pkgconfig/compiz-gconf.pc
%{_libdir}/pkgconfig/compiz-scale.pc
%{_datadir}/compiz/schemas.xslt
%{_includedir}/compiz
%{_libdir}/libdecoration.so


%changelog
* Thu Mar 27 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.7.2-3
- Fix gconf plugin loop RH #438794, patch based on 
  older one from Guillaume Seguin
- Add core to default plugin list

* Wed Mar 26 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.7.2-2
- Reword kde-desktop-effects messages to mention Compiz by name (#438883)

* Mon Mar 24 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.7.2-1
- Update to 0.7.2

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.6.2-7
- Autorebuild for GCC 4.3

* Thu Jan 17 2008 Kristian Høgsberg <krh@redhat.com> - 0.6.2-6
- Update to desktop-effects version 0.7.17 which include more
  translations and move desktop-effects translations to compiz-gnome.
- Fix spelling in beryl-core obsoletes.

* Mon Jan 07 2008 Adel Gadllah <adel.gadllah@gmail.com> - 0.6.2-5
- Update buildrequires (kwd uses the kde3 api) 

* Tue Nov  6 2007 Stepan Kasal <skasal@redhat.com> - 0.6.2-4
- Fix a typo in description of the main package.
- All descriptions should end with a dot (unlike the summary line)

* Thu Oct 25 2007 Sebastian Vahl <fedora@deadbabylon.de> - 0.6.2-3
- Include kde-desktop-effects in kde subpackage

* Tue Oct 23 2007 Adel Gadllah <adel.gadllah@gmail.com> - 0.6.2-2
- Obsolete berly-core

* Mon Oct 22 2007 Warren Togami <wtogami@redhat.com> - 0.6.2-1
- 0.6.2

* Fri Oct 12 2007 Kristian Høgsberg <krh@redhat.com> - 0.6.0-2
- Disable scale corner initiate and install a GNOME key config entry.

* Wed Oct 10 2007 Warren Togami <wtogami@redhat.com> - 0.6.0-1
- 0.6.0 final
- always-restack-windows-on-map 

* Tue Oct  9 2007 Warren Togami <wtogami@redhat.com> - 0.5.2-14
- Make compiz behave with gnome-terminal (#304051)

* Fri Oct  5 2007 Matthias Clasen <mclasen@redhat.com> - 0.5.2-13
- Also install gwd.schemas (#319621)

* Thu Sep 20 2007 Kristian Høgsberg <krh@redhat.com> - 0.5.2-12
- Update to more recent 0.6 branch snapshot (fixes #253575).

* Fri Sep 14 2007 Warren Togami <wtogami@redhat.com> - 0.5.2-11
- compiz-gnome: install core schema so it actually works
- remove unnecessary gconf stuff from %%install

* Tue Aug 28 2007 Kristian Høgsberg <krh@redhat.com> - 0.5.2-9
- Make compiz-gnome Obsolete the older compiz package so yum/anaconda
  will pull it in (thans to Adel Gadllah).

* Wed Aug 22 2007 Kristian Høgsberg <krh@redhat.com> - 0.5.2-8
- Bump to desktop-effects 0.7.7 to avoid kill decorator when popping
  up dialog.
- Fix broken gconf install and uninstall rules.
- Pick up shadowman logo for RHEL builds (#232398).

* Tue Aug 21 2007 Kristian Høgsberg <krh@redhat.com> - 0.5.2-7.0ec3ec
- Add more-sm-junk.patch so we set SM restart style to
  SmRestartIfRunning on exit (#247163, #245971).
- Add Requires to compiz-devel (#253407).
- Update to desktop-effects 0.7.6, which terminates decorator when
  switching to metacity or on compiz failure (#215247, #215032).

* Fri Aug 17 2007 Adel Gadllah <adel.gadllah@gmail.com> 0.5.2-6.0ec3ec
- Split into gnome and kde subpackages
- Minor cleanups

* Wed Aug 15 2007 Kristian Høgsberg <krh@redhat.com> - 0.5.2-5.0ec3ec
- Reorder plugin list to avoid 'place' getting removed on startup.
- Add run-command-key.patch to put the run command key in the GNOME
  keyboard shortcut dialog (#213576).
- Drop a bunch of obsolete patches.
- Bump mesa-libGL and X server requires to fix TFP bugs for
  power-of-two textures (#251935).
- Rebase fedora-logo and composite-cube-logo patch.

* Tue Aug 14 2007 Kristian Høgsberg <krh@redhat.com> - 0.5.2-4.0ec3ec
- Build with desktop-effects so we don't pick up metacity work spaces.
  Fixes #250568.

* Tue Aug 14 2007 Kristian Høgsberg <krh@redhat.com> - 0.5.2-3.0ec3ec
- Build git snapshot from fedora branch at
  git://people.freedesktop.org/~krh/compiz, brances from 0.6 upstream
  branch.
- Fixes #237486.

* Fri Aug 10 2007 Kristian Høgsberg <krh@redhat.com> - 0.5.2-3
- Require desktop-effects 0.7.3 and gnome-session 2.19.6-5 which pass
  'glib' on the command line too.

* Fri Aug 10 2007 Kristian Høgsberg <krh@redhat.com> - 0.5.2-2
- Move xml meta data files to main package.

* Thu Aug  9 2007 Kristian Høgsberg <krh@redhat.com> - 0.5.2-1
- Update to 0.5.2.
- Require at least gnome-session 2.19.6-2 so gnome-wm starts compiz
  with LIBGL_ALWAYS_INDIRECT set.

* Wed Jun 27 2007 Kristian Høgsberg <krh@redhat.com> - 0.5.0-1
- Update to 0.5.0

* Tue Jun  5 2007 Matthias Clasen <mclasen@redhat.com> - 0.4.0-1
- Update to 0.4.0

* Mon Jun  4 2007 Matthias Clasen <mclasen@redhat.com> - 0.3.6-10
- Rebuild against new libwnck

* Sat Apr 21 2007 Matthias Clasen <mclasen@redhat.com> - 0.3.6-9
- Don't install INSTALL

* Mon Apr 16 2007 Kristian Høgsberg <krh@hinata.boston.redhat.com> - 0.3.6-8
- Update metacity build requires to metacity-devel.

* Wed Apr  4 2007 Kristian Høgsberg <krh@hinata.boston.redhat.com> - 0.3.6-7
- Fix typo in ./configure option.

* Wed Apr  4 2007 Kristian Høgsberg <krh@redhat.com> - 0.3.6-6
- Add place and clone plugins to default plugin list.

* Wed Mar 28 2007 Kristian Høgsberg <krh@redhat.com> - 0.3.6-5
- Update URL (#208214).
- Require at least metacity 2.18 (#232831).
- Add close-session.patch to deregister from SM when replaced (#229113).

* Tue Mar 27 2007 Kristian Høgsberg <krh@redhat.com> 0.3.6-4
- Explicitly disable KDE parts (#234128).

* Mon Mar 26 2007 Matthias Clasen <mclasen@redhat.com> 0.3.6-3
- Fix some directory ownership issues (#233825)
- Small spec cleanups

* Tue Feb  6 2007 Kristian Høgsberg <krh@redhat.com> 0.3.6
- Require gnome-session > 2.16 so it starts gtk-window-decorator.
- Update to desktop-effects 0.7.1 that doesn't refuse to work with Xinerama.

* Tue Jan 16 2007 Kristian Høgsberg <krh@redhat.com> - 0.3.6-1
- Update to 0.3.6, update patches.
- Drop autotool build requires.
- Drop glfinish.patch, cow.patch, resize-offset.patch and icon-menu-patch.
- Add libdecoration.so
- Update to desktop-effects-0.7.0, which spawns the right decorator
  and plays nicely with unknown plugins.

* Sat Nov 25 2006 Matthias Clasen <mclasen@redhat.com> - 0.3.4-2
- Update the fedora logo patch (#217224)

* Thu Nov 23 2006 Matthias Clasen <mclasen@redhat.com> - 0.3.4-1
- Update to 0.3.4

* Wed Nov 15 2006 Matthias Clasen <mclasen@redhat.com> - 0.3.2-2
- Use cow by default, bug 208044

* Fri Nov 10 2006 Matthias Clasen <mclasen@redhat.com> - 0.3.2-1
- Update to 0.3.2
- Drop upstreamed patches
- Work with new metacity theme api

* Mon Oct 2 2006 Soren Sandmann <sandmann@redhat.com> - 0.0.13-0.32.20060818git.fc6
- Install the .desktop file with desktop-file-install. Add X-Red-Hat-Base to make it appear in "Preferences", rather than "More Preferences".

* Sat Sep 30 2006 Soren Sandmann <sandmann@redhat.com> - 0.0.13-0.31.20060818git.fc6
- Add buildrequires on intltool

* Sat Sep 30 2006 Soren Sandmann <sandmann@redhat.com> - 0.0.13-0.31.20060818git.fc6
- Build

* Fri Sep 29 2006 Soren Sandmann <sandmann@redhat.com>
- Update to desktop-effects-0.6.163, which has translation enabled. (Bug 208257)

* Thu Sep 28 2006 Soren Sandmann <sandmann@redhat.com> - 0.0.13-0.30.20060817git.fc6
- Add patch to terminate keyboard moves when a mouse buttons is pressed. (Bug 207792).

* Thu Sep 28 2006 Soren Sandmann <sandmann@redhat.com>
- Change default plugin list to not include the plane plugin. (Bug 208448).
- Change default keybinding for shrink to be Pause (Bug 206187).

* Wed Sep 27 2006 Soren Sandmann <sandmann@redhat.com>
- Add patch to show a menu when the window icon is clicked. (Bug 201629).

* Tue Sep 26 2006 Soren Sandmann <sandmann@redhat.com> - 0.0.13-0.29.20060817git.fc6
- Add restart.patch to make compiz ask the session manager to restart it
  if it crashes (bug 200280).

* Mon Sep 25 2006 Soren Sandmann <sandmann@redhat.com> - 0.0.13-0.28.20060817git.fc6
- Change plane.patch to not do cyclical window movement in dimensions
  where the desktop has size 1 (bug 207263).

* Thu Sep 21 2006 Soren Sandmann <sandmann@redhat.com>
- Add patch to fix resizing smaller than minimum size (resize-offset.patch, bug 201623).

* Tue Sep 19 2006 Soren Sandmann <sandmann@redhat.com> - 0.0.13-0.27.20060817git.fc6
- Change .plane patch to 
  (a) not set the background color to pink in the plane plugin. 
  (b) allow workspaces with horizontal sizes less then 4.

* Mon Sep 18 2006 Soren Sandmann <sandmann@redhat.com> - 0.0.13-0.26.20060817git.fc6
- Change plane patch to correctly initialize the screen size to the
  defaults (bug 206088).

* Mon Sep 18 2006 Soren Sandmann <sandmann@redhat.com>
- Run update-desktop-database and gtk-update-icon-cache in post. Add icons
  to list of packaged files. Also bump to 0.6.137 of dialog (which just makes
  directories before attempting to install to them).

* Mon Sep 18 2006 Soren Sandmann <sandmann@redhat.com>
- Upgrade to 0.6.107 of the desktop-effects dialog box. Only change is
  that the new version has icons.

* Fri Sep 15 2006 Soren Sandmann <sandmann@redhat.com>
- Add patch to fix mispositioning of window decorator event windows (bug 201624)

* Fri Sep 15 2006 Soren Sandmann <sandamnn@redhat.com>
- Upgrade to version 0.6.83 of desktop-effects. (bug 206500)

* Fri Sep 15 2006 Soren Sandmann <sandmann@redhat.com>
- Add patch to only accept button 1 for close/minimize/maximize (bug 201628)

* Fri Sep 15 2006 Soren Sandmann <sandmann@redhat.com>
- Add patch to fix thumbnail sorting (bug 201605)

* Thu Sep 14 2006 Soren Sandmann <sandmann@redhat.com>
- Add patch to fix double clicking (bug 201783).

* Tue Sep 12 2006 Soren Sandmann <sandmann@redhat.com>
- Don't attempt to move the viewport when dx = dy = 0.(last bit of 206088).

* Tue Sep 12 2006 Soren Sandmann <sandamnn@redhat.com>
- Fix plane.patch to draw correctly when no timeout is running. (206088).

* Wed Sep  6 2006 Kristian Høgsberg <krh@redhat.com>
- Update fbconfig-depth-fix.patch to also skip fbconfigs without
  corresponding visuals.

* Tue Sep 5 2006 Soren Sandmann <sandmann@redhat.com> - 0.0.13-0.25.20060817git.fc6
- Make number of vertical size configurable

* Tue Sep 5 2006 Soren Sandmann <sandmann@redhat.com> - 0.0.13-0.24.20060817git.fc6
- Fix vertical viewport support in the plane patch.

* Fri Sep 1 2006 Soren Sandmann <sandmann@redhat.com> - 0.0.13-0.23.20060817git.fc6
- Upgrade to 0.6.61 of the dialog

* Fri Sep 1 2006 Soren Sandmann <sandmann@redhat.com> - 0.0.13-0.22.20060817git.fc6
- Add libtool to BuildRequires

* Fri Sep 1 2006 Soren Sandmann <sandmann@redhat.com> - 0.0.13-0.22.20060817git.fc6
- Add automake and autoconf to BuildRequires 

* Fri Sep 1 2006 Soren Sandmann <sandmann@redhat.com> - 0.0.13-0.22.20060817git.fc6
- Add a patch to put viewports on a plane.

* Wed Aug 30 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13-0.21.20060817git.fc6
- Drop gl-include-inferiors.patch now that compiz uses COW and the X
  server evicts offscreen pixmaps automatically on
  GLX_EXT_texture_from_pixmap usage.

* Tue Aug 29 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13-0.20.20060817git.fc6
- Add cow.patch to make compiz use the composite overlay window.

* Fri Aug 25 2006 Soren Sandmann <sandmann@redhat.com> - 0.0.13-0.19-20060817git.fc6
- Rebase to desktop-effects 0.6.41

* Fri Aug 25 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13-0.18.20060817git.fc6
- Rebase to desktop-effects 0.6.19 and drop
  desktop-effects-0.6.1-delete-session.patch

* Tue Aug 22 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13-0.17.20060817git.fc6
- Add patch from upstream to also use sync protocol for override
  redirect windows (sync-override-redirect-windows.patch).

* Thu Aug 17 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13-0.16.20060817git.fc6
- Rebase to latest upstream changes which has the rest of the bindings
  rewrite.  Add resize-move-keybindings.patch to make move and resize
  bindings work like metacity.
- Add back scale plugin.

* Thu Aug 10 2006 Ray Strode <rstrode@redhat.com> 0.0.13-0.15.20060721git.fc5.aiglx
- Add Requires: gnome-session 2.15.90-2.fc6 (bug 201473)
- unlink session file on changing wms (bug 201473)

* Thu Aug  3 2006 Soren Sandmann <sandmann@redhat.com> 0.0.13-0.14.20060721git.fc5.aiglx
- Add Requires: gnome-session 2.15.4-3

* Wed Aug  3 2006 Soren Sandmann <sandmann@redhat.com> 0.0.13-0.13.20060721git.fc5.aiglx
- New version of dialog box. Macro the version number.

* Wed Aug  2 2006 Soren Sandmann <sandmann@redhat.com> 0.0.13-0.13.20060721git.fc5.aiglx
- Add 'desktop effects' dialog box.

* Mon Jul 31 2006 Kristian Høgsberg <krh@redhat.com> 0.0.13-0.12.20060721git.fc5.aiglx
- Add libwnck requires.

* Wed Jul 26 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13-0.11.20060721git.fc5.aiglx
- Bump and build for fc5 AIGLX repo.

* Wed Jul 26 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13-0.12.20060721git
- Fix gconf hooks.

* Tue Jul 25 2006 Kristian Høgsberg <krh@redhat.com>
- Require system-logos instead.

* Mon Jul 24 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13-0.10.20060721git
- Bump version to work around tagging weirdness.

* Mon Jul 24 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13-0.9.20060721git
- Add devel package and require redhat-logos instead of fedora-logos (#199757).

* Fri Jul 21 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13-0.8.20060720git
- Add workaround for AIGLX throttling problem.

* Thu Jul 20 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13-0.7.20060720git
- Drop scale plugin from snapshot.

* Tue Jul 18 2006 Matthias Clasen <mclasen@redhat.com> - 0.0.13-0.6.20060717git
- Don't build on s390

* Mon Jul 17 2006 Matthias Clasen <mclasen@redhat.com> - 0.0.13-0.5.20060717git
- Do some changes forced upon us by package review

* Thu Jul 13 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13-5.1
- Use sane numbering scheme.

* Fri Jul  7 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13.fedora1-4
- Drop the fullscreen hardcode patch and require X server that has
  GLX_MESA_copy_sub_buffer.

* Tue Jun 27 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13.fedora1-3
- Unbreak --replace.

* Thu Jun 15 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13.fedora1-2
- Add Requires, fix start-compiz.sh.

* Wed Jun 14 2006 Kristian Høgsberg <krh@redhat.com> - 0.0.13.fedora1-1
- Spec file for compiz, borrowing bits and pieces from Alphonse Van
  Assches spec file (#192432).
