-- noinspection SqlNoDataSourceInspectionForFile

CREATE OR REPLACE PACKAGE NAMEX.trigger_handler AS
    --
    -- Called from a trigger in COLIN_MGR_XXX to queue name data that needs to be sent to the namex application.
    --
    PROCEDURE enqueue_corp_name(p_corp_num VARCHAR2, p_corp_name_typ_cd CHAR, p_start_event_id INTEGER,
            p_corp_name_seq_num INTEGER);

    --
    -- Called from a trigger in COLIN_MGR_XXX to queue state data that needs to be sent to the namex application.
    --
    PROCEDURE enqueue_corp_state(p_corp_num VARCHAR2, p_start_event_id INTEGER);

    --
    -- Called from a trigger in COLIN_MGR_XXX to queue corporation/party data that needs to be sent to the search application.
    --
    PROCEDURE enqueue_corporation(p_corp_num VARCHAR2);
END trigger_handler;
/
