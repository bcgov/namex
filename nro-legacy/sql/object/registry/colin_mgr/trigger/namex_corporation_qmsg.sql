-- noinspection SqlNoDataSourceInspectionForFile

DROP TRIGGER NAMEX_CORPORATION_QMSG;

CREATE OR REPLACE TRIGGER namex_corporation_qmsg AFTER INSERT or UPDATE ON CORPORATION FOR EACH ROW
BEGIN
    namex_trigger_handler.enqueue_corporation(:new.corp_num);

    EXCEPTION
        WHEN OTHERS THEN
            application_log_insert('namex_corporation_qmsg', SYSDATE, -1, SQLERRM);
END;
/
