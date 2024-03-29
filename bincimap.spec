Summary:	IMAP4rev1 server for Maildir
Summary(pl.UTF-8):	Serwer IMAP dla Maildirów
Name:		bincimap
Version:	1.2.12final
Release:	2
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://www.bincimap.org/dl/tarballs/1.2/%{name}-%{version}.tar.bz2
# Source0-md5:	ed40f8b5e560c0fd22fbbf346df1ee94
Source1:	%{name}.inetd
Source2:	%{name}-ssl.inetd
Source3:	%{name}.pam
URL:		http://www.bincimap.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	checkpassword-pam
Requires:	rc-inetd
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

%description -l pl.UTF-8
Binc IMAP to modularny serwer IMAP4rev1 dla Maildirów. Stara się być
stabilnym, szybkim, elastycznym i zgodnym z RFC. Został zaprojektowany
tak, aby być przyjaznym dla użytkowników qmail-pop3d, do
uwierzytelniania używa checkpassword i jest bardzo prosty do
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

touch $RPM_BUILD_ROOT/etc/security/blacklist.imap

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q rc-inetd reload

%postun
if [ "$1" = 0 ]; then
	%service -q rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/bincimap
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/bincimap-ssl
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/bincimap
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/blacklist.imap
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man[15]/*
