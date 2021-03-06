%define enginedir /usr/clearos/sandbox/

Name: webconfig-utils
Version: 6.1.1
Release: 1%dist
Group: Applications/Modules
Summary: Web-based administration tool core
Source: %{name}-%{version}.tar.gz
Requires: webconfig-php
Requires(post): initscripts
BuildRequires: webconfig-php-devel
Obsoletes: cc-webconfig-engine
License: GPL
BuildRoot: /tmp/%{name}-%{version}-build

%description
Web-based administration tool core

%prep
%setup -q
%build
rm -rf $RPM_BUILD_ROOT

cd php-ifconfig
%configure \
	--prefix=%{enginedir} \
	--with-php-config=%{enginedir}%{_bindir}/php-config \
	--enable-ifconfig
make

cd ../php-statvfs
%configure \
	--prefix=%{enginedir} \
	--with-php-config=%{enginedir}%{_bindir}/php-config \
	--enable-statvfs
make

%install
mkdir -p -m 755 $RPM_BUILD_ROOT%{enginedir}%{_libdir}/php/modules
mkdir -p -m 755 $RPM_BUILD_ROOT%{enginedir}%{_sysconfdir}/php.d

# ifconfig PHP module
cp php-ifconfig/modules/ifconfig.so $RPM_BUILD_ROOT%{enginedir}%{_libdir}/php/modules
echo "extension=ifconfig.so" > $RPM_BUILD_ROOT%{enginedir}%{_sysconfdir}/php.d/ifconfig.ini

# statvfs PHP module
cp php-statvfs/modules/statvfs.so $RPM_BUILD_ROOT%{enginedir}%{_libdir}/php/modules
echo "extension=statvfs.so" > $RPM_BUILD_ROOT%{enginedir}%{_sysconfdir}/php.d/statvfs.ini

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{enginedir}%{_libdir}/php/modules/ifconfig.so
%{enginedir}%{_libdir}/php/modules/statvfs.so
%{enginedir}%{_sysconfdir}/php.d/ifconfig.ini
%{enginedir}%{_sysconfdir}/php.d/statvfs.ini
