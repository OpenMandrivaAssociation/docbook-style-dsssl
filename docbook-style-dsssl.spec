%define name docbook-style-dsssl
%define version 1.79
%define release %mkrel 4

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
%patch -p1

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


