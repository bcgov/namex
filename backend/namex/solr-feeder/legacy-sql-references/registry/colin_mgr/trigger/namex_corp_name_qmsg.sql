-- noinspection SqlNoDataSourceInspectionForFile

DROP TRIGGER NAMEX_CORP_NAME_QMSG;

CREATE OR REPLACE TRIGGER namex_corp_name_qmsg AFTER INSERT ON CORP_NAME FOR EACH ROW
BEGIN
    namex_trigger_handler.enqueue_corp_name(:new.corp_num, :new.corp_name_typ_cd, :new.start_event_id,
            :new.corp_name_seq_num);
    namex_trigger_handler.enqueue_corporation(:new.corp_num);

    EXCEPTION
        WHEN OTHERS THEN
            application_log_insert('namex_name_qmsg', SYSDATE, -1, SQLERRM);
END;
/
