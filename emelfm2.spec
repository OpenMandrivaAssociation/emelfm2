%define name    emelfm2
%define version 0.3.2
%define release %mkrel 1

#this is to allow easy relocation eg to /usr/local
%define prefix /usr
%define _bindir %{prefix}/bin
%define _libdir %{prefix}/lib

Name:      %{name}
Version:   %{version}
Release:   %{release}
Summary:   Gtk+2 file manager with two-panel format
Group:     File tools
License:   GPL
#URL:      http://emelfm2.org
URL:       http://emelfm2.net
Source:    %{name}-%{version}.tar.bz2
Patch0:    emelfm2_change_config.diff
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Requires:        gtk+2.0 >= 2.4 file findutils >= 4.2 grep sed
Requires:        libgamin-1_0 >= 0.1
BuildRequires:   gtk+2-devel
BuildRequires:   gcc >= 3.2
BuildRequires:   gamin-devel >= 0.1
BuildRequires:   desktop-file-utils

%description
emelFM2 is a file manager with the efficient two-panel format,
featuring:
  o Simple interface
  o Bookmarks and history lists 
  o Flexible filetyping scheme
  o Multiple actions selectable for each filetype 
  o Filename, size, and date Filters
  o Built-in command line
  o Configurable keyboard bindings
  o Configurable toolbars
  o Runtime loadable plugins

It is the Gtk+2 port of emelFM. 

Note: EmelFM2 and EmelFM are parallel installable

%package   i18n
Summary:   Translation files for emelFM2
Group:     File tools
Requires:  %{name} = %{version}

%description i18n
This package contains a translation files which may be installed
to allow emelFM2 to use non-english names in its user-interface

%prep
%setup -q
%patch0 -p0

%build

%ifarch x86_64
%make PREFIX=%{prefix} DOCS_VERSION=1 USE_GAMIN=1 CFLAGS="-O2"
%else
%make PREFIX=%{prefix} DOCS_VERSION=1 USE_GAMIN=1 CFLAGS="-O2 -march=i586"
%endif


%install
rm -rf $RPM_BUILD_ROOT
%make install PREFIX=%{buildroot}%{prefix}

mkdir -p %{buildroot}%{_bindir}
install -m 755 %{name} %{buildroot}%{_bindir}

%make install_i18n PREFIX=%{buildroot}%{prefix}

# remove unnecessary
rm -rf %{buildroot}/%{_datadir}/doc/emelfm2

%find_lang %{name}

# menu
mkdir -p %{buildroot}{%{_miconsdir},%{_iconsdir},%{_liconsdir},%{_menudir}}
install -m 644 icons/emelfm2_48.png %{buildroot}%{_liconsdir}/%{name}.png
install -m 644 icons/emelfm2_32.png %{buildroot}%{_iconsdir}/%{name}.png
install -m 644 icons/emelfm2_24.png %{buildroot}%{_miconsdir}/%{name}.png

cat > %{buildroot}%{_menudir}/%{name} << EOF
?package(%{name}):\
command="%{name}"\
title="Emelfm2"\
longtitle="Gtk+2 file manager"\
needs="x11"\
icon="%{name}.png"\
section="System/File Tools" \
xdg="true"
EOF

desktop-file-install --vendor="" \
--add-category="X-MandrivaLinux-System-FileTools" \
--dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/* 

%find_lang %{name}

%post
%{update_menus}

%postun
%{clean_menus}

%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(644,root,root,755)
%doc docs/ACTIONS docs/CONFIGURATION docs/CREDITS
%doc docs/GPL docs/HACKING docs/INSTALL docs/README docs/TODO docs/USAGE
%doc docs/WARNING
%defattr (-,root,root)
%{_bindir}/*
%{prefix}/share/pixmaps/*
%{prefix}/share/applications/*
%{prefix}/share/application-registry/*
%dir %_libdir/%{name}
%dir %_libdir/%{name}/plugins
%{_libdir}/%{name}/plugins/e2p*.so
%{_menudir}/%{name}
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_mandir}/man1/* 


