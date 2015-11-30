#!/bin/bash

# Make sure only root can run our script
if [[ $EUID -ne 0 ]]; then
	echo "Felix must be started as root" 1>&2
	exit 1
fi

java \
    -Dfelix.config.properties="file:///etc/felix/felix.conf" \
    -Djava.security.policy="/etc/felix/all.policy" \
    -Dlogback.configurationFile="/etc/felix/logback.xml" \
    -jar /usr/lib/java/org.apache.felix.main.jar

