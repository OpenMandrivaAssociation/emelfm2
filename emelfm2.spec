%define name    emelfm2
%define version 0.8.1
%define release 3

Name:      %{name}
Version:   %{version}
Release:   %{release}
Summary:   GTK+ 2 file manager with two-panel format
Group:     File tools
License:   GPLv3+ and LGPLv3+
URL:       http://emelfm2.net
Source0:   http://emelfm2.net/rel/%{name}-%{version}.tar.bz2
BuildRequires:	gtk+3-devel
BuildRequires:	polkit-1-devel
BuildRequires:	desktop-file-utils
BuildRequires:	magic-devel
BuildRequires:	acl-devel
BuildRequires:	pkgconfig(udev)
Obsoletes:	%{name}-i18n

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

It is the GTK+ 2 port of emelFM.

Note: EmelFM2 and EmelFM are parallel installable

%prep
%setup -q -n %{name}-%{version}

%build
sed -i Makefile -e 's:dbus-glib-1::' || die

%make OPTIMIZE="${RPM_OPT_FLAGS}" \
        CFLAGS="${RPM_OPT_FLAGS}" \
        USE_INOTIFY=1 \
	GTK3=1	\
	WITH_POLKIT=1 \
	WITH_DEVKIT=1 \
	WITH_ACL=1	\
        USE_LATEST=1 \
        PREFIX="%{_prefix}" \
        WITH_THUMBS=1 \
        WITH_TRACKER=1 \
        WITH_CUSTOMMOUSE=1 \
        WITH_HAL=0 \
        EDITOR_SPELLCHECK=0 \
        PREFIX="%{_prefix}"

%install
make install PREFIX=%{buildroot}%{_prefix}
make install_i18n PREFIX=%{buildroot}%{_prefix}

#mkdir -p %{buildroot}%{_bindir}
#install -m 755 %{name} %{buildroot}%{_bindir}

# remove unnecessary
rm -rf %{buildroot}/%{_docdir}/*

# icons
install -m 644 -D icons/emelfm2_48.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
install -m 644 -D icons/emelfm2_32.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m 644 -D icons/emelfm2_24.png %{buildroot}%{_iconsdir}/hicolor/24x24/apps/%{name}.png

# menu
perl -pi -e 's,Icon=emelfm2/emelfm2_48.png,Icon=%{name},g' %{buildroot}%{_datadir}/applications/*
desktop-file-install --vendor="" \
  --add-category="System" \
  --add-category="Utility" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

%find_lang %{name}

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc docs/ACTIONS docs/CONFIGURATION docs/CREDITS
%doc docs/HACKING docs/README docs/TODO docs/USAGE
%doc docs/WARNING
%defattr (-,root,root)
%{_bindir}/*
%{_datadir}/pixmaps/*
%{_datadir}/applications/*
%{_datadir}/application-registry/*
%{_prefix}/lib/%{name}
%{_iconsdir}/hicolor/48x48/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/24x24/apps/%{name}.png
%{_mandir}/man1/*
