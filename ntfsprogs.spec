#
# Conditional build:
%bcond_without	crypto		# don't build crypto support
%bcond_without	gnome		# don't build gnome-vfs2 module
%bcond_without	fuse		# don't build ntfsmount utility
#
%define	docver	0.5
Summary:	NTFS filesystem libraries and utilities
Summary(pl.UTF-8):	Narzędzia i biblioteki do obsługi systemu plików NTFS
Name:		ntfsprogs
Version:	2.0.0
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/linux-ntfs/%{name}-%{version}.tar.bz2
# Source0-md5:	2b39dece8897bc748f4ab4c40ec7699e
Source1:	http://dl.sourceforge.net/linux-ntfs/ntfsdoc-%{docver}.tar.bz2
# Source1-md5:	d713836df621686785c3230e5788c689
Patch0:		%{name}-pkgconfig.patch
Patch1:		%{name}-stdarg_h-required.patch
Patch2:		%{name}-va.patch
URL:		http://www.linux-ntfs.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gcc >= 5:3.1
%{?with_gnome:BuildRequires:	gnome-vfs2-devel >= 2.0}
%{?with_crypto:BuildRequires:	gnutls-devel >= 1.2.8}
%{?with_fuse:BuildRequires:	libfuse-devel >= 2.3.0}
%{?with_crypto:BuildRequires:	libgcrypt-devel >= 1.2.0}
BuildRequires:	libconfig-devel >= 1.1.3
BuildRequires:	libtool >= 1:1.4.2-9
BuildRequires:	pkgconfig
Obsoletes:	linux-ntfs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Linux-NTFS project (http://linux-ntfs.sf.net/) aims to bring full
support for the NTFS filesystem to the Linux operating system.
Linux-NTFS currently consists of a library and utilities. This package
contains the following utilities:

- ntfsfix - attempt to fix an NTFS partition that has been damaged by
  the Linux NTFS driver. It should be run every time after you have used
  the Linux NTFS driver to write to an NTFS partition to prevent massive
  data corruption from happening when Windows mounts the partition.
  IMPORTANT: Run this only *after* unmounting the partition in Linux but
  *before* rebooting into Windows NT/2000!,
- mkntfs - create partition with the NTFS filesystem,
- ntfslabel - display/change the label of an NTFS partition,
- ntfsundelete - recover deleted files from an NTFS volume,
- ntfsresize - resize an NTFS volume,
- ntfsclone - clone, image, restore or rescue NTFS,
- ntfswipe - wipe junk from unused space,
- ntfsdecrypt - descrypt $EFS-encrypted files.

You can find more information about these utilities in their manuals.

%description -l pl.UTF-8
Projekt Linux-NTFS ma na celu dostarczyć pełną obsługę NTFS pod
Linuksem. Aktualnie składa się z biblioteki i narzędzi. Pakiet zawiera
następujące narzędzia:

- ntfsfix - próbuje naprawiać partycję NTFS uszkodzone przez linuksowy
  sterownik do NTFS. Powinien być uruchamiany po każdym zapisie na
  partycji NTFS, aby zapobiec masowemu zniszczeniu danych. WAŻNE: należy
  uruchamiać ten program tylko *po* odmontowaniu partycji pod Linuksem,
  ale *przed* uruchomieniem Windows NT/2000!
- mkntfs - "formatuje" partycję NTFS.
- ntfslabel - wyświetla/zmienia etykietę partycji NTFS.
- ntfsundelete - odzyskuje usunięte pliki z wolumenu NTFS.
- ntfsresize - zmienia rozmiar wolumenu NTFS.
- ntfsclone
- ntfswipe
- ntfsdecrypt

Więcej informacji na temat tych narzędzi można znaleźć w manualach.

%package devel
Summary:	Files required to compile software that uses libntfs
Summary(pl.UTF-8):	Pliki potrzebne do kompilowania programów korzystających z libntfs
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	linux-ntfs-devel

%description devel
This package includes the header files needed to link software with
libntfs.

%description devel -l pl.UTF-8
Pliki nagłówkowe potrzebne do budowania programów korzystających z
libntfs.

%package static
Summary:	Static version of libntfs
Summary(pl.UTF-8):	Statyczna wersja libntfs
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	linux-ntfs-static

%description static
This package contains the static version of libntfs library.

%description static -l pl.UTF-8
Ten pakiet zawiera statyczną wersję biblioteki libntfs.

%package fuse
Summary:	NTFS FUSE module (ntfsmount)
Summary(pl.UTF-8):	Moduł FUSE dla NTFS (ntfsmount)
Group:		Base/Utilities
Requires:	%{name} = %{version}-%{release}

%description fuse
This package contains the ntfsmount utility which is an NTFS
filesystem in userspace (FUSE) module allowing users to mount an NTFS
filesystem from userspace and accessing it using the functionality
provided by the NTFS library (libntfs).

%description fuse -l pl.UTF-8
Pakiet zawiera narzędzie ntfmount, które jest modułem FUSE
pozwalającym użytkownikom na dostęp do systemu plików NTFS w
przestrzeni użytkownika wykorzystując funkcjonalność biblioteki
libntfs.

%package -n gnome-vfs2-module-ntfs
Summary:	NTFS module for gnome-vfs
Summary(pl.UTF-8):	Moduł NTFS dla gnome-vfs
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description -n gnome-vfs2-module-ntfs
NTFS module for gnome-vfs.

%description -n gnome-vfs2-module-ntfs -l pl.UTF-8
Moduł NTFS dla gnome-vfs.

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1
#%patch2 -p1

%if !%{with crypto}
echo 'AC_DEFUN([AM_PATH_LIBGCRYPT],[:])' > fake-am_path_libgcrypt.m4
echo 'AC_DEFUN([AM_PATH_LIBGNUTLS],[:])' > fake-am_path_libgnutls.m4
%endif

%build
%{__libtoolize}
%{__aclocal} -I .
%{__autoconf}
%{__autoheader}
%{__automake}

# -fms-extensions needed to compile typedefed unnamed structs with gcc 3.3
CFLAGS="%{rpmcflags} -fms-extensions"
%configure \
	--%{?with_fuse:en}%{!?with_fuse:dis}able-fuse-module \
	--%{?with_gnome:en}%{!?with_gnome:dis}able-gnome-vfs \
	--%{?with_crypto:en}%{!?with_crypto:dis}able-crypto

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make}  install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/gnome-vfs-2.0/modules/lib*.{la,a}
# instead of symlinks
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/{mkfs.ntfs,mount.ntfs-fuse}.8
echo '.so mkntfs.8' > $RPM_BUILD_ROOT%{_mandir}/man8/mkfs.ntfs.8
echo '.so ntfsmount.8' > $RPM_BUILD_ROOT%{_mandir}/man8/mount.ntfs-fuse.8

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS ChangeLog NEWS README TODO*
%attr(755,root,root) %{_bindir}/ntfsfix
%attr(755,root,root) %{_bindir}/ntfsinfo
%attr(755,root,root) %{_bindir}/ntfscat
%attr(755,root,root) %{_bindir}/ntfscluster
%attr(755,root,root) %{_bindir}/ntfscmp
%attr(755,root,root) %{_bindir}/ntfsls
%attr(755,root,root) %{_sbindir}/mkntfs
%attr(755,root,root) %{_sbindir}/ntfsclone
%attr(755,root,root) %{_sbindir}/ntfscp
%attr(755,root,root) %{_sbindir}/ntfslabel
%attr(755,root,root) %{_sbindir}/ntfsresize
%attr(755,root,root) %{_sbindir}/ntfsundelete
%attr(755,root,root) /sbin/mkfs.ntfs
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_mandir}/man8/mkfs.ntfs.8*
%{_mandir}/man8/mkntfs.8*
%{_mandir}/man8/ntfs[!m][!o]*.8*

%files devel
%defattr(644,root,root,755)
%doc ntfsdoc-*/* doc/{attribute_definitions,tunable_settings,*.txt}
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/*.la
%{_includedir}/*
%{_mandir}/man8/libntfs.8*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%if %{with fuse}
%files fuse
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ntfsmount
%attr(755,root,root) /sbin/mount.ntfs-fuse
%{_mandir}/man8/mount.ntfs-fuse.8*
%{_mandir}/man8/ntfsmount.8*
%endif

%if %{with gnome}
%files -n gnome-vfs2-module-ntfs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gnome-vfs-2.0/modules/libntfs-gnomevfs.so*
%{_sysconfdir}/gnome-vfs-2.0/modules/libntfs.conf
%{_mandir}/man8/libntfs-gnomevfs.8*
%endif
