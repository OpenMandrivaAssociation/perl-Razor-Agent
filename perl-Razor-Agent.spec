%define debug_package %{nil}
%define pkgname razor-agents
%define upstream_version 2.85

Summary:	Use a Razor catalogue server to filter spam messages
Name:		perl-Razor-Agent
Version:	%perl_convert_version %{upstream_version}
Release:	22
Group:		Networking/Mail
License:	Artistic License 2.0
Url:		https://razor.sourceforge.net
Source0:	http://prdownloads.sourceforge.net/razor/%{pkgname}-%{upstream_version}.tar.bz2
BuildRequires:	perl-devel
BuildRequires:	perl-Net-DNS
BuildRequires:	perl-Digest-SHA1
BuildRequires:	perl-MailTools
BuildRequires:	perl-Time-HiRes
BuildRequires:	perl-URI
BuildRequires:	perl-MIME-Base64
Requires:	hping2
Requires:	perl-Net-DNS

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
%setup -qn %{pkgname}-%{upstream_version}

%build
%__perl Makefile.PL INSTALLDIRS=vendor

pushd Razor2-Preproc-deHTMLxs
%__perl Makefile.PL INSTALLDIRS=vendor
popd

%make OPTIMIZE="$CFLAGS" 

%check
make test

pushd Razor2-Preproc-deHTMLxs
make test
popd

%install
%makeinstall_std -C Razor2-Preproc-deHTMLxs
%makeinstall_std

install -d %{buildroot}%{_mandir}/man5
install -m0644 blib/man5/*.5 %{buildroot}%{_mandir}/man5

# fix some defaults
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}/var/log/razor
install -d %{buildroot}%{_sysconfdir}/razor

cat > %{buildroot}%{_sysconfdir}/razor/razor-agent.conf << EOF
logfile                = /var/log/razor/razor-agent.log
EOF

# fix logrotating
cat > %{buildroot}%{_sysconfdir}/logrotate.d/razor-agent << EOF
/var/log/razor/razor-agent.log {
    # create 644 root root
    weekly
    notifempty
    missingok
    compress
}
EOF

%post
# only do this if we have a working network and if the config file contains just one line
if [ "`cat %{_sysconfdir}/razor/razor-agent.conf|wc -l`" -eq "1" ] ; then
    if /usr/sbin/hping -c 4 -p 2703 --tcpexitcode discovery.razor.cloudmark.com >/dev/null 2>&1; then
        %{_bindir}/razor-admin -d -create -home=%{_sysconfdir}/razor
    else
        echo "You might want to run \"%{_bindir}/razor-admin -d -create -home=%{_sysconfdir}/razor\" when your network works"
    fi
fi

%files
%doc BUGS CREDITS Changes FAQ README SERVICE_POLICY
%attr(0755,root,root) %dir %{_sysconfdir}/razor
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/razor/razor-agent.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/razor-agent
%{_bindir}/*
%{perl_vendorlib}/Razor2
%{perl_vendorlib}/auto/Razor2
%{perl_vendorarch}/Razor2
%{perl_vendorarch}/auto/Razor2
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%attr(0755,root,root) %dir /var/log/razor

