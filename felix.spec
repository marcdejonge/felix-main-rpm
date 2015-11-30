Name:           felix-service
Version:        1.0.0
Release:        1%{?dist}
Summary:        This package installs Apache Felix as a daemon.
BuildArch:	noarch

License:        Apache v2.0
URL:            https://jonghuis.nl/osgi/felix

BuildRequires:  maven-local
Requires:       java-headless >= 1.8

Source:		felix-service.tar.gz

%description
Apache Felix is an OSGi framework that makes it possible to dynamically add, update and remove Java bundles at runtime. It also facilitates easy interaction between bundles using APIs without having hard dependencies between bundles. This package installs this framework and adds the scripts to run it as a daemon.

%prep
tar -xvf $RPM_SOURCE_DIR/felix-service.tar.gz

%build

%install
mkdir -p $RPM_BUILD_ROOT/etc/felix/config
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/lib/java
mkdir -p $RPM_BUILD_ROOT/usr/lib/felix

cp felix-run.sh $RPM_BUILD_ROOT/usr/bin/felix
chmod +x $RPM_BUILD_ROOT/usr/bin/felix

BASE_URL=http://mirror.proserve.nl/apache/felix/
NAME=org.apache.felix.main
VERSION=`curl -s $BASE_URL | perl -n -e/$NAME'-([\d\.]+)\.jar/ && print $1'`
curl -s $BASE_URL$NAME-$VERSION.jar > $RPM_BUILD_ROOT/usr/lib/java/$NAME.jar

cp felix.config $RPM_BUILD_ROOT/etc/felix/felix.conf

for NAME in org.apache.felix.gogo.command org.apache.felix.gogo.runtime org.apache.felix.gogo.shell org.apache.felix.shell.remote
do
	VERSION=`curl -s $BASE_URL | perl -n -e/$NAME'-([\d\.]+)\.jar/ && print $1'`
	curl -s $BASE_URL$NAME-$VERSION.jar > $RPM_BUILD_ROOT/usr/lib/felix/$NAME.jar
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc
/etc/felix/felix.conf
/usr/bin/felix
/usr/lib/java/org.apache.felix.main.jar
/usr/lib/felix/org.apache.felix.gogo.command.jar
/usr/lib/felix/org.apache.felix.gogo.runtime.jar
/usr/lib/felix/org.apache.felix.gogo.shell.jar
/usr/lib/felix/org.apache.felix.shell.remote.jar

%changelog
*Wed Nov 25 2015 Marc de Jonge <marcdejonge@gmail.com> 1
-- Initial Build
