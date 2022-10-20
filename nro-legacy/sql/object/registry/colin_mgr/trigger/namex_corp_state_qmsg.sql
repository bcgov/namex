-- noinspection SqlNoDataSourceInspectionForFile

DROP TRIGGER NAMEX_CORP_STATE_QMSG;

CREATE OR REPLACE TRIGGER namex_corp_state_qmsg AFTER INSERT ON CORP_STATE FOR EACH ROW
BEGIN
    namex_trigger_handler.enqueue_corp_state(:new.corp_num, :new.start_event_id);
    namex_trigger_handler.enqueue_corporation(:new.corp_num);

    EXCEPTION
        WHEN OTHERS THEN
            application_log_insert('namex_state_qmsg', SYSDATE, -1, SQLERRM);
END;
/
