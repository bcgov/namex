-- noinspection SqlNoDataSourceInspectionForFile

CREATE OR REPLACE PACKAGE BODY trigger_handler AS
    --
    -- Add the given transaction id to the queue.
    --
    PROCEDURE enqueue_transaction(id NUMBER) IS
    BEGIN
        INSERT INTO name_transaction (transaction_id) VALUES (id);
    EXCEPTION
        WHEN OTHERS THEN
            dbms_output.put_line('error: ' || SQLCODE || ' / ' || SQLERRM);
            application_log_insert('enqueue_transaction', SYSDATE(), -1, SQLERRM);
    END;
END trigger_handler;
/
