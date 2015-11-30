Name:           felix-service
Version:        1.0.0
Release:        1%{?dist}
Summary:        This package installs Apache Felix as a daemon.
BuildArch:	noarch

License:        Apache v2.0
URL:            https://jonghuis.nl/osgi/felix

BuildRequires:  maven-local
Requires:       java-headless >= 1:8

%description
Apache Felix is an OSGi framework that makes it possible to dynamically add, update and remove Java bundles at runtime. It also facilitates easy interaction between bundles using APIs without having hard dependencies between bundles. This package installs this framework and adds the scripts to run it as a daemon.

%prep
rm -rf $RPM_BUILD_DIR/*
BASE_URL=http://mirror.proserve.nl/apache/felix/
for NAME in org.apache.felix.main org.apache.felix.gogo.command org.apache.felix.gogo.runtime org.apache.felix.gogo.shell org.apache.felix.shell.remote
do
	VERSION=`curl -s $BASE_URL | perl -n -e/$NAME'-([\d\.]+)\.jar/ && print $1'`
	curl -s $BASE_URL$NAME-$VERSION.jar > $NAME.jar
done

%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/var/felix
cp org.apache.felix.gogo.* $RPM_BUILD_ROOT/var/felix
cp org.apache.felix.shell* $RPM_BUILD_ROOT/var/felix

mkdir -p $RPM_BUILD_ROOT/usr/bin
cp org.apache.felix.main* $RPM_BUILD_ROOT/usr/bin
echo '#!/bin/bash' > $RPM_BUILD_ROOT/usr/bin/felix.sh
echo 'java \\ ' > $RPM_BUILD_ROOT/usr/bin/felix.sh
echo '    -Dfelix.config.properties="file:///etc/felix/felix.conf \\ ' > $RPM_BUILD_ROOT/usr/bin/felix.sh
echo '    -Dfelix.cm.dir="/etc/felix/config \\ ' > $RPM_BUILD_ROOT/usr/bin/felix.sh
echo '    -Djava.security.policy="/etc/felix/all.policy" \\ ' > $RPM_BUILD_ROOT/usr/bin/felix.sh
echo '    -Dlogback.configurationFile="/etc/felix/logback.xml" \\ ' > $RPM_BUILD_ROOT/usr/bin/felix.sh
echo '    -jar /usr/bin/org.apache.felix.main.jar ' > $RPM_BUILD_ROOT/usr/bin/felix.sh
chmod +x $RPM_BUILD_ROOT/usr/bin/felix.sh

mkdir -p $RPM_BUILD_ROOT/etc/felix/config
echo "felix.startlevel.framework=1" > $RPM_BUILD_ROOT/etc/felix/felix.conf
echo "felix.startlevel.bundle=2" >> $RPM_BUILD_ROOT/etc/felix/felix.conf
echo "org.osgi.framework.startlevel.beginning=2" >> $RPM_BUILD_ROOT/etc/felix/felix.conf
echo "felix.auto.deploy.dir=/var/felix" >> $RPM_BUILD_ROOT/etc/felix/felix.conf
echo "felix.auto.deploy.action=install,update,start" >> $RPM_BUILD_ROOT/etc/felix/felix.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc
/etc/felix/felix.conf
/usr/bin/felix.sh
/usr/bin/org.apache.felix.main.jar
/var/felix/org.apache.felix.gogo.command.jar
/var/felix/org.apache.felix.gogo.runtime.jar
/var/felix/org.apache.felix.gogo.shell.jar
/var/felix/org.apache.felix.shell.remote.jar

%changelog
*Wed Nov 25 2015 Marc de Jonge <marcdejonge@gmail.com> 1
-- Initial Build
