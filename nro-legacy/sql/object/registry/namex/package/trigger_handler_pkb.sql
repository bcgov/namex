-- noinspection SqlNoDataSourceInspectionForFile

CREATE OR REPLACE PACKAGE BODY NAMEX.trigger_handler AS
    --
    -- Called from a trigger in COLIN_MGR_XXX to queue name data that needs to be sent to the namex application.
    --
    PROCEDURE enqueue_corp_name(p_corp_num VARCHAR2, p_corp_name_typ_cd CHAR, p_start_event_id INTEGER,
            p_corp_name_seq_num INTEGER) IS
    BEGIN
        INSERT INTO triggered_corp_name (id, corp_num, corp_name_typ_cd, start_event_id, corp_name_seq_num) VALUES
                (triggered_corp_name_seq.NEXTVAL, p_corp_num, p_corp_name_typ_cd, p_start_event_id,
                p_corp_name_seq_num);
    EXCEPTION
        WHEN OTHERS THEN
            dbms_output.put_line('error: ' || SQLCODE || ' / ' || SQLERRM);
            application_log_insert('enqueue_corp_name', SYSDATE(), -1, SQLERRM);
    END;

    --
    -- Called from a trigger in COLIN_MGR_XXX to queue state data that needs to be sent to the namex application.
    --
    PROCEDURE enqueue_corp_state(p_corp_num VARCHAR2, p_start_event_id INTEGER) IS
    BEGIN
        INSERT INTO triggered_corp_state (id, corp_num, start_event_id) VALUES (triggered_corp_state_seq.NEXTVAL,
                p_corp_num, p_start_event_id);
    EXCEPTION
        WHEN OTHERS THEN
            dbms_output.put_line('error: ' || SQLCODE || ' / ' || SQLERRM);
            application_log_insert('enqueue_corp_state', SYSDATE(), -1, SQLERRM);
    END;

    --
    -- Called from a trigger in COLIN_MGR_XXX to queue corp data that needs to be sent to the business search application.
    --
    PROCEDURE enqueue_corporation(p_corp_num VARCHAR2) IS
    BEGIN
        INSERT INTO triggered_corporation (id, corp_num) VALUES (triggered_corporation_seq.NEXTVAL, p_corp_num);
    EXCEPTION
        WHEN OTHERS THEN
            dbms_output.put_line('error: ' || SQLCODE || ' / ' || SQLERRM);
            application_log_insert('enqueue_corporation', SYSDATE(), -1, SQLERRM);
    END;
END trigger_handler;
/
