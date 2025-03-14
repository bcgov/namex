-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.CORP_JURS_VW;

CREATE OR REPLACE FORCE VIEW namex.corp_jurs_vw (corp_num, home_jurisdiction)
AS
    SELECT j.corp_num, j.can_jur_typ_cd || '-' || jt.full_desc AS home_jurisdiction
      FROM jurisdiction j INNER JOIN jurisdiction_type jt ON jt.can_jur_typ_cd = j.can_jur_typ_cd
     WHERE j.end_event_id IS NULL;


DROP PUBLIC SYNONYM CORP_JURS_VW;

CREATE PUBLIC SYNONYM CORP_JURS_VW FOR NAMEX.CORP_JURS_VW;
