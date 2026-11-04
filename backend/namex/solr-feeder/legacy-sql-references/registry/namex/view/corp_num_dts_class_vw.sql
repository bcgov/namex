-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.CORP_NUM_DTS_CLASS_VW;

CREATE OR REPLACE FORCE VIEW namex.corp_num_dts_class_vw (corp_num, recognition_dts, corp_class)
AS
    SELECT c.corp_num, c.recognition_dts, ct.corp_class
      FROM corporation c LEFT OUTER JOIN corp_name corp ON corp.corp_num = c.corp_num
           LEFT OUTER JOIN corp_type ct ON ct.corp_typ_cd = c.corp_typ_cd
     WHERE corp.end_event_id IS NULL AND corp.corp_name_seq_num = 0;


DROP PUBLIC SYNONYM CORP_NUM_DTS_CLASS_VW;

CREATE PUBLIC SYNONYM CORP_NUM_DTS_CLASS_VW FOR NAMEX.CORP_NUM_DTS_CLASS_VW;
