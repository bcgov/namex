-- noinspection SqlNoDataSourceInspectionForFile

DROP TRIGGER NAMESDB.NAMEX_TRANSACTION_QMSG;

CREATE OR REPLACE TRIGGER NAMESDB.namex_transaction_qmsg AFTER INSERT ON NAMESDB.TRANSACTION FOR EACH ROW
BEGIN
    namex_trigger_handler.enqueue_transaction(:new.transaction_id);

    EXCEPTION
        WHEN OTHERS THEN
            application_log_insert('namex_qmsg', SYSDATE, -1, SQLERRM);
END;
/
