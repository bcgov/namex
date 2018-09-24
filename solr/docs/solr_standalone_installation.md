# Installing Solr

*September 2018 – Windows 7 government workstation*

Apache Solr is the search index database used by the name examination system. To do development with Solr, you may want
to run it locally as a standalone server - this allows for rapid reconfiguration without the overheads associated with
GitHub and OpenShift.

The documentation describes the process for installing the custom version of Apache Solr that was built using the steps
described in `solr_custom_standalone.md`. This documentation assumes that you have a copy of the Github project
`bcgov/namex` on your local computer in the directory `C:\Users\<username>\PycharmProjects\namex`.

## Solr Installation Steps

Unzip the archive created in `solr_standalone_customization.md` to a local (C: Drive) directory, as it will be faster
than running it off the home directory ()which is mapped to the networked H: drive).

### Solr Jetty Datasource

The first step is to configure the datasources used by the application. Create a new file
`server\solr-webapp\webapp\WEB-INF\jetty-env.xml`.

If you are using port-forwarded OpenShift PostgreSQL databases for the synonyms and wrappers, use the following file
with the appropriate `[username]` and `[password]` settings:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Configure PUBLIC "-//Mort Bay Consulting//DTD Configure//EN" "http://www.eclipse.org/jetty/configure.dtd">

<Configure class="org.eclipse.jetty.webapp.WebAppContext">
    <!-- =====================================================================

    The connection to the database that contains the synonyms.

    ====================================================================== -->
    <New id="synonyms" class="org.eclipse.jetty.plus.jndi.Resource">
        <Arg></Arg>
        <Arg>jdbc/synonyms</Arg>
        <Arg>
            <New class="org.postgresql.ds.PGSimpleDataSource">
                <Set name="User">[username]</Set>
                <Set name="Password">[password]</Set>
                <Set name="DatabaseName">namex</Set>
                <Set name="ServerName">localhost</Set>
                <Set name="PortNumber">54321</Set>
            </New>
        </Arg>

        <!-- bind to java:comp/env for this webapp -->
        <Call name="bindToENC">
            <Arg>jdbc/synonyms</Arg>
        </Call>
    </New>

    <!-- =====================================================================

    The connection to the corporations database used for loading cores.

    ====================================================================== -->
    <New id="bcrs_corps" class="org.eclipse.jetty.plus.jndi.Resource">
        <Arg></Arg>
        <Arg>jdbc/bcrs_corps</Arg>
        <Arg>
            <New class="org.postgresql.ds.PGSimpleDataSource">
                <Set name="User">[username]</Set>
                <Set name="Password">[password]</Set>
                <Set name="DatabaseName">BC_REGISTRIES</Set>
                <Set name="ServerName">localhost</Set>
                <Set name="PortNumber">54322</Set>
            </New>
        </Arg>

        <!-- bind to java:comp/env for this webapp -->
        <Call name="bindToENC">
            <Arg>jdbc/bcrs_corps</Arg>
        </Call>
    </New>

    <!-- =====================================================================

    The connection to the names database used for loading cores.

    ====================================================================== -->
    <New id="bcrs_names" class="org.eclipse.jetty.plus.jndi.Resource">
        <Arg></Arg>
        <Arg>jdbc/bcrs_names</Arg>
        <Arg>
            <New class="org.postgresql.ds.PGSimpleDataSource">
                <Set name="User">[username]</Set>
                <Set name="Password">[password]</Set>
                <Set name="DatabaseName">BC_REGISTRIES_NAMES</Set>
                <Set name="ServerName">localhost</Set>
                <Set name="PortNumber">54323</Set>
            </New>
        </Arg>

        <!-- bind to java:comp/env for this webapp -->
        <Call name="bindToENC">
            <Arg>jdbc/bcrs_names</Arg>
        </Call>
    </New>
</Configure>
```

### Port Forwarding

Start the port forwarding to the OpenShift databases in a shell:

```
C:\> start /b oc port-forward postgresql-solr-<pod_id> 54321:5432
C:\> start /b oc port-forward postgres-oracle-fdw-registry-<pod_id> 54322:5432
C:\> start /b oc port-forward postgresql-oracle-fdw-names-<pod_id> 54323:5432
```

### Starting Solr

In a new shell, change directory in Solr and start the application:

```
C:\Users\<username>\solr-6.6.3> bin\solr start
Waiting up to 30 to see Solr running on port 8983
Started Solr server on port 8983. Happy searching!
```

Solr is now running on [http://localhost:8983](http://localhost:8983) and has a web UI that can be used for
configuration and testing.

## Creating Solr Cores

Create the Solr cores from the latest files on GitHub in the `solr` directory of the `bcgov/namex` project:

```
C:\Users\<username>\solr-6.6.3> bin\solr create -c names -d C:\Users\<username>\PycharmProjects\namex\solr\cores\names\conf
C:\Users\<username>\solr-6.6.3> bin\solr create -c possible.conflicts -d C:\Users\<username>\PycharmProjects\namex\solr\cores\possible.conflicts\conf
C:\Users\<username>\solr-6.6.3> bin\solr create -c trademarks -d C:\Users\<username>\PycharmProjects\namex\solr\cores\trademarks\conf
```

### Loading Solr Cores

The `names` and `possible.conflicts` cores are loaded through the Solr UI. Select the core name from the `Core Selector`
drop down list, and then choose `dataimport`. Click the `Execute` button and the core will begin loading through the
port-forwarded PostgreSQL databases.

The `trademarks` core is loaded using a custom Python script and a custom extract of the trademarks data. See the
[https://github.com/bcgov/namex/blob/master/solr/trademarks](trademarks) portion of the namex project for details on
running the loader script (the parser script should already have been run, with the extract stored in
`N:\BCAP2\6450 Projects\20-Mainframe Migration\Names Examination\trademarks`).
s