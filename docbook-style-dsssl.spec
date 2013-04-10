%define sgmlbase %{_datadir}/sgml

Summary:	Norman Walsh's modular stylesheets for DocBook
name:		docbook-style-dsssl
version:	1.79
release:	14
Group:		Publishing
License:	Artistic style
Url:		http://sourceforge.net/projects/docbook/
Source0:	http://prdownloads.sourceforge.net/docbook/docbook-dsssl-%{version}.tar.bz2
Patch0:		docbook-dsssl-1.78-DTDDECL.patch
BuildArch:	noarch
Requires:	openjade
Requires:	sgml-common >= 0.2

%description
These DSSSL stylesheets allow you to convert any DocBook document to another
printed (for example, RTF or PostScript) or online (for example, HTML) format.
They are highly customizable.

%prep
%setup -qn docbook-dsssl-%{version}
%setup -T -D -n docbook-dsssl-%{version}
%apply_patches

%build

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{sgmlbase}/docbook/dsssl-stylesheets-%{version}/

install bin/collateindex.pl %{buildroot}%{_bindir}
cp -r contrib catalog dtds VERSION olink common html frames lib print images %{buildroot}%{sgmlbase}/docbook/dsssl-stylesheets-%{version}/

rm -f %{buildroot}%{sgmlbase}/docbook/dsssl-stylesheets
ln -sf dsssl-stylesheets-%{version} %{buildroot}%{sgmlbase}/docbook/dsssl-stylesheets

%files
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

