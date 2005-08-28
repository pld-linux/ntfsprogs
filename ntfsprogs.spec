#
# Conditional build:
%bcond_without	gnome		# don't build gnome-vfs2 module
%bcond_without	fuse		# don't build ntfsmount utility
#
Summary:	NTFS filesystem libraries and utilities
Summary(pl):	Narzêdzia i biblioteki do obs³ugi systemu plików NTFS
Name:		ntfsprogs
Version:	1.11.2
%define	docver	0.5
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/linux-ntfs/%{name}-%{version}.tar.gz
# Source0-md5:	db39d930f581e55c9731718f08a5b6f0
Source1:	http://dl.sourceforge.net/linux-ntfs/ntfsdoc-%{docver}.tar.bz2
# Source1-md5:	d713836df621686785c3230e5788c689
Patch0:		%{name}-gcc33.patch
Patch1:		%{name}-pkgconfig.patch
URL:		http://linux-ntfs.sf.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gcc >= 3.1
%{?with_gnome:BuildRequires:	gnome-vfs2-devel >= 2.0}
%{?with_fuse:BuildRequires:	libfuse-devel >= 2.3.0}
BuildRequires:	libtool >= 1:1.4.2-9
%{?with_gnome:BuildRequires:	pkgconfig}
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
  *before* rebooting into Windows NT/2000!
- mkntfs - format a partition with the NTFS filesystem.
- ntfslabel - display/change the label of an NTFS partition.
- ntfsundelete - recover deleted files from an NTFS volume.
- ntfsresize - resize an NTFS volume.

You can find more information about these utilities in their manuals.

%description -l pl
Projekt Linux-NTFS ma na celu dostarczyæ pe³n± obs³ugê NTFS pod
Linuksem. Aktualnie sk³ada siê z biblioteki i narzêdzi. Pakiet zawiera
nastêpuj±ce narzêdzia:

- ntfsfix - próbuje naprawiaæ partycjê NTFS uszkodzone przez linuksowy
  sterownik do NTFS. Powinien byæ uruchamiany po ka¿dym zapisie na
  partycji NTFS, aby zapobiec masowemu zniszczeniu danych. WA¯NE:
  nale¿y uruchamiaæ ten program tylko *po* odmontowaniu partycji pod
  Linuksem, ale *przed* uruchomieniem Windows NT/2000!
- mkntfs - "formatuje" partycjê NTFS.
- ntfslabel - wy¶wietla/zmienia etykietê partycji NTFS.
- ntfsundelete - odzyskuje usuniête pliki z wolumenu NTFS.
- ntfsresize - zmienia rozmiar wolumenu NTFS.

Wiêcej informacji na temat tych narzêdzi mo¿na znale¼æ w manualach.

%package devel
Summary:	Files required to compile software that uses libntfs
Summary(pl):	Pliki potrzebne do kompilowania programów korzystaj±cych z libntfs
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	linux-ntfs-devel

%description devel
This package includes the header files needed to link software with
libntfs.

%description devel -l pl
Pliki nag³ówkowe potrzebne do budowania programów korzystaj±cych z
libntfs.

%package static
Summary:	Static version of libntfs
Summary(pl):	Statyczna wersja libntfs
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	linux-ntfs-static

%description static
This package contains the static version of libntfs library.

%description static -l pl
Ten pakiet zawiera statyczn± wersjê biblioteki libntfs.

%package fuse
Summary:	NTFS FUSE module (ntfsmount)
Summary(pl):	Modu³ FUSE dla NTFS (ntfsmount)
Group:		Base/Utilities
Requires:	%{name} = %{version}-%{release}

%description fuse
This package contains the ntfsmount utility which is an NTFS
filesystem in userspace (FUSE) module allowing users to mount an NTFS
filesystem from userspace and accessing it using the functionality
provided by the NTFS library (libntfs).

%description fuse -l pl
Pakiet zawiera narzêdzie ntfmount, które jest modu³em FUSE
pozwalaj±cym u¿ytkownikom na dostêp do systemu plików NTFS w
przestrzeni u¿ytkownika wykorzystuj±c funkcjonalno¶æ biblioteki
libntfs.

%package -n gnome-vfs2-module-ntfs
Summary:	NTFS module for gnome-vfs
Summary(pl):	Modu³ NTFS dla gnome-vfs
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description -n gnome-vfs2-module-ntfs
NTFS module for gnome-vfs.

%description -n gnome-vfs2-module-ntfs -l pl
Modu³ NTFS dla gnome-vfs.

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1

%build
echo 'AC_DEFUN([AM_PATH_LIBGCRYPT],[:])' > fake-am_path_libgcrypt.m4

%{__libtoolize}
%{__aclocal} -I .
%{__autoconf}
%{__autoheader}
%{__automake}

# -fms-extensions needed to compile typedefed unnamed structs with gcc 3.3
CFLAGS="%{rpmcflags} -fms-extensions"
%configure \
	--%{?with_fuse:en}%{!?with_fuse:dis}able-fuse-module \
	--%{?with_gnome:en}%{!?with_gnome:dis}able-gnome-vfs

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make}  install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/gnome-vfs-2.0/modules/lib*.{la,a}

%clean
rm -rf "$RPM_BUILD_ROOT"

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS ChangeLog NEWS README TODO*
%attr(755,root,root) %{_bindir}/ntfsfix
%attr(755,root,root) %{_bindir}/ntfsinfo
%attr(755,root,root) %{_bindir}/ntfscat
%attr(755,root,root) %{_bindir}/ntfscluster
%attr(755,root,root) %{_bindir}/ntfsls
%attr(755,root,root) %{_sbindir}/mkntfs
%attr(755,root,root) %{_sbindir}/ntfsclone
%attr(755,root,root) %{_sbindir}/ntfscp
%attr(755,root,root) %{_sbindir}/ntfslabel
%attr(755,root,root) %{_sbindir}/ntfsresize
%attr(755,root,root) %{_sbindir}/ntfsundelete
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_mandir}/man8/mkntfs.8*
%{_mandir}/man8/ntfs[!m][!o]*.8*

%files devel
%defattr(644,root,root,755)
%doc ntfsdoc-*/* doc/{attribute_definitions,tunable_settings,*.txt}
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/*.la
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%if %{with fuse}
%files fuse
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ntfsmount
%{_mandir}/man8/ntfsmount.8*
%endif

%if %{with gnome}
%files -n gnome-vfs2-module-ntfs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gnome-vfs-2.0/modules/libntfs-gnomevfs.so*
%{_sysconfdir}/gnome-vfs-2.0/modules/libntfs.conf
%{_mandir}/man8/libntfs-gnomevfs.8*
%endif
