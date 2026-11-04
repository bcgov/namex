#!/bin/bash

KCADM=/opt/jboss/keycloak/bin/kcadm.sh
OUTPUT=$($KCADM create users -r master -s username=$1 -s enabled=true --no-config --server http://localhost:8080/auth --realm master --user admin --password admin 2>&1)
echo $OUTPUT
if [[ $OUTPUT == *"Created new user"* ]]; then
	$KCADM set-password -r master --username $1 -p $2 --no-config --server http://localhost:8080/auth --realm master --user admin --password admin
	$KCADM add-roles -r master --uusername $1 --rolename $3 --no-config --server http://localhost:8080/auth --realm master --user admin --password admin
	$KCADM get-roles -r master --uusername $1 --no-config --server http://localhost:8080/auth --realm master --user admin --password admin
else
	echo $OUTPUT
    exit 1
fi
