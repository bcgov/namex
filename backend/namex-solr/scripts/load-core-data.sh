#!/bin/bash

SERVER=localhost
PORT=8983

if [ -z "$1" ]; then
    # Usage
    echo 'Usage: load-core-data.sh <core-name>'
else
    CORENAME=$1
    ENDPOINT="http://${SERVER}:${PORT}/solr/${CORENAME}/dataimport?command=full-import&wt=json"
    echo $ENDPOINT
    CURL=`curl -X GET ${ENDPOINT}`
    echo $CURL
fi
