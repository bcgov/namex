-- noinspection SqlNoDataSourceInspectionForFile

CREATE OR REPLACE PACKAGE NAMEX.solr AS
    --
    -- Called from a job to send queued changes to Solr.
    --
    -- Errors will appear in application_log, and also in the solr_feeder.error_msg for the last error for that entry.
    -- Errored rows will be retried the next time the job runs, so we need a way to make sure something isn't stuck in
    -- limbo forever.
    PROCEDURE feed_solr;
END solr;
/
