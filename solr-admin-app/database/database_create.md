
# postgresql-solr

This document describes the process for creating the PostgreSQL database that is used by the Solr application.

#### Storage

In the OpenShift Console, go to your environment and select `Storage` from right left-hand menu. Click the `Create
Storage` button. For `Name` enter `postgresql-solr`. For size enter `1 GiB`. Click the `Create` button.

#### Database

In the OpenShift Console, go to your environment and select `Catalog` from right left-hand menu. Click the `PostgreSQL`
icon.
 - Page 1: Click `Next`.
 - Page 2: For the `Database Service Name` enter `postgresql-solr`, and for `Database name` enter `solr`. Click `Next`.
 - Page 3: Select `Create a secret to be used later`. Click `Create`.
 - Page 4: Click `Close`.

#### Scripts for creating databases

The SQL in `database_create.sql` is used to create the database objects needed for Solr configuration. These are a
"least effort" way of creating the seldom-changing objects. This process would be much easier if there was a way to run
the script from pgadmin, but that does not seem to work.

This documentation assumes that `oc.exe` from OpenShift Origin Client Tools has been installed and that the user is
either running Minishift locally or has an account on the Pathfinder OpenShift cluster.

#### Port Forward to the OpenShift Database

Log into the `OpenShift Web Console`. Click the drop-down for your username in the upper-right corner, and select
`Copy Login Command`. Paste the command into your shell:

```
C:\> oc login https://console.pathfinder.gov.bc.ca:8443 --token=<blahblahblah>
Logged into "https://console.pathfinder.gov.bc.ca:8443" as "<username>" using the token provided.

You have access to the following projects and can switch between them with 'oc project <projectname>':

  * servicebc-ne-dev
    servicebc-ne-test
    servicebc-ne-tools

Using project "servicebc-ne-dev".
```

(Note that you could also run `oc login` and enter the same credentials).

If your current project isn't the one of the environment you're working with, change it. For example for dev:

```
C:\> oc project servicebc-ne-dev
```

Start the port forwarding:

```
C:\> oc port-forward postgresql-solr-<pod-id> 54321:5432
```

#### Run the Script

Next connect to the database and run the scripts:

```
C:\> "C:\Program Files\PostgreSQL\10\bin\psql" -h localhost -p 54321 -f C:\<path>\database_create.sql solr <username>
C:\> "C:\Program Files\PostgreSQL\10\bin\psql" -h localhost -p 54321 -f C:\<path>\synonyms_data.sql solr <username>
```

TEMP Synonym load: POrt-forward test, tehn:

pg_dump -h localhost -p 54321 -U userXXX -W --table=synonym --data-only --column-inserts solr > syn.sql

pg_dump -h localhost -p 54321 -U userXXX -W --table=synonym_audit --data-only --column-inserts solr > syn_a.sql

Port-forward first dev, then prod and:

psql -h localhost -p 54321 solr userXXX
> delete from synonym;
> delete from synonym_audit;
> \q

psql -h localhost -p 54321 -f syn.sql solr userXXX

psql -h localhost -p 54321 -f syn_a.sql solr userXXX

reload cores -3
