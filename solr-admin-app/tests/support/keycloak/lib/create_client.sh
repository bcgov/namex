#!/bin/bash

KCADM=/opt/jboss/keycloak/bin/kcadm.sh
OUTPUT=$($KCADM create clients -r master -s clientId=$1 -s enabled=true -s 'redirectUris=["http://0.0.0.0:8080/*", "http://localhost:8080/*", "http://0.0.0.0:8090/*", "http://localhost:8090/*"]' --no-config --server http://localhost:8080/auth --realm master --user admin --password admin 2>&1)
if [[ $OUTPUT == *"Created new client"* ]]; then
	CLIENTID=$(echo $OUTPUT | cut -d"'" -f 2)
	$KCADM get clients/$CLIENTID/installation/providers/keycloak-oidc-keycloak-json -r master --no-config --server http://localhost:8080/auth --realm master --user admin --password admin
else
	echo $OUTPUT
    exit 1
fi
