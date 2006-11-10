#						-*- mode: rpm-spec -*-

%define		dialogversion	0.6.163

Name:           compiz
Url:            http://www.freedesktop.org/Software/compiz
License:        X11/MIT/GPL
Group:          User Interface/Desktops
Version:        0.3.2
Release:        1%{?dist}

Summary:        OpenGL window and compositing manager
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# libdrm is not available on these arches
ExcludeArch:   	s390 s390x ppc64

Requires:	xorg-x11-server-Xorg >= 1.1.0-26
Requires:	mesa-libGL >= 6.5-9
Requires:	libwnck >= 2.15.4
Requires:       system-logos
Requires:	gnome-session >= 2.15.90-2.fc6

BuildRequires:  libX11-devel, libdrm-devel, libwnck-devel
BuildRequires:  libXfixes-devel, libXrandr-devel, libXrender-devel
BuildRequires:  libXcomposite-devel, libXdamage-devel, libXext-devel
BuildRequires:  libXt-devel, libXmu-devel, libICE-devel, libSM-devel
BuildRequires:  gnome-desktop-devel, control-center-devel, GConf2-devel
BuildRequires:  gettext autoconf automake libtool
BuildRequires:  desktop-file-utils
BuildRequires:  intltool >= 0.35

Source0:        %{name}-%{version}.tar.bz2
Source1:	desktop-effects-%{dialogversion}.tar.gz

# Patches that are not upstream
Patch101: aiglx-defaults.patch
Patch102: tfp-server-extension.patch
Patch103: composite-cube-logo.patch
#Patch104: fbconfig-depth-fix.patch
Patch105: fedora-logo.patch
Patch106: glfinish.patch
#Patch107: cow.patch
#Patch108: plane.patch
#Patch109: double-click.patch
#Patch110: thumbnail-sorting.patch
#Patch111: button-clicks.patch
#Patch112: positioning.patch
Patch113: resize-offset.patch
Patch114: restart.patch
Patch115: icon-menu.patch
Patch116: terminate-move.patch

%description
Compiz is one of the first OpenGL-accelerated compositing window
managers for the X Window System. The integration allows it to perform
compositing effects in window management, such as a minimization
effect and a cube workspace.  Compiz is an OpenGL compositing manager
that use Compiz use EXT_texture_from_pixmap OpenGL extension extension
for binding redirected top-level windows to texture objects.


%package devel
Summary: Development packages for compiz.
Group: Development/Libraries
Requires: compiz = %{PACKAGE_VERSION}

%description devel
The compiz-devel package includes the header files,
and developer docs for the compiz package.

Install compiz-devel if you want to develop plugins for the compiz
windows and compositing manager.

%prep
%setup -q -T -b1 -n desktop-effects-%{dialogversion}
%setup -q 

%patch101 -p1 -b .aiglx-defaults
%patch102 -p1 -b .tfp-server-extension
%patch103 -p1 -b .composite-cube-logo
#%patch104 -p1 -b .fbconfig-depth-fix
%patch105 -p1 -b .fedora-logo
%patch106 -p1 -b .glfinish
#%patch107 -p1 -b .cow
#%patch108 -p1 -b .plane
#%patch109 -p1 -b .double-click
#%patch110 -p1 -b .thumbnail-sorting
#%patch111 -p1 -b .button-clicks
#%patch112 -p1 -b .positioning
%patch113 -p1 -b .resize-offset
%patch114 -p1 -b .restart
%patch115 -p1 -b .icon-menu
%patch116 -p1 -b .terminate-move

%build
rm -rf $RPM_BUILD_ROOT

CPPFLAGS="$CPPFLAGS -I$RPM_BUILD_ROOT%{_includedir}"
export CPPFLAGS

autoreconf

%configure --disable-libsvg-cairo

make %{?_smp_mflags} 

# desktop-effects
cd ../desktop-effects-%{dialogversion}
%configure 
make


%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make DESTDIR=$RPM_BUILD_ROOT install || exit 1
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

echo INSTALLING DESKTOP EFFECTS
cd ../desktop-effects-%{dialogversion}
make DESTDIR=$RPM_BUILD_ROOT install || exit 1
desktop-file-install --vendor redhat --delete-original      \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications             \
  --add-category X-Red-Hat-Base                             \
  $RPM_BUILD_ROOT%{_datadir}/applications/desktop-effects.desktop

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} ';'

%post
update-desktop-database -q %{_datadir}/applications
export GCONF_CONFIG_SOURCE=`/usr/bin/gconftool-2 --get-default-source`
/usr/bin/gconftool-2 --makefile-install-rule \
	%{_sysconfdir}/gconf/schemas/compiz.schemas > /dev/null
touch %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
	/usr/bin/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor
fi

%preun
if [ "$1" -eq 0 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule \
	%{_sysconfdir}/gconf/schemas/compiz.schemas > /dev/null
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc AUTHORS ChangeLog COPYING* INSTALL README TODO
%{_bindir}/compiz
%{_bindir}/gnome-window-decorator
%{_libdir}/compiz/*.so
%{_libdir}/window-manager-settings/libcompiz.so
%{_sysconfdir}/gconf/schemas/compiz.schemas
%{_datadir}/compiz/*.png
%{_datadir}/gnome/wm-properties/compiz.desktop
%{_datadir}/locale/*/LC_MESSAGES/compiz.mo
%{_bindir}/desktop-effects
%{_datadir}/compiz/desktop-effects.glade
%{_datadir}/applications/redhat-desktop-effects.desktop
%{_datadir}/icons/hicolor/16x16/apps/desktop-effects.png
%{_datadir}/icons/hicolor/24x24/apps/desktop-effects.png
%{_datadir}/icons/hicolor/32x32/apps/desktop-effects.png
%{_datadir}/icons/hicolor/36x36/apps/desktop-effects.png
%{_datadir}/icons/hicolor/48x48/apps/desktop-effects.png
%{_datadir}/icons/hicolor/96x96/apps/desktop-effects.png

%files devel
%defattr(-, root, root)
%{_libdir}/pkgconfig/compiz.pc
%{_includedir}/compiz

%changelog
* Fri Nov 10 2006 Matthias Clasen <mclasen@redhat.com> - 0.3.2-1
- Update to 0.3.2
- Drop upstreamed patches

* Mon Oct 2 2006 Soren Sandmann <sandmann@redhat.ocm> - 0.0.13-0.32.20060818git.fc6
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
