#!/bin/bash

KCADM=/opt/jboss/keycloak/bin/kcadm.sh
$KCADM create roles -r master -s name=$1 --no-config --server http://localhost:8080/auth --realm master --user admin --password admin 2>&1
