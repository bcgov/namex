# Installing Solr

*October 2018 – Windows 7 government workstation*

Apache Solr is the search index database used by the name examination system. To do development with Solr, you may want
to run it locally as a standalone server - this allows for rapid reconfiguration without the overheads associated with
GitHub and OpenShift.

This documentation describes the process for reconfiguring Apache Solr so that it can use JDBC connections to read from
databases. These connections are used for both loading the core data as well as the synonyms used for queries. This
process should not need to be repeated often - once it has been done for a new version of Solr, it can be zipped up and
made available to the team.

## Solr Installation Steps

Download the version of Solr that matches what is being run in OpenShift. At the time of writing, this is
[v6.6.3](http://archive.apache.org/dist/lucene/solr/6.6.3/solr-6.6.3.zip).
Unzip it to a local (C: drive) directory, as it will be faster than running it off the home directory (which is mapped
to the networked H: drive).

### Reconfigure Jetty

The version of the Jetty web server that comes with Solr is stripped down and provides minimal functionality. As we
need JNDI for datasource lookups, we need to add some functionality to Jetty.

Download the version of Jetty that matches what is being run by Solr. Looking at the `server\lib` directory in Solr
v6.6.3, we see that the jar files from Jetty are
[v9.3.14](https://repo1.maven.org/maven2/org/eclipse/jetty/jetty-distribution/9.3.14.v20161028). Copy:
* Jetty's `etc\jetty-plus.xml` to Solr's `server\etc`.
* Jetty's `lib\jetty-jndi-9.3.14.v20161028.jar` to Solr's `server\lib`.
* Jetty's `lib\jetty-plus-9.3.14.v20161028.jar` to Solr's `server\lib`.
* Jetty's `modules\jndi.mod` to Solr's `server\modules`.
* Jetty's `modules\plus.mod` to Solr's `server\modules`.
* Jetty's `modules\security.mod` to Solr's `server\modules`.
* Jetty's `modules\servlet.mod` to Solr's `server\modules`.
* Jetty's `modules\webapp.mod` to Solr's `server\modules`.

Create the file `server\start.d\plus.ini` with the contents
```
--module=plus
```

### Additional Libraries

Our custom version of Solr requires the following additional libraries.

####  PostgreSQL Driver

To load data via the PostgreSQL foreign data wrappers, you need the PostgreSQL driver. See the `Dockerfile` in the
repository `bcgov/namex-solr` for the most recent version, but at the time of writing the driver can be downloaded from
http://central.maven.org/maven2/org/postgresql/postgresql/42.2.1/postgresql-42.2.1.jar. Put this jar into the Solr
directory `server\lib`.

####  Solr JDBC Library

To load the synonyms from a JDBC connection rather than a file, we use the third-party project `shopping24/solr-jdbc`.
See the `Dockerfile` in the repository `bcgov/namex-solr` for the most recent version, but at the time of writing the
library can be downloaded from
http://central.maven.org/maven2/com/s24/search/solr/solr-jdbc/2.3.8/solr-jdbc-2.3.8.jar. Create the directory
`contrib\dataimporthandler\lib` and put the jar into it.

Solr JDBC requires the Apache Commons library `DBUtils`. Checking the `pom.xml` project for `shopping24/solr-jdbc` we
see that `commons-dbutils.version` is v1.6, but we will go with the latest
[v1.7](http://central.maven.org/maven2/commons-dbutils/commons-dbutils/1.7/commons-dbutils-1.7.jar). Download it and
put into `server\lib`.

#### Zip it up!

The reconfiguration is complete! Zip up the directory into something like `solr-namex-6.6.3.zip` and spread it around.
See the document `solr_standalone_installation.md` for details on configuring for use with namex.
