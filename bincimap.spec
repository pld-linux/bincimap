Summary:	IMAP4rev1 server for Maildir
Summary(pl):	Serwer IMAP dla Maildirów
Name:		bincimap
Version:	1.2.8final
Release:	1
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://www.bincimap.org/dl/tarballs/1.2/%{name}-%{version}.tar.bz2
# Source0-md5:	1369d3c7d96491568b1261d8c9984794
Source1:	%{name}.inetd
Source2:	%{name}-ssl.inetd
Source3:	%{name}.pam
URL:		http://www.bincimap.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	openssl-devel >= 0.9.7d
PreReq:		rc-inetd
Requires:	checkpassword-pam
Conflicts:	courier-imap
Conflicts:	cyrus-imapd
Conflicts:	imap
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_bindir		%{_sbindir}

%description
Binc IMAP is a modular IMAP4rev1 server for Maildir. It strives to be
stable, fast, flexible, and RFC compliant. It is designed to be
familiar for qmail-pop3d users, uses checkpassword to authenticate,
and it is very easy to set up.

%description -l pl
Binc IMAP to modularny serwer IMAP4rev1 dla Maildirów. Stara siê byæ
stabilnym, szybkim, elastycznym i zgodnym z RFC. Zosta³ zaprojektowany
tak, aby byæ przyjaznym dla u¿ytkowników qmail-pop3d, do
uwierzytelniania u¿ywa checkpassword i jest bardzo prosty do
skonfigurowania.

%prep
%setup -q

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd
install -d $RPM_BUILD_ROOT/etc/pam.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/bincimap
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/bincimap-ssl
install %{SOURCE3} $RPM_BUILD_ROOT/etc/pam.d/bincimap

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%config(noreplace) %verify(not size mtime md5) /etc/%{name}.conf
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/rc-inetd/bincimap
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/rc-inetd/bincimap-ssl
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/pam.d/bincimap
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man[15]/*
