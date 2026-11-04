## Local SOLR build/run
Everything in this folder was copied from the solr-dev pod and altered accordingly for running the bcgov namex solr instance locally.

### Getting recent version of the solr files:
- **NOTE:** *if you just want the recent manage_schema / other single file changes you can copy/paste them into solr/... from repo bcgov/namex/solr and skip these steps*
1. overwrite solr directory: `oc rsync <solr-pod>:server/solr .`
2. delete trademarks data folder at: `solr/mycores/trademarks/data`
- **NOTE:** *if you get errors creating any of the other cores try deleting the data folder like ^ and rebuild the image (it will be recreated with the core when it boots up)*

### Running the solr instance locally:
1. update the dockerfile:
- uncomment out all the 'for running locally' code in the dockerfile
- comment out these permission change commands ~line 97:
```
RUN chgrp -R 0 /opt/solr \
    && chmod -R g+rwX /opt/solr

RUN chgrp -R 0 /opt/docker-solr \
    && chmod -R g+rwX /opt/docker-solr
```
2. Fill in empty db env variables
- **NOTE:** *to access dbs on your localhost set the host env to `host.docker.internal`*
3. Build the image `docker build . -t solr`
4. run the image `docker run -p 8983:8983 --name=solr solr:latest`
5. in your browser go to: http://localhost:8983/solr/#/
6. do a data import on the cores you want to use via the UI
