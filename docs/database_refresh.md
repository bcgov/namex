# Database Refresh

This document describes the process used to refresh the development environment's
`postgresql` database from the `NAMESD` Oracle database.

#### 1. Export the OpenShift PostgreSQL database

```
$ oc login https://console.pathfinder.gov.bc.ca:8443 --token=[your token]
$ oc -n servicebc-ne-dev port-forward postgresql-dev-<pod_id> 54323:5432 &
```

In `pgAgmin`:

1. Connect to the database as the `postgres` user on `localhost:54323`.
1. Under `Databases` right-click `namex` and choose `Backup...`.
1. Choose a file on your local disk (not a network drive, for performance).
1. Click the "Backup" button.

#### 2. Import into a local instance of PostgreSQL

In `pgAgmin`:

1. Connect to your local database as the `postgres` user.
1. Under `Databases` if you have a `namex` database, `Delete/Drop` it.
1. Create a `namex` database.
1. Right-click `namex` and choose `Restore...`.
1. Choose the backup file.
1. In the `Restore options` tab under the `Do not save` section, set `Owner` to `Yes`.
1. Click the `Restore` button.

#### 3. Delete data from the tables to be loaded

In `pgAgmin`:

1. Under the `namex` database open `Schemas`, then `public`, and then `Tables`.
1. Right-click the `requests` table and choose `Truncate` > `Truncate Cascade`.

#### 4. Do the Oracle database setup

So that the development environment isn't impacted, create a new feeder table called `namex_feeder_temp`.
```sql
-- Create a temporary feeder table.
CREATE TABLE namex_feeder_temp
   (id NUMBER(10, 0) NOT NULL, 
    transaction_id NUMBER(10, 0) NOT NULL, 
    status CHAR(1 BYTE) DEFAULT 'P' NOT NULL, 
    nr_num VARCHAR2(10 BYTE),
    action CHAR(1 BYTE), 
    send_count NUMBER(10, 0) DEFAULT 0, 
    send_time TIMESTAMP(6),
    error_msg VARCHAR2(4000 BYTE)
   );

INSERT INTO namex_feeder_temp (id, transaction_id, status, nr_num, action)
    WITH data AS
    (
        SELECT 0 transaction_id, 'P' status, nr_num, 'C' action FROM request
        WHERE nr_num LIKE 'NR %' ORDER BY request_id
    )
    SELECT namex_feeder_id_seq.NEXTVAL, transaction_id, status, nr_num, action FROM data;
```

#### 5. Run `nro-extractor` locally to load the tables

It would take a week to load the NRs sequentially, so instead split the work among ten parallel processes.

Set up the `.env` for the `nro-extractor` project so that it connects to the local PostGreSQL and NAMESD:

```
# nro-extractor settings.

# Connection information for NAMESD.
NRO_DB_NAME=namesd.bcgov
NRO_HOST=[HOSTNAME]
NRO_PASSWORD=[PASSWORD]
NRO_PORT=1521
NRO_USER=[USERNAME]

# Connection information for the local installation of PostgreSQL.
PG_HOST=localhost
PG_NAME=namex
PG_PASSWORD=[PASSWORD]
PG_USER=postgres

# Maximum number of rows per run - all of them.
MAX_ROWS=10000000
```

In PyCharm edit `namex/jobs/nro-extractor/extractor/app.py` with:
1. In two places change the table name to `namex_feeder_temp`. At the time of writing, this was lines 49 and 63.
1. Change the first query to do 1/10 of the NRs, by adding ` AND SUBSTR(nr_num, 10, 1) = '0'`

Note that the last digit of the NR is used because the majority of them start with "NR 0". Using the last digit gives an even distribution between the processes. Run the script in the background. Change the "0" from step #2 to "1" and re-run, etc, up to "9".

#### 6. Export the local PostgreSQL database

In `pgAgmin`:

1. Connect to the local database as the `postgres` user.
1. Under `Databases` right-click `namex` and choose `Backup...`.
1. Choose a file on your local disk (not a network drive, for performance).
1. Click the "Backup" button.

#### 7. Shut down NameX including cron jobs

It's a good idea to shut down all of NameX, rather than have it try to work while the database and permissions are missing.

#### 8. Import into the OpenShift PostgreSQL

##### _NOTE: this process drops the namex database and recreates with the necessary permissions. There is probably a better way._

```
$ oc login https://console.pathfinder.gov.bc.ca:8443 --token=[your token]
$ oc -n servicebc-ne-dev port-forward postgresql-dev-<pod_id> 54323:5432 &
```

In `pgAgmin`:

1. Connect to the OpenShift database as the `postgres` user.
1. Under `Databases` if you have a `namex` database, `Delete/Drop` it.
1. Create a `namex` database.
1. Right-click `namex` and choose `Restore...`.
1. Choose the backup file.
1. In the `Restore options` tab under the `Do not save` section, set `Owner` to `Yes`.
1. Click the `Restore` button.

In PostgreSQL:
 
```sql
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "<appuser>";
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO "<appuser>";
COMMIT;
```

#### 9. Do data cleanup

Since all the NRs will be created in NameX, the `furnished` flag will not be set on a lot of NRs. If you don't do this, the `nro-update` cron job will run for days.

```sql
UPDATE requests SET furnished = 'Y' WHERE state_cd IN ('APPROVED', 'CANCELLED', 'COMPLETED', 'EXPIRED', 'HISTORICAL', 'REJECTED');
```

A bunch of the NRs are marked not completed but they have decisions. Consider the decision to have been made.

``sql
UPDATE requests SET state_cd = 'APPROVED' WHERE state_cd in ('DRAFT', 'INPROGRESS', 'HOLD') AND requests.id IN
    (SELECT nr_id FROM names WHERE state = 'APPROVED');
UPDATE requests SET state_cd = 'REJECTED' WHERE state_cd in ('DRAFT', 'INPROGRESS', 'HOLD') AND requests.id IN
    (SELECT nr_id FROM names WHERE state = 'REJECTED');
COMMIT;
```

Next, if this returns nothing:

```sql
SELECT * FROM requests INNER JOIN names ON requests.id = names.nr_id WHERE state_cd = 'HOLD' AND state != 'NE';
```

then set all HOLDs back to DRAFT:

```sql
UPDATE requests SET state_cd = 'DRAFT' WHERE state_cd = 'HOLD';
COMMIT;
```

Finally, all the DRAFT requests should not have name decisions. This should be empty:

```sql
SELECT state_cd, state, requests.*, names.* FROM requests INNER JOIN names ON requests.id = names.nr_id WHERE state_cd = 'DRAFT' AND state != 'NE';
```


#### 10. Start NameX

In OpenShift start NameX (slowly to make sure everything is OK). Run some smoke tests.

#### 11. Clean up Oracle

Drop the `namex_feeder_temp` table in NAMESD.

#### 12. Final notes

Something still doesn't seem right with the data, but it's NRO data from 2006. For example, there are names in NRO that are unexamined but have decision data. Suggest that at some point we do a full comparison and sync as needed. We will also probably need to sync corp nums for consumed names, etc.