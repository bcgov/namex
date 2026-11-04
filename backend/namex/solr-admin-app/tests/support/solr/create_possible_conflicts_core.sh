#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

docker exec solr /tmp/solr/create_core.sh
docker exec solr /tmp/solr/create_schema.sh

curl "http://localhost:8983/solr/admin/cores?core=possible.conflicts&action=RELOAD"
