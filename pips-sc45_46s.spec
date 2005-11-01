Summary:	Stylus C45/C46 Series Photo Image Print System
Summary(pl):	System druku fotograficznego dla serii drukarek Stylus C45/C46
Name:		pips-sc45_46s
Version:	2.6.2
Release:	2
License:	Mixed (GPL, LGPL, distributable)
Group:		Applications/Printing
Source0:	http://lx2.avasys.jp/pips/sc45_46/%{name}-%{version}.tar.gz
# Source0-md5:	0cac5222dcd5dd7a7a4f75848e23a92e
Source1:	%{name}-ekpd.init
Patch0:		%{name}-amfix.patch
Patch1:		%{name}-dyn_ltdl.patch
Patch2:		%{name}-compat-libstdc++.patch
Patch3:		%{name}-ekpd-permissions.patch
Patch4:		%{name}-services.patch
Patch5:		%{name}-init.patch
URL:		http://www.avasys.jp/english/linux_e/dl_ink.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	compat-libstdc++-2.10
BuildRequires:	cups-devel
BuildRequires:	gettext-devel
BuildRequires:	gtk+-devel >= 0.99.7
BuildRequires:	libltdl-devel
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.174
BuildRequires:	sed >= 4.0
Requires:	ghostscript
Requires(post,preun):	/sbin/chkconfig
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pipedir	%{_var}/run/ekpd
%define		_kowadir	%{_libdir}/EPKowa

%description
This software is a printer driver (filter) for high quality print
with EPSON Stylus C45 and C46 color ink jet printers.

%description -l pl
Sterownik drukarki (filtr) dla wysokojako¶ciowego wydruku na
kolorowych drukarkach atramentowych EPSON Stylus C45 i C46.

%package cups
Summary:	Cups binding of Stylus C45/C46 print system
Summary(pl):	Dowi±zania systemu druku Stylus C45/C46 dla cupsa
Group:		Applications/Printing
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description cups
Cups binding of Stylus C45/C46 print system.

%description cups -l pl
Dowi±zania systemu druku Stylus C45/C46 dla cupsa.

%prep
%setup -q
%patch0 -p1
# belongs with patch0
cp src/str{,_lib}.c
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
sed -i 's,/usr/local/EPKowa,%{_kowadir},' setup/* src/filter.tmp doc/* configure.in
sed -i 's,/var/ekpd,%{_pipedir},' src/filter.tmp src/ekplp.c ekpd/*.* {setup,doc}/*

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_sbindir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ekpd
:> $RPM_BUILD_ROOT%{_sysconfdir}/pipsrc
mv $RPM_BUILD_ROOT%{_kowadir}/printer/ekpd $RPM_BUILD_ROOT%{_sbindir}

rm -rf $RPM_BUILD_ROOT%{_kowadir}/SC45_46S/{ekpd.*,*readme*,rc.d,inst-rc_d.sh}
# useless without public headers
rm -f $RPM_BUILD_ROOT%{_libdir}/libsc45_46s.so
# doesn't do anything this RPM doesn't
rm -f $RPM_BUILD_ROOT%{_kowadir}/SC45_46S/scripts/inst-cups-post.sh

mv -f $RPM_BUILD_ROOT%{_datadir}/locale/zh{,_CN}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ekpd
if [ -f /var/lock/subsys/ekpd ]; then
	/etc/rc.d/init.d/ekpd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/ekpd start\" to start EPSON KOWA Printer Daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/ekpd ]; then
		/etc/rc.d/init.d/ekpd stop 1>&2
	fi
	/sbin/chkconfig --del ekpd
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog COPYING*
%doc doc/readme-sc45_46s
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*rc
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/ekpd
%attr(754,root,root) /etc/rc.d/init.d/ekpd
%dir %attr(770,root,lp) %{_pipedir}
%attr(600,lp,lp) %{_pipedir}/*
%dir %{_kowadir}
%dir %{_kowadir}/printer
%attr(755,root,root) %{_kowadir}/printer/dtrfilter
%attr(755,root,root) %{_kowadir}/printer/freset
%attr(755,root,root) %{_kowadir}/printer/gsconfig
%{_kowadir}/printer/paper_list.csv
%dir %{_kowadir}/SC45_46S
%attr(755,root,root) %{_kowadir}/SC45_46S/filter-sc45_46s
%{_kowadir}/SC45_46S/lang
%{_kowadir}/SC45_46S/cupsopt.csv
%{_kowadir}/SC45_46S/BID.PRN
%dir %{_kowadir}/SC45_46S/scripts
%{_kowadir}/SC45_46S/scripts/*.lc
%attr(755,root,root) %{_kowadir}/SC45_46S/scripts/setup-lpr.sh
%attr(755,root,root) %{_kowadir}/SC45_46S/scripts/inst-lpr-post.sh

%files cups
%defattr(644,root,root,755)
%doc doc/readme-sc45_46s-cups
%attr(755,root,root) %{_libdir}/cups/backend/*
%attr(755,root,root) %{_libdir}/cups/filter/*
%{_datadir}/cups/model/*
%attr(755,root,root) %{_kowadir}/SC45_46S/scripts/setup-cups.sh
