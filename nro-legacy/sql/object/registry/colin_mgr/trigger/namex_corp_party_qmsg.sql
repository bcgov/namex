-- noinspection SqlNoDataSourceInspectionForFile

DROP TRIGGER NAMEX_CORP_PARTY_QMSG;

CREATE OR REPLACE TRIGGER namex_corp_party_qmsg AFTER INSERT or UPDATE or DELETE ON CORP_PARTY FOR EACH ROW
BEGIN
    IF :new.party_typ_cd not in ('PAS','PDI','PSA','RAD','RAF','RAO','RAS','TAP','TAA','TSP') THEN
        namex_trigger_handler.enqueue_corporation(:new.corp_num);
    END IF;

    EXCEPTION
        WHEN OTHERS THEN
            application_log_insert('namex_corp_party_qmsg', SYSDATE, -1, SQLERRM);
END;
/
