#						-*- mode: rpm-spec -*-

%define		sha1 fc6b7773fc52f6104b66a9f86c18395f8a958848
%define		snapshot 20060721

Name:           compiz
Url:            http://www.freedesktop.org/Software/compiz
License:        X11/MIT/GPL
Group:          User Interface/Desktops
Version:        0.0.13
Release:        0.11.%{snapshot}git.fc5.aiglx

Summary:        OpenGL window and compositing manager
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# libdrm is not available on these arches
ExcludeArch:   	s390 s390x ppc64

Requires:	xorg-x11-server-Xorg >= 1.1.0-26
Requires:	mesa-libGL >= 6.5-9
Requires:       system-logos

BuildRequires:  libX11-devel, libdrm-devel, libwnck-devel
BuildRequires:  libXfixes-devel, libXrandr-devel, libXrender-devel
BuildRequires:  libXcomposite-devel, libXdamage-devel, libXext-devel
BuildRequires:  libXt-devel, libXmu-devel, libICE-devel, libSM-devel
BuildRequires:  gnome-desktop-devel, control-center-devel, GConf2-devel
BuildRequires:  gettext

Source0:        %{name}-%{sha1}.tar.bz2

Patch100: gl-include-inferiors.patch
Patch101: aiglx-defaults.patch
Patch102: tfp-server-extension.patch
Patch103: composite-cube-logo.patch
Patch104: fbconfig-depth-fix.patch
Patch105: fedora-logo.patch
Patch106: glfinish.patch


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
%setup -q -n %{name}-%{sha1}

%patch100 -p1 -b .gl-include-inferiors
%patch101 -p1 -b .aiglx-defaults
%patch102 -p1 -b .tfp-server-extension
%patch103 -p1 -b .composite-cube-logo
%patch104 -p1 -b .fbconfig-depth-fix
%patch105 -p1 -b .fedora-logo
%patch106 -p1 -b .glfinish

%build
%configure --disable-libsvg-cairo

make %{?_smp_mflags} 

%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make DESTDIR=$RPM_BUILD_ROOT install || exit 1
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} ';'

%post
export GCONF_CONFIG_SOURCE=`/usr/bin/gconftool-2 --get-default-source`
/usr/bin/gconftool-2 --makefile-install-rule \
	%{_sysconfdir}/gconf/schemas/compiz.schemas > /dev/null

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

%files devel
%defattr(-, root, root)
%{_libdir}/pkgconfig/compiz.pc
%{_includedir}/compiz

%changelog
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
