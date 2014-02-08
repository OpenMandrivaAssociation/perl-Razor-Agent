%define pkgname razor-agents

%define debug_package %{nil}

Summary:	Use a Razor catalogue server to filter spam messages
Name:		perl-Razor-Agent
Version:	2.85
Release:	10
Group:		Networking/Mail
License:	Artistic License 2.0
URL:		http://razor.sourceforge.net
Source0:	http://prdownloads.sourceforge.net/razor/%{pkgname}-%{version}.tar.bz2
Requires:	perl-Net-DNS
Requires:	hping2
BuildRequires:	perl-devel
BuildRequires:	perl-Net-DNS
BuildRequires:	perl-Digest-SHA1
BuildRequires:	perl-MailTools
BuildRequires:	perl-Time-HiRes
BuildRequires:	perl-URI
BuildRequires:	perl-MIME-Base64

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

%make OPTIMIZE="$CFLAGS" 

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

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, root)
%doc BUGS CREDITS Changes FAQ README SERVICE_POLICY
%attr(0755,root,root) %dir %{_sysconfdir}/razor
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/razor/razor-agent.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/razor-agent
%{_bindir}/*
%{perl_vendorlib}/Razor2
%{perl_vendorlib}/auto/Razor2
%{perl_vendorarch}/Razor2
%{perl_vendorarch}/auto/Razor2
%{_mandir}/*/*
%attr(0755,root,root) %dir /var/log/razor


%changelog
* Sun Feb 12 2012 Per Ã˜yvind Karlsen <peroyvind@mandriva.org> 2.85-9
+ Revision: 773477
- drop %%serverbuild...
- svn commit -m mass rebuild of perl extension against perl 5.14.2

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuilt for perl-5.14.2
    - bump release
    - rebuilt for perl-5.14.x

* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 2.85-5
+ Revision: 667301
- mass rebuild

* Sun Aug 01 2010 Funda Wang <fwang@mandriva.org> 2.85-4mdv2011.0
+ Revision: 564577
- rebuild for perl 5.12.1

  + JÃ©rÃ´me Quelin <jquelin@mandriva.org>
    - rebuild for perl 5.12

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 2.85-2mdv2010.1
+ Revision: 426586
- rebuild

* Wed Jul 23 2008 Frederic Crozat <fcrozat@mandriva.com> 2.85-1mdv2009.0
+ Revision: 242355
- Release 2.85
- Code is now under Artistic License 2.0

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 2.84-5mdv2009.0
+ Revision: 224004
- rebuild

* Wed Jan 23 2008 Thierry Vignaud <tv@mandriva.org> 2.84-4mdv2008.1
+ Revision: 157265
- rebuild with fixed %%serverbuild macro

* Tue Jan 15 2008 Thierry Vignaud <tv@mandriva.org> 2.84-3mdv2008.1
+ Revision: 152251
- rebuild
- kill re-definition of %%buildroot on Pixel's request
- replace %%{_datadir}/man by %%{_mandir}!

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Wed Jul 18 2007 Oden Eriksson <oeriksson@mandriva.com> 2.84-2mdv2008.0
+ Revision: 53257
- provide a basic /etc/razor/razor-agent.conf file and do magic in %%post, fixes #26573
- use the %%serverbuild macro

* Sun Jun 03 2007 Oden Eriksson <oeriksson@mandriva.com> 2.84-1mdv2008.0
+ Revision: 34849
- 2.84
- spec file cleansing


* Wed May 31 2006 Frederic Crozat <fcrozat@mandriva.com> 2.82-1mdv2007.0
- Release 2.82

* Tue Apr 04 2006 Frederic Crozat <fcrozat@mandriva.com> 2.81-1mdk
- Release 2.80
- use mkrel

* Wed Mar 01 2006 Frederic Crozat <fcrozat@mandriva.com> 2.80-1mdk
- Release 2.80

* Thu Jul 07 2005 Frederic Crozat <fcrozat@mandriva.com> 2.75-1mdk 
- Release 2.75

* Mon Jul 04 2005 Frederic Crozat <fcrozat@mandriva.com> 2.74-1mdk 
- Release 2.74

* Tue Jun 21 2005 Götz Waschk <waschk@mandriva.org> 2.72-2mdk
- drop the symlinks (thanks to Daniel J McDonald)

* Fri Jun 17 2005 Götz Waschk <waschk@mandriva.org> 2.72-1mdk
- New release 2.72

* Wed Dec 29 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.67-1mdk 
- Release 2.67

* Mon Nov 15 2004 Michael Scherer <misc@mandrake.org> 2.61-2mdk
- Rebuild for new perl

* Tue Jul 06 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.61-1mdk
- Release 2.61

* Wed May 19 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 2.40-1mdk
- Release 2.40
- Remove patch0 (merged upstream)
- perl-Digest-Nilsimsa is no longer needed

* Mon Nov 17 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.36-3mdk
- rebuilt for perl-5.8.2

* Wed Nov 05 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 2.36-2mdk
- Fix build on older distro than 9.2 (Nicolas Chipaux)
- from Oden Eriksson <oden.eriksson@kvikkjokk.net>
 - added rediffed P0 taken from the spamassassin v2.60 tarball
 - misc spec file fixes

* Mon Aug 18 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.36-1mdk
- 2.36
- use %%makeinstall_std macro

* Thu Jul 31 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.34-4mdk
- Always enforce perl-Net-DNS dependency, it is not auto-detected by spechelper

* Wed Jul 16 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.34-3mdk
- Fix buildrequires

* Wed Jun 04 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.34-2mdk
- Fix man install for Mdk 8.0

* Mon Jun 02 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 2.34-1mdk
- Release 2.34

