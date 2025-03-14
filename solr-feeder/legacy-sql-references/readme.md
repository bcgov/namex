
# Legacy Oracle SQL

This document describes the references to legacy Oracle SQL. This folder contains the Oracle artifacts that lead to calling the Solr Feeder to update the Solr instances of NameX, Business Search and Person Search.

## Directory Layout

The directories are laid out as:
 
 - `sql/<SCHEMA>/<OBJECT_TYPE>/<SQL>`, such as `sql/registry/colin_mgr/trigger/namex_corp_name_qmsg.sql`.
 - `sql/release/<YYYYMMDD_RELEASE_NAME>/<DATABASE>/<SCHEMA>`, such as `sql/release/20230706_updates_for_dir_search/colin_mgr/create.sql`. The convention for unconfirmed dates is represent unknown values such as `201809XX` and to rename the directory once the date is confirmed.

The releases can be run with the command `sqlplus user/pass@database @scriptname`.

The `release` directory contains the scripts that are run to make the changes that are in the items under the `object`
directory. The `object` directory should be a copy of what exists in the database, so there are a few things to keep in
mind:

 - The directory structure is what is used to indicate what user is to run the contained scripts.
 - The table scripts drop and recreate the tables, which is something that is not typically done when the tables contain
   data. For example, when adding a column to a table you typically put the `ALTER TABLE` command in a file under the
   `release` directory, but you would also add the column to the table under the `object` directory so that a future
   comparison does not produce differences.
 - TOAD is the tool used by the DBAs, so the files under `object` should be in TOAD format. This makes life much easier
   for the DBA when comparing databases across environments, and comparing an environment against the repository. Try to
   follow convention when updating or creating files.
 - If there is more than one release on the go at a single time, it is very easy to accidentally deploy changes from a
   different release. Ideally do no have more than one future release, or if you do then ensure that they are touching
   different objects.

Obviously this workflow is not perfect and has room for improvement - suggestions welcome!

## Deployment Procedure

The following procedures are to be followed when making Oracle database changes:

 - DEV: The development is for the developers to do as they please. However, all changes must be tracked in this repository, and must have proper scripts in a `release` directory.
 - TEST: Once changes are ready to go to test, give the DBAs the link to the GitHub location containing the release changes.
 - PROD: Production changes typically are only made during the Tuesday evening or Sunday morning change window. An outage window will have to be arranged with the DBAs.

## Helpful debugging queries

```
select trigger_name from sys.dba_triggers;
```

```
select TRIGGER_NAME, TRIGGERING_EVENT, TABLE_NAME, STATUS from sys.dba_triggers where trigger_name='NAMEX_INSERT_CORPORATION_QMSG';
```

```
select * from namex.triggered_corporation where corp_num='<corp_num>';
```

```
select * from namex.solr_feeder where corp_num='<corp_num>';
```

```
select * from namex.APPLICATION_LOG where PROGRAM_NAME='<interested_program_name>' and LOG_DATE > to_date('2025-03-10', 'yyyy-mm-dd') and LOG_DATE < to_date('2025-03-11', 'yyyy-mm-dd');
```