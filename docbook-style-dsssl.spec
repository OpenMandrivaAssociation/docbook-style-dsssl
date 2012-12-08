%define name docbook-style-dsssl
%define version 1.79
%define release 13

name:		%{name}
version:	%{version}
release:	%{release}
Group:		Publishing

Summary:	Norman Walsh's modular stylesheets for DocBook

License:	Artistic style
URL:		http://sourceforge.net/projects/docbook/

Requires:	sgml-common >= 0.2
Requires:	jade >= 1.2.1

BuildRoot:	%{_tmppath}/%{name}-buildroot 

BuildArch:	noarch
Source0:	http://prdownloads.sourceforge.net/docbook/docbook-dsssl-%{version}.tar.bz2
Patch0:		docbook-dsssl-1.78-DTDDECL.patch

%define sgmlbase %{_datadir}/sgml

%description
These DSSSL stylesheets allow you to convert any DocBook document to another
printed (for example, RTF or PostScript) or online (for example, HTML) format.
They are highly customizable.


%prep
%setup -n docbook-dsssl-%{version} -q
%setup -T -D -n docbook-dsssl-%{version}
%patch0 -p1

%build

%install
DESTDIR=$RPM_BUILD_ROOT
mkdir -p $DESTDIR%{_bindir}
mkdir -p $DESTDIR%{sgmlbase}/docbook/dsssl-stylesheets-%{version}/

cd $RPM_BUILD_DIR/docbook-dsssl-%{version}

install bin/collateindex.pl $DESTDIR%{_bindir}
cp -r contrib catalog dtds VERSION olink common html frames lib print images $DESTDIR%{sgmlbase}/docbook/dsssl-stylesheets-%{version}/

rm -f $DESTDIR%{sgmlbase}/docbook/dsssl-stylesheets
ln -sf dsssl-stylesheets-%{version} $DESTDIR%{sgmlbase}/docbook/dsssl-stylesheets

cd ..


%clean
DESTDIR=$RPM_BUILD_ROOT
rm -rf $DESTDIR


%Files
%defattr (0644,root,root,0755)
%doc BUGS README RELEASE-NOTES.* VERSION
%doc ChangeLog WhatsNew
%attr(-,root,root) %{_bindir}/collateindex.pl
%dir %{sgmlbase}/docbook/dsssl-stylesheets-%{version}
%{sgmlbase}/docbook/dsssl-stylesheets-%{version}/*
%{sgmlbase}/docbook/dsssl-stylesheets

%post
# remove possible old references to 
# %{sgmlbase}/docbook/dsssl-stylesheets-%{version}/catalog
rm -f %{_sysconfdir}/sgml/sgml-docbook-\*.cat

# fix old broken stuff
if [ -f %{_sysconfdir}/sgml/xml-docbook-\*.cat ]; then
sed -e '\|CATALOG "%{_sysconfdir}/sgml/xml-docbook-\*.cat"|D' %{_sysconfdir}/sgml/catalog > \
	%{_sysconfdir}/sgml/catalog.bak 
    mv -f %{_sysconfdir}/sgml/catalog.bak %{_sysconfdir}/sgml/catalog
    rm -f %{_sysconfdir}/sgml/xml-docbook-\*.cat
fi

for centralized in %{_sysconfdir}/sgml/sgml-docbook-*.cat; do
   if [ "$centralized" = "%{_sysconfdir}/sgml/sgml-docbook-*.cat" ]; then break; fi
   sed -e "/dsssl-stylesheets-[0-9]/D" $centralized > \
	 $centralized.bak 
   mv -f $centralized.bak $centralized
done 

for centralized in %{_sysconfdir}/sgml/{sgml,xml}-docbook-*.cat; do
  if [ "$centralized" = "%{_sysconfdir}/sgml/{sgml,xml}-docbook-*.cat" ]; then break; fi
  if [ "$centralized" = "%{_sysconfdir}/sgml/xml-docbook-*.cat" ]; then continue; fi
  if [ "$centralized" = "%{_sysconfdir}/sgml/sgml-docbook-*.cat" ]; then continue; fi
  if [ -f "$centralized" ]; then
     %{_bindir}/xmlcatalog --sgml --noout --add $centralized \
	 %{sgmlbase}/docbook/dsssl-stylesheets/catalog
   fi
done

%postun 
# Do not remove if upgrade
if [ "$1" = "0" -a -x %{_bindir}/xmlcatalog ]; then
     for centralized in %{_sysconfdir}/sgml/{sgml,xml}-docbook-*.cat; do
      if  [ "$centralized" = "%{_sysconfdir}/sgml/{sgml,xml}-docbook-*.cat" ]; then break; fi
      if  [ "$centralized" = "%{_sysconfdir}/sgml/xml-docbook-*.cat" ]; then continue; fi
      if  [ "$centralized" = "%{_sysconfdir}/sgml/sgml-docbook-*.cat" ]; then continue; fi

	if [ -w $centralized ]; then
	  %{_bindir}/xmlcatalog --sgml --noout --del $centralized \
	     %{sgmlbase}/docbook/dsssl-stylesheets/catalog
	fi
     done 
    
fi




%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.79-11mdv2011.0
+ Revision: 663840
- mass rebuild

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.79-10mdv2011.0
+ Revision: 604807
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 1.79-9mdv2010.1
+ Revision: 520692
- rebuilt for 2010.1

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 1.79-8mdv2010.0
+ Revision: 413370
- rebuild

* Sat Mar 21 2009 Funda Wang <fwang@mandriva.org> 1.79-7mdv2009.1
+ Revision: 359903
- fix patch num

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 1.79-7mdv2009.0
+ Revision: 220675
- rebuild

* Sat Jan 12 2008 Thierry Vignaud <tv@mandriva.org> 1.79-6mdv2008.1
+ Revision: 149204
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu Aug 16 2007 Thierry Vignaud <tv@mandriva.org> 1.79-5mdv2008.0
+ Revision: 64211
- rebuild

* Sat Apr 28 2007 Adam Williamson <awilliamson@mandriva.org> 1.79-4mdv2008.0
+ Revision: 18847
- clean spec; rebuild for new era


* Tue Mar 21 2006 Camille Begnis <camille@mandriva.com> 1.79-3mdk
- rebuild

* Fri Feb 11 2005 Camille Begnis <camille@mandrakesoft.com> 1.79-2mdk
- fix circular link [Bug 13511]
- fix license and summary

* Fri Nov 05 2004 Camille Begnis <camille@mandrakesoft.com> 1.79-1mdk
- 1.79

* Thu Apr 22 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 1.78-6mdk
- Don't output error when xmlcatalog is no longer present when uninstalling

* Mon Jul 21 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 1.78-5mdk
- Fix install when more than one dtd package is installed

* Fri Jul 18 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 1.78-4mdk
- Fix install when no sgml dtd package is installed

* Tue May 13 2003 <camille@ke.mandrakesoft.com> 1.78-3mdk
- Added a patch to remove unsupported DTDDECL entry in catalog
- removed unneeded 'Requires: docbook-dtd-sgml'

* Fri Apr 25 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 1.78-2mdk
- Remove xml-docbook-*.cat wrongly created

