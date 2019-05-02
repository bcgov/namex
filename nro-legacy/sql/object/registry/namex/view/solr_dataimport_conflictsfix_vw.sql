-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.SOLR_DATAIMPORT_CONFLICTSFIX_VW;

CREATE OR REPLACE FORCE VIEW namex.solr_dataimport_conflictsfix_vw (ID, NAME, state_type_cd, SOURCE)
AS
SELECT c.corp_num AS ID, corp.corp_nme AS NAME, op.state_typ_cd AS state_type_cd,
       'CORP' AS SOURCE
FROM corporation c LEFT OUTER JOIN corp_name corp ON corp.corp_num = c.corp_num
                   LEFT OUTER JOIN corp_state cs ON cs.corp_num = corp.corp_num
                   LEFT OUTER JOIN corp_op_state op ON op.state_typ_cd = cs.state_typ_cd
                   LEFT OUTER JOIN corp_type ct ON ct.corp_typ_cd = c.corp_typ_cd
WHERE corp.end_event_id IS NULL
  AND corp.corp_name_typ_cd IN ('CO', 'NB')
  AND cs.end_event_id IS NULL
  AND op.op_state_typ_cd = 'ACT'
  AND ct.corp_class IN ('BC', 'OT')
UNION ALL
SELECT c.corp_num AS ID, corp.corp_nme AS NAME, op.state_typ_cd AS state_type_cd,
       'CORP' AS SOURCE
FROM corporation c
         LEFT OUTER JOIN corp_name corp ON corp.corp_num = c.corp_num
         LEFT OUTER JOIN corp_state cs ON cs.corp_num = corp.corp_num
         LEFT OUTER JOIN corp_op_state op ON op.state_typ_cd = cs.state_typ_cd
         LEFT OUTER JOIN corp_type ct ON ct.corp_typ_cd = c.corp_typ_cd
WHERE corp.end_event_id IS NULL
  AND corp.corp_name_typ_cd IN ('CO')
  AND cs.end_event_id IS NULL
  AND op.op_state_typ_cd = 'ACT'
  AND ct.corp_class IN ('SOC', 'XPRO')
  AND c.corp_num NOT IN (SELECT cname.corp_num FROM corp_name cname
                         LEFT OUTER JOIN corporation c1 ON c1.corp_num = cname.corp_num
                         WHERE cname.corp_num = c.corp_num
                           AND cname.corp_name_typ_cd = 'AS' AND cname.end_event_id IS NULL)
UNION ALL
SELECT c.corp_num AS ID, corp.corp_nme AS NAME, op.state_typ_cd AS state_type_cd,
       'CORP' AS SOURCE
FROM corporation c
         LEFT OUTER JOIN corp_name corp ON corp.corp_num = c.corp_num
         LEFT OUTER JOIN corp_state cs ON cs.corp_num = corp.corp_num
         LEFT OUTER JOIN corp_op_state op ON op.state_typ_cd = cs.state_typ_cd
         LEFT OUTER JOIN corp_type ct ON ct.corp_typ_cd = c.corp_typ_cd
WHERE corp.end_event_id IS NULL
  AND corp.corp_name_typ_cd IN ('AS')
  AND cs.end_event_id IS NULL
  AND op.op_state_typ_cd = 'ACT'
  AND ct.corp_class IN ('SOC', 'XPRO');
