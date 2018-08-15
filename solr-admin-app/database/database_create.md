
# Scripts for creating databases.

The SQL in database_create.sql is used to create the database objects needed for Solr configuration. These are a "least
effort" way of creating the seldom-changing objects. This process would be much easier if there was a way to run the
script from pgadmin, but that does not seem to work.

This documentation assumes that `oc.exe` from OpenShift Origin Client Tools has been installed and that the user is
either running Minishift locally or has an account on the Pathfinder OpenShift cluster.

## Port Forward to the OpenShift Database

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

## Run the Script

Next connect to the database and run the scripts:

```
C:\> "C:\Program Files\PostgreSQL\10\bin\psql" -h localhost -p 54321 -f C:\<path>\database_create.sql solr <username>
C:\> "C:\Program Files\PostgreSQL\10\bin\psql" -h localhost -p 54321 -f C:\<path>\synonyms_data.sql solr <username>
```
