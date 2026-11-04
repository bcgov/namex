#!/bin/bash
SCRIPT_DIR=$(dirname $0)

docker build -t 'openshift-solr' -f ${SCRIPT_DIR}/Dockerfile ${SCRIPT_DIR}
