
--
-- Monitoring queries.
--

SELECT * FROM application_log ORDER BY log_date DESC;

SELECT * FROM namex_feeder WHERE status != 'C' ORDER BY id DESC;

SELECT * FROM solr_feeder WHERE status != 'C' ORDER BY id DESC;

SELECT * FROM namex_feeder ORDER BY id DESC;

SELECT * FROM solr_feeder ORDER BY id DESC;

-- Ensure Solr cores are the correct size.

SELECT COUNT(*) FROM solr_dataimport_names_vw;

SELECT COUNT(*) FROM solr_dataimport_conflicts_vw;

-- Ensure Solr views do not have duplicate IDs - should be empty.

SELECT id, COUNT(*) FROM solr_dataimport_conflicts_vw GROUP BY id HAVING COUNT(*) > 1;

SELECT id, COUNT(*) FROM solr_dataimport_names_vw GROUP BY id HAVING COUNT(*) > 1;


--
-- Debugging queries.
--

-- Find what has been triggered for a given NR Number.

SELECT * FROM name_transaction NATURAL JOIN transaction NATURAL JOIN request NATURAL JOIN event WHERE nr_num = :nr_num
        ORDER BY transaction_id DESC;

SELECT * FROM name_transaction ORDER BY transaction_id DESC;

SELECT * FROM triggered_corp_name ORDER BY id DESC;

SELECT * FROM triggered_corp_state ORDER BY id DESC;


--
-- Administrative tasks (common).
--

-- Check the jobs.

SELECT o.name, j.program_action, j.last_start_date, j.last_end_date FROM sys.scheduler$_job j INNER JOIN sys.obj$ o ON
    j.obj# = o.obj# WHERE name IN ('NAMEX_OUTBOUND', 'SOLR_OUTBOUND') ORDER BY name;

-- Disable jobs - use the force flag so that we can disable even if the job is currently running.

/*
EXECUTE DBMS_SCHEDULER.disable('NAMEX_OUTBOUND', TRUE);

EXECUTE DBMS_SCHEDULER.disable('SOLR_OUTBOUND', TRUE);
*/

-- Enable jobs.

EXECUTE DBMS_SCHEDULER.enable('NAMEX_OUTBOUND');

EXECUTE DBMS_SCHEDULER.enable('SOLR_OUTBOUND');

-- Check the ACLs.

SELECT * FROM dba_network_acls;


--
-- Administrative tasks (rare).
--

-- Do the initial data load of names data into the NAMEX postgresql database. This is done by putting every NR into the
-- namex_feeder table, which generally is used to trickle data in as it comes into the database.

/*
INSERT INTO namex.namex_feeder (id, transaction_id, status, nr_num, action)
        WITH data AS
        (
            SELECT 0 transaction_id, 'P' status, nr_num, 'C' action FROM request
            WHERE nr_num LIKE 'NR %' AND request_id > 0 AND request_id <= 1
            ORDER BY request_id
        )
        SELECT namex_feeder_id_seq.NEXTVAL, transaction_id, status, nr_num, action FROM data;
*/

-- DANGEROUS! Drop jobs - use the force flag so that we can drop even if the job is currently running. Useful if the job
-- is stuck in a busy loop, but ensure that you are able to recreate the job afterwards.

/*
EXECUTE DBMS_SCHEDULER.drop_job('NAMEX_OUTBOUND', TRUE);

EXECUTE DBMS_SCHEDULER.drop_job('SOLR_OUTBOUND', TRUE);
*/
