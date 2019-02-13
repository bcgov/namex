#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

rm $DIR/keycloak_client_info
docker exec keycloak /tmp/keycloak/create_client.sh namex-solr-admin-app > $DIR/keycloak_client_info
docker exec keycloak /tmp/keycloak/create_role.sh names_manager

docker exec keycloak /tmp/keycloak/create_user_with_role.sh names-with-admin-access WhatEver1 names_manager
docker exec keycloak /tmp/keycloak/create_user.sh names-no-admin-access WhatEver1

python $DIR/adjust_client_secrets_json.py