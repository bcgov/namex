#!/bin/bash

KCADM=/opt/jboss/keycloak/bin/kcadm.sh
OUTPUT=$($KCADM create users -r master -s username=$1 -s enabled=true --no-config --server http://localhost:8080/auth --realm master --user admin --password admin 2>&1)
echo $OUTPUT
if [[ $OUTPUT == *"Created new user"* ]]; then
	USERID=$(echo $OUTPUT | cut -d"'" -f 2)
	OUTPUT=$($KCADM set-password -r master --username $1 -p $2 --no-config --server http://localhost:8080/auth --realm master --user admin --password admin 2>&1)
else
	echo $OUTPUT
    exit 1
fi
