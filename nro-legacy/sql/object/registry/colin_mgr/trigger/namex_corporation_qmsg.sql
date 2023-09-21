-- noinspection SqlNoDataSourceInspectionForFile

DROP TRIGGER NAMEX_CORPORATION_QMSG;

CREATE OR REPLACE TRIGGER namex_corporation_qmsg AFTER INSERT or UPDATE ON CORPORATION FOR EACH ROW
BEGIN
    if (nvl(:old.bn_9            ,'^') <> nvl(:new.bn_9             ,'^')
     or nvl(:old.bn_15           ,'^') <> nvl(:new.bn_15            ,'^')
     or nvl(:old.corp_typ_cd     ,'^') <> nvl(:new.corp_typ_cd      ,'^')
     or nvl(:old.last_ar_filed_dt,'^') <> nvl(:new.last_ar_filed_dt ,'^')
     or nvl(:old.transition_dt   ,'^') <> nvl(:new.transition_dt    ,'^')) then
        namex_trigger_handler.enqueue_corporation(:new.corp_num);
    end if;

    EXCEPTION
        WHEN OTHERS THEN
            application_log_insert('namex_corporation_qmsg', SYSDATE, -1, SQLERRM);
END;
/
