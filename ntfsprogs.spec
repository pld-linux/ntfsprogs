Summary:	NTFS filesystem libraries and utilities
Summary(pl):	Narzêdzia i biblioteki do obs³ugi systemu plików NTFS
Name:		ntfsprogs
Version:	1.7.1
%define	docver	0.4
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/linux-ntfs/%{name}-%{version}.tar.gz
Source1:	http://dl.sourceforge.net/linux-ntfs/ntfsdoc-%{docver}.tar.bz2
Patch0:		%{name}-noc++.patch
URL:		http://linux-ntfs.sf.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gcc >= 3.1
BuildRequires:	libtool
Obsoletes:	linux-ntfs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Linux-NTFS project (http://linux-ntfs.sf.net/) aims to bring full
support for the NTFS filesystem to the Linux operating system.
Linux-NTFS currently consists of a library and utilities. This package
contains the following utilities:

- ntfsfix - attempt to fix an NTFS partition that has been damaged by
  the Linux NTFS driver. It should be run every time after you have
  used the Linux NTFS driver to write to an NTFS partition to prevent
  massive data corruption from happening when Windows mounts the
  partition. IMPORTANT: Run this only *after* unmounting the partition
  in Linux but *before* rebooting into Windows NT/2000!
- mkntfs - format a partition with the NTFS filesystem.
- ntfslabel - display/change the label of an NTFS partition.
- ntfsundelete - recover deleted files from an NTFS volume.
- ntfsresize - resize an NTFS volume.

You can find more information about these utilities in their manuals.

%description -l pl
Projekt Linux-NTFS ma na celu pe³n± obs³ugê NTFS pod Linuksem.
Aktualnie sk³ada siê z biblioteki i narzêdzi. Pakiet zawiera
nastêpuj±ce narzêdzia:

- ntfsfix - próbuje naprawiaæ partycjê NTFS uszkodzone przez linuksowy
driver do NTFS. Powinien byæ uruchamiany po ka¿dym zapisie na partycji
NTFS, aby zapobiec masowemu zniszczeniu danych. WA¯NE: uruchamiaj ten
program tylko *po* odmontowaniu partycji pod Linuksem, ale *przed*
uruchomieniem Windows NT/2000!

- mkntfs - "formatuje" partycjê NTFS. Szczegó³y w manualu.

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

%prep
%setup -q -a1
%patch -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make}  install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf "$RPM_BUILD_ROOT"

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS ChangeLog NEWS README TODO*
%attr(755,root,root) %{_bindir}/ntfsfix
%attr(755,root,root) %{_bindir}/ntfsinfo
%attr(755,root,root) %{_sbindir}/mkntfs
%attr(755,root,root) %{_sbindir}/ntfslabel
%attr(755,root,root) %{_sbindir}/ntfsresize
%attr(755,root,root) %{_sbindir}/ntfsundelete
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{_mandir}/man8/mkntfs.8*
%{_mandir}/man8/ntfs*

%files devel
%defattr(644,root,root,755)
%doc ntfsdoc doc/{attribute_definitions,tunable_settings,*.txt}
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/*.la
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
