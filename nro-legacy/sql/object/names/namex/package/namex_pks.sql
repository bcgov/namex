-- noinspection SqlNoDataSourceInspectionForFile

CREATE OR REPLACE PACKAGE NAMEX.namex AS
    --
    -- Called from a job to send NRs that have been queued due to being created or changed to NameX.
    --
    -- NRs that are no longer in (where state = DRAFT) will not send changes to NameX
    --
    -- Errors will appear in application_log, and also in the namex_feeder.error_msg.
    -- Errored NRs will be retried the next time the job runs, so we need a way to
    -- make sure something isn't stuck in limbo forever.
    PROCEDURE queue_data_for_namex;
END namex;
/
