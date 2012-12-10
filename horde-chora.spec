%define	module	chora
%define	name	horde-%{module}
%define	version	2.1
%define	release	%mkrel 7

%define _requires_exceptions pear(Horde.*)

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	The Horde CVS viewer
License:	GPL
Group: 		System/Servers
URL:		http://www.horde.org/%{module}
Source0:	ftp://ftp.horde.org/pub/%{module}/%{module}-h3-%{version}.tar.bz2
Requires(post):	rpm-helper
Requires:	horde >= 3.3.5
Requires:	cvs
BuildArch:	noarch

%description
Chora is the Horde CVS viewer, and it provides an advanced web-based 
view of any CVS repository. It now includes annotation support, visual 
branch viewing capability, and human-readable diffs.

%prep
%setup -q -n %{module}-h3-%{version}

%build

%install
rm -rf %{buildroot}

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
# %{name} Apache configuration file

<Directory %{_datadir}/horde/%{module}/lib>
    Order allow,deny
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/locale>
    Order allow,deny
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/scripts>
    Order allow,deny
    Deny from all
</Directory>

<Directory %{_datadir}/horde/%{module}/templates>
    Order allow,deny
    Deny from all
</Directory>
EOF

# horde configuration
install -d -m 755 %{buildroot}%{_sysconfdir}/horde/registry.d
cat > %{buildroot}%{_sysconfdir}/horde/registry.d/%{module}.php <<'EOF'
<?php
//
// Chora Horde configuration file
//
 
$this->applications['chora'] = array(
    'fileroot'    => $this->applications['horde']['fileroot'] . '/chora',
    'webroot'     => $this->applications['horde']['webroot'] . '/chora',
    'name'        => _("Version Control"),
    'status'      => 'active',
    'menu_parent' => 'devel'
);
EOF

# remove .htaccess files
find . -name .htaccess -exec rm -f {} \;

# install files
install -d -m 755 %{buildroot}%{_datadir}/horde/%{module}
cp -pR *.php %{buildroot}%{_datadir}/horde/%{module}
cp -pR themes %{buildroot}%{_datadir}/horde/%{module}
cp -pR lib %{buildroot}%{_datadir}/horde/%{module}
cp -pR locale %{buildroot}%{_datadir}/horde/%{module}
cp -pR templates %{buildroot}%{_datadir}/horde/%{module}
cp -pR config %{buildroot}%{_sysconfdir}/horde/%{module}

install -d -m 755 %{buildroot}%{_sysconfdir}/horde
pushd %{buildroot}%{_datadir}/horde/%{module}
ln -s ../../../..%{_sysconfdir}/horde/%{module} config
popd

# activate configuration files
for file in %{buildroot}%{_sysconfdir}/horde/%{module}/*.dist; do
	mv $file ${file%.dist}
done

# fix script shellbang
for file in `find %{buildroot}%{_datadir}/horde/%{module}/scripts`; do
	perl -pi -e 's|/usr/local/bin/php|/usr/bin/php|' $file
done

%clean
rm -rf %{buildroot}

%post
if [ $1 = 1 ]; then
	# configuration
	%create_ghostfile %{_sysconfdir}/horde/%{module}/conf.php apache apache 644
	%create_ghostfile %{_sysconfdir}/horde/%{module}/conf.php.bak apache apache 644
fi
%if %mdkversion < 201010
%_post_webapp
%endif

%postun
%if %mdkversion < 201010
%_postun_webapp
%endif

%files
%defattr(-,root,root)
%doc COPYING README docs
%config(noreplace) %{_webappconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/horde/registry.d/%{module}.php
%config(noreplace) %{_sysconfdir}/horde/%{module}
%{_datadir}/horde/%{module}



%changelog
* Tue Aug 03 2010 Thomas Spuhler <tspuhler@mandriva.org> 2.1-7mdv2011.0
+ Revision: 565209
- Increased release for rebuild

* Mon Jan 18 2010 Guillaume Rousse <guillomovitch@mandriva.org> 2.1-6mdv2010.1
+ Revision: 493342
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise
- restrict default access permissions to localhost only, as per new policy
- header in registry config file

* Sun Sep 20 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.1-3mdv2010.0
+ Revision: 445977
- new version
- new setup (simpler is better)

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 2.1-2mdv2010.0
+ Revision: 437872
- rebuild

* Thu Mar 19 2009 Guillaume Rousse <guillomovitch@mandriva.org> 2.1-1mdv2009.1
+ Revision: 358197
- update to new version 2.1

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 2.0.1-6mdv2009.0
+ Revision: 246876
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Dec 18 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.0.1-4mdv2008.1
+ Revision: 132440
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Fri Aug 25 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.0.1-3mdv2007.0
- Rebuild

* Wed Jan 11 2006 Guillaume Rousse <guillomovitch@mandriva.org> 2.0.1-2mdk
- fix automatic dependencies

* Tue Dec 27 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.0.1-1mdk
- new version
- %%mkrel

* Thu Jun 30 2005 Guillaume Rousse <guillomovitch@mandriva.org> 2.0-5mdk 
- better fix encoding
- fix requires

* Fri Feb 18 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0-4mdk
- spec file cleanups, remove the ADVX-build stuff
- strip away annoying ^M

* Thu Jan 27 2005 Guillaume Rousse <guillomovitch@mandrake.org> 2.0-3mdk 
- no automatic config generation, incorrect default values
- horde isn't a prereq
- spec cleanup

* Mon Jan 17 2005 Guillaume Rousse <guillomovitch@mandrake.org> 2.0-2mdk 
- fix inclusion path
- fix configuration perms
- generate configuration at postinstall
- horde and rpm-helper are now a prereq

* Fri Jan 14 2005 Guillaume Rousse <guillomovitch@mandrake.org> 2.0-1mdk 
- new version
- top-level is now /var/www/horde/chora
- config is now in /etc/horde/chora
- other non-accessible files are now in /usr/share/horde/chora
- drop old obsoletes
- no more apache configuration
- rpmbuildupdate aware
- spec cleanup

* Wed Aug 04 2004 Guillaume Rousse <guillomovitch@mandrake.org> 1.2.2-1mdk 
- new version

* Sun Jul 18 2004 Guillaume Rousse <guillomovitch@mandrake.org> 1.2-4mdk 
- apache config file in /etc/httpd/webapps.d

* Sat May 01 2004 Guillaume Rousse <guillomovitch@mandrake.org> 1.2-3mdk
- renamed to horde-chora
- pluggable horde configuration
- standard perms for /etc/httpd/conf.d/%%{order}_horde-chora.conf
- don't provide useless ADVXpackage virtual package
- untagged localisation files
- removed .htaccess files

* Tue Sep 09 2003 Guillaume Rousse <guillomovitch@linux-mandrake.com> 1.2-2mdk
- changed order to 72, as all other horde apps
- requires horde, not horde2
- standard perms and ownership for config files, access is already denied

* Mon Sep 08 2003 Guillaume Rousse <guillomovitch@linux-mandrake.com> 1.2-1mdk
- 1.2
- spec cleanup
- remove useless files from webroot (.dist, doc files, .po)
- properly tag localisation files
- ADVX macros
- apache2 integration
- fixed URL

