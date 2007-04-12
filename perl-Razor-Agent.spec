# copied from 9.2 mdk rpm macros
%define mdkversion             %(perl -pe '/(\\d+)\\.(\\d)\\.?(\\d)?/; $_="$1$2".($3||0)' /etc/mandrake-release)
%define pkgname razor-agents

%if %{mdkversion} < 920 
%define perl_sitelib %(echo %{perl_sitearch} |sed 's/i386-linux//')
%endif


Name:		perl-Razor-Agent
Version: 2.82
Release: %mkrel 1
Summary:	Use a Razor catalogue server to filter spam messages
Source0:	http://prdownloads.sourceforge.net/razor/%{pkgname}-%{version}.tar.bz2
Requires:	perl-Net-DNS
%if %{mdkversion} < 920
Requires:	perl
Requires:	perl-Digest-SHA1
Requires:	perl-MailTools
Requires:	perl-Time-HiRes
Requires:	perl-URI
Requires:	perl-MIME-Base64
%endif
License:	Artistic
Group:		Networking/Mail
URL:		http://razor.sourceforge.net
BuildRoot:	%{_tmppath}/%{name}-%{version}-builroot
BuildRequires:	perl-devel
BuildRequires:	perl-Net-DNS
BuildRequires:	perl-Digest-SHA1
BuildRequires:	perl-MailTools
BuildRequires:	perl-Time-HiRes
BuildRequires:	perl-URI
BuildRequires:	perl-MIME-Base64

%description
Vipul's Razor is a distributed, collaborative, spam detection and
filtering network.  Razor establishes a distributed and constantly
updating catalogue of spam in propagation.  This catalogue is used by
clients to filter out known spam.  On receiving a spam, a Razor
Reporting Agent (run by an end-user or a troll box) calculates and
submits a 20-character unique identification of the spam (a SHA
Digest) to its closest Razor Catalogue Server.  The Catalogue Server
echos this signature to other trusted servers after storing it in its
database.  Prior to manual processing or transport-level reception,
Razor Filtering Agents (end-users and MTAs) check their incoming mail
against a Catalogue Server and filter out or deny transport in case of
a signature match.  Catalogued spam, once identified and reported by a
Reporting Agent, can be blocked out by the rest of the Filtering
Agents on the network.

%prep

%setup -q -n %{pkgname}-%{version}

%build

%if %mdkversion == 800
  %{__perl} Makefile.PL INSTALLDIRS=site
%else
  %{__perl} Makefile.PL INSTALLDIRS=vendor
%endif

cd Razor2-Preproc-deHTMLxs

%if %mdkversion == 800
  %{__perl} Makefile.PL INSTALLDIRS=site
%else
  %{__perl} Makefile.PL INSTALLDIRS=vendor
%endif

cd ..
%make OPTIMIZE="$RPM_OPT_FLAGS" 

%install
rm -rf $RPM_BUILD_ROOT
cd Razor2-Preproc-deHTMLxs
%if %mdkversion == 800
%makeinstall PREFIX=$RPM_BUILD_ROOT%{_prefix}
%else
%makeinstall_std
%endif
cd ..

%if %mdkversion == 800
export PERL5LIB="$RPM_BUILD_ROOT%{perl_sitearch}"
%else
export PERL5LIB="$RPM_BUILD_ROOT%{perl_vendorarch}" 
%endif

%if %mdkversion == 800
%makeinstall PREFIX=$RPM_BUILD_ROOT%{_prefix}
%else
%makeinstall_std INSTALLMAN5DIR=%{_mandir}/man5
%endif

%if %mdkversion == 800
  for nb in 1 3 5; do
     install -d $RPM_BUILD_ROOT%{_mandir}/man${nb}
     install -m 644 blib/man${nb}/* $RPM_BUILD_ROOT%{_mandir}/man${nb}
  done
%else
  install -d $RPM_BUILD_ROOT%{_mandir}/man5
  install -m 644 blib/man5/* $RPM_BUILD_ROOT%{_mandir}/man5
%endif

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, root)
%doc INSTALL FAQ README Changes CREDITS
%{_bindir}/*
%if %mdkversion == 800
%{perl_sitelib}/Razor2
%{perl_sitelib}/auto/Razor2
%{perl_sitearch}/Razor2
%{perl_sitearch}/auto/Razor2
%else
%{perl_vendorlib}/Razor2
%{perl_vendorlib}/auto/Razor2
%{perl_vendorarch}/Razor2
%{perl_vendorarch}/auto/Razor2
%endif
%{_datadir}/man/*/*

