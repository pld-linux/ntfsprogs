Summary: 	NTFS filesystem libraries and utilities
Name:		ntfsprogs
Version:	1.7.1
Release:	0.1
License:	GPL
Group:		System Environment/Base
Source:		http://prdownloads.sf.net/linux-ntfs/ntfsprogs-%{version}.tar.gz
BuildRequires:	gcc >= 3.1
Requires:	libgcc >= 3.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Linux-NTFS project (http://linux-ntfs.sf.net/) aims to bring full support
for the NTFS filesystem to the Linux operating system. Linux-NTFS currently
consists of a static library and utilities. This package contains the following
utilities:
	NtfsFix - Attempt to fix an NTFS partition that has been damaged by the
Linux NTFS driver. It should be run every time after you have used the Linux
NTFS driver to write to an NTFS partition to prevent massive data corruption
from happening when Windows mounts the partition.
IMPORTANT: Run this only *after* unmounting the partition in Linux but *before*
rebooting into Windows NT/2000! See man 8 ntfsfix for details.
	mkntfs - Format a partition with the NTFS filesystem. See man 8 mkntfs
for command line options.
	ntfslabel - Display/change the label of an NTFS partition. See man 8
ntfslabel for details.
	ntfsundelete - Recover deleted files from an NTFS volume.  See man 8
ntfsundelete for details.
	ntfsresize - Resize an NTFS volume. See man 8 ntfsresize for details.

%package devel
Summary		: files required to compile software that uses libntfs
Group		: Development/System
Requires	: ntfsprogs = %{version}-%{release}

%description devel
This package includes the header files and libraries needed to link software
with libntfs.

%prep
%setup -q

%build
./configure \
	--prefix=%{_prefix} \
	--mandir=%{_mandir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make}  install-strip \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf "$RPM_BUILD_ROOT"

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING CREDITS ChangeLog INSTALL NEWS README TODO.include TODO.libntfs TODO.ntfsprogs doc/CodingStyle doc/attribute_definitions doc/attributes.txt doc/compression.txt doc/tunable_settings doc/template.c doc/template.h doc/system_files.txt doc/system_security_descriptors.txt
%attr(0755,root,root) %{_bindir}/ntfsfix
%attr(0755,root,root) %{_bindir}/ntfsinfo
%attr(0755,root,root) %{_sbindir}/mkntfs
%attr(0755,root,root) %{_sbindir}/ntfslabel
%attr(0755,root,root) %{_sbindir}/ntfsresize
%attr(0755,root,root) %{_sbindir}/ntfsundelete
%{_mandir}/man8/mkntfs.8*
%{_mandir}/man8/ntfs*
%attr(755,root,root) %{_libdir}/lib*.so*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
%attr(644,root,root) %{_libdir}/lib*.a
%{_libdir}/*.la*
