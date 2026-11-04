#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
docker run --rm -v $DIR/lib:/tmp/solr -p 8983:8983 --name solr library/solr

