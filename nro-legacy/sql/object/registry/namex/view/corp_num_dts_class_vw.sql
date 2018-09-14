-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.CORP_NUM_DTS_CLASS_VW;

create or replace view corp_num_dts_class_vw as
select c.corp_num, 
    c.recognition_dts, 
    ct.corp_class 
from corporation c
left outer join corp_name corp on corp.corp_num = c.corp_num
left outer join corp_type ct ON ct.corp_typ_cd = c.corp_typ_cd
where corp.end_event_id IS NULL and corp.corp_name_seq_num = 0;

DROP PUBLIC SYNONYM CORP_NUM_DTS_CLASS_VW;

CREATE PUBLIC SYNONYM CORP_NUM_DTS_CLASS_VW FOR NAMEX.CORP_NUM_DTS_CLASS_VW;
