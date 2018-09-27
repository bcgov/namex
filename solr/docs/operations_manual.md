
# Solr Operations Manual

_September 2018_

The document describes everything you should ever need to know about the care and feeding of Solr.

## 1. Background

### 1.1 What is Solr

[Apache Solr](http://lucene.apache.org/solr) is the database and search system. Solr is configured with one or more
_cores_, each of which is a searchable database. For the NAMEX application we have three cores, one each for name
history, possible name conflicts, and possible trademark conflicts. The search system uses a collection of _synonyms_ to
disallow the use of similar legal entity names. For example, _bistro_ and _restaurant_ are synonyms, so if _Bob's
Restaurant_ already exists then _Bob's Bistro_ would be considered a conflicting name.

Solr works by configuring cores, and then loading the cores by _indexing_ a set of _documents_ - this is called a
_dataimport_. A _document_ can be nearly anything, and in our case we use either database rows or JSON strings. Once
documents are loaded into a core, they can be searched by running a _query_ in the search system. Searching is done
either through a web-based user interface (used for testing, etc), or a set of web services (used by the NAMEX
application).

### 1.2 Solr in OpenShift

NAMEX builds upon the Solr v6.6 [bcgov/openshift-solr](https://github.com/bcgov/openshift-solr) repository by adding
support for multiple cores, PostgreSQL database drivers, and the ability to read synonyms from a database rather than a
file. The resulting project [bcgov/namex-solr](https://github.com/bcgov/namex-solr) provides documentation that gives
in-depth details on creating the base Solr image. This image is generic and has no NAMEX-specific functionality. It
rarely changes.

The [bcgov/namex/solr](https://github.com/bcgov/namex/solr) project adds NAMEX-specific functionality. It sets up the
three cores _names_, _possible.conflicts_, and _trademarks_. The configuration for the cores defines the algorithms that
are used for document indexing, as well as the algorithms for the queries.

### 1.3 Solr on the Desktop

When configuring the indexing and query algorithms, it is often preferable to run Solr on your desktop. Doing so is
accomplished by following the steps in the
[standalone installation](https://github.com/bcgov/namex/tree/master/solr/docs/solr_standalone_installation.md)
documentation. 

### 1.4 Loading Cores

Documents are put into the cores through an initial bulk data load, and then optionally followed by updates for those
cores that have data that changes frequently.

#### 1.4.1 Loading the _names_ Core

The _names_ core is loaded through the Solr web-based UI. The dataimport is set up to read from a view called
`solr_dataimport_names_vw` in the Oracle "NAMES" databases. This step is only performed once, and afterwards any changes
to the view are slowly fed into the core through the Solr web services.

#### 1.4.2 Loading the _possible.conflicts_ Core

The _possible.conflicts_ core is loaded through the Solr web-based UI. The dataimport is set up to read from a view
called `solr_dataimport_conflicts_vw` in the Oracle "NAMES" and "REGISTRY" databases. This step is only performed once,
and afterwards any changes to the view are slowly fed into the core through the Solr web services.

#### 1.4.3 Loading the _trademarks_ Core

The _trademarks_ core is different from the above cores. Trademarks data is published every six months by the Canadian
Intellectual Property Office. The data is parse to extract only that which is of interest to us, and then the extracted
data is fed into the core through the Solr web services. When a new set of data is published, the core will be wiped out
and then reloaded. See the [trademarks](https://github.com/bcgov/namex/tree/master/solr/trademarks) project for details.

### 1.5 Synonyms in Solr

As mentioned above, we have synonyms such as _bistro_ and _restaurant_, so that if _Bob's Restaurant_ already exists
then _Bob's Bistro_ would be considered a conflicting name. Solr normally stores synonyms in a file, but since the
collection of synonyms is always evolving it was decided to put them into a database for ease of editing. The database
for the synonyms is called `postgresql-solr`. It is a standard PostgreSQL instance.

The application for editing the synonyms is called `solr-admin-app`. It is a Python application built using the Flask
Admin framework for database CRUD operations. Authentication is done using Keycloak. This application is deployed to all
environments, but it is read-only in dev and production. The idea is that staff will edit the synonyms in the test
environment, and do whatever testing they need to do. Once they are happy with the synonyms they will be exported to the
production environment for use. They will also be exported at the same time to the development environment, so that
searching there behaves similarly to test and production. All synonym edits are recorded in an audit table, which is
also accessed through the application. The audit table is readonly in all environments.

Synonyms are only used for querying the _names_ and _possible.conflicts_ cores. Since they are not used for indexing,
changing the synonyms does not force a re-index of the documents in these cores. However, the two cores do need to be
reloaded when the synonyms change, as they cache the synonyms on startup. There is no interruption of service when the
cores are reloaded.

### TODO: Logical Diagrams

## 2 Operations

If the following do not answer your operations questions, please add a new one (with the answer!).

##### How do I know if Solr is running?

The easiest way to check that Solr is running is to look at the OpenShift pod called `solr` in the environment. If the
pod it up, it means that Solr's liveness probe is answering requests.

You can also visit Solr's web-based UI for the environment. The URL for the UI can be found in OpenShift's routes, with
the name `solr`. The _Dashboard_ tells you how long Solr has been running, and how much JVM memory is being used. The
_Core Admin_ tells you when a core was started, when it was last updated, and how many documents it contains.

##### How do I make `solr-admin-app` editable in dev?

Usually the `solr-admin-app` does not allow the user to edit data - all editing is done in the test environment and
exported to the others. However, if you need to test in OpenShift and want to use the dev environment, change the
`FLASK_ENV` environment variable to be _testing_.

##### How do I know that the _names_ core is up to date?

The _names_ core is up to date if it contains the same number of documents as there are rows in the
`solr_dataimport_names_vw` view in the NAMES database (NAMESD/NAMEST/NAMESP). Note that it can take a minute for data
to flow from the database to Solr.

##### How do I know that the _possible.conflicts_ core is up to date?

The _possible.conflicts_ core is up to date if it contains the same number of documents as there are rows in the
`solr_dataimport_conflicts_vw` view in the NAMES database (NAMESD/NAMEST/NAMESP) plus the REGISTRY database
(CDEV/CTST/CPRD). Note that it can take a minute for data to flow from the databases to Solr.

##### What do I do if the cores are not up to date?

This indicates a bug in the feeders. 

##### How do I know that the _trademarks_ core is up to date?

The _trademarks_ core only changes twice a year, so basically if it has data it should be correct. All environments
should have the same number of documents.

##### How do I know that the solr-feeder is running?

##### How do I know that the solr-feeder is working?

LOgs, probes

##### How do I reconfigure the solr-feeder endpoint?

##### How do I troubleshoot missing/extra core data?

trigger and feeder tables and statuses

##### How do I resend data from Oracle?

##### How do I find errors on the Oracle side?

##### What is an Oracle Access Control List?

##### What is an Oracle Wallet?


-- change db settings? Like hostname