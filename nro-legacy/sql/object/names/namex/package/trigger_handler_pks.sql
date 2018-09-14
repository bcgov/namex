-- noinspection SqlNoDataSourceInspectionForFile

CREATE OR REPLACE PACKAGE NAMEX.trigger_handler AS
    --
    -- Called from a trigger in NAMESDB to queue data that needs to be sent to the namex application.
    --
    PROCEDURE enqueue_transaction(id NUMBER);
END trigger_handler;
/
