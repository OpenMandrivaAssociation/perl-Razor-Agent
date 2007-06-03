%define pkgname razor-agents

Summary:	Use a Razor catalogue server to filter spam messages
Name:		perl-Razor-Agent
Version:	2.84
Release:	%mkrel 1
Group:		Networking/Mail
License:	Artistic
URL:		http://razor.sourceforge.net
Source0:	http://prdownloads.sourceforge.net/razor/%{pkgname}-%{version}.tar.bz2
Requires:	perl-Net-DNS
BuildRequires:	perl-devel
BuildRequires:	perl-Net-DNS
BuildRequires:	perl-Digest-SHA1
BuildRequires:	perl-MailTools
BuildRequires:	perl-Time-HiRes
BuildRequires:	perl-URI
BuildRequires:	perl-MIME-Base64
BuildRoot:	%{_tmppath}/%{name}-%{version}-builroot

%description
Vipul's Razor is a distributed, collaborative, spam detection and filtering
network. Razor establishes a distributed and constantly updating catalogue of
spam in propagation.  This catalogue is used by clients to filter out known
spam. On receiving a spam, a Razor Reporting Agent (run by an end-user or a
troll box) calculates and submits a 20-character unique identification of the
spam (a SHA Digest) to its closest Razor Catalogue Server. The Catalogue Server
echos this signature to other trusted servers after storing it in its database.
Prior to manual processing or transport-level reception, Razor Filtering Agents
(end-users and MTAs) check their incoming mail against a Catalogue Server and
filter out or deny transport in case of a signature match. Catalogued spam,
once identified and reported by a Reporting Agent, can be blocked out by the
rest of the Filtering Agents on the network.

%prep

%setup -q -n %{pkgname}-%{version}

%build

%{__perl} Makefile.PL INSTALLDIRS=vendor

pushd Razor2-Preproc-deHTMLxs
    %{__perl} Makefile.PL INSTALLDIRS=vendor
popd

%make OPTIMIZE="%{optflags}" 

%check
make test

pushd Razor2-Preproc-deHTMLxs
    make test
popd

%install
rm -rf %{buildroot}

pushd Razor2-Preproc-deHTMLxs
%makeinstall_std
popd

%makeinstall_std

install -d %{buildroot}%{_mandir}/man5
install -m0644 blib/man5/*.5 %{buildroot}%{_mandir}/man5

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, root)
%doc BUGS CREDITS Changes FAQ README SERVICE_POLICY
%{_bindir}/*
%{perl_vendorlib}/Razor2
%{perl_vendorlib}/auto/Razor2
%{perl_vendorarch}/Razor2
%{perl_vendorarch}/auto/Razor2
%{_datadir}/man/*/*
