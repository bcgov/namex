-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.SOLR_DATAIMPORT_CONFLICTS_VW;

CREATE OR REPLACE FORCE VIEW namex.solr_dataimport_conflicts_vw (id, name, state_type_cd, source, start_date, jurisdiction)
AS
SELECT c.corp_num AS id, corp.corp_nme AS name, op.state_typ_cd AS state_type_cd,
       'CORP' AS source, C.RECOGNITION_DTS AS start_date,
	case 
             when j.can_jur_typ_cd IS NULL
                then 'BC'
             when j.can_jur_typ_cd = 'OT'
                then j.othr_juris_desc
             else j.can_jur_typ_cd
        end AS jurisdiction
FROM corporation c LEFT OUTER JOIN corp_name corp ON corp.corp_num = c.corp_num
                   LEFT OUTER JOIN corp_state cs ON cs.corp_num = corp.corp_num
                   LEFT OUTER JOIN corp_op_state op ON op.state_typ_cd = cs.state_typ_cd
                   LEFT OUTER JOIN corp_type ct ON ct.corp_typ_cd = c.corp_typ_cd
                   LEFT OUTER JOIN jurisdiction j ON j.corp_num = c.corp_num
WHERE corp.end_event_id IS NULL
  AND corp.corp_name_typ_cd IN ('CO', 'NB')
  AND cs.end_event_id IS NULL
  AND j.end_event_id IS NULL
  AND op.op_state_typ_cd = 'ACT'
  AND ct.corp_class IN ('BC', 'SOC', 'OT')
UNION ALL
SELECT c.corp_num AS id, corp.corp_nme AS name, op.state_typ_cd AS state_type_cd,
       'CORP' AS source, C.RECOGNITION_DTS AS start_date,
	case 
             when j.can_jur_typ_cd IS NULL
                then 'BC'
             when j.can_jur_typ_cd = 'OT'
                then j.othr_juris_desc
             else j.can_jur_typ_cd
        end AS jurisdiction
FROM corporation c
         LEFT OUTER JOIN corp_name corp ON corp.corp_num = c.corp_num
         LEFT OUTER JOIN corp_state cs ON cs.corp_num = corp.corp_num
         LEFT OUTER JOIN corp_op_state op ON op.state_typ_cd = cs.state_typ_cd
         LEFT OUTER JOIN corp_type ct ON ct.corp_typ_cd = c.corp_typ_cd
         LEFT OUTER JOIN jurisdiction j ON j.corp_num = c.corp_num
WHERE corp.end_event_id IS NULL
  AND corp.corp_name_typ_cd IN ('CO')
  AND cs.end_event_id IS NULL
  AND j.end_event_id IS NULL
  AND op.op_state_typ_cd = 'ACT'
  AND ct.corp_class IN ('XPRO')
  and c.corp_num NOT IN (select cname.corp_num   from corp_name cname
                         left outer join corporation c1 on c1.corp_num = cname.corp_num
                         where cname.corp_num = c.corp_num
                           and cname.corp_name_typ_cd ='AS' and cname.end_event_id IS NULL)
UNION ALL
SELECT c.corp_num AS id, corp.corp_nme AS name, op.state_typ_cd AS state_type_cd,
       'CORP' AS source, C.RECOGNITION_DTS AS start_date,
        case 
             when j.can_jur_typ_cd IS NULL
                then 'BC'
             when j.can_jur_typ_cd = 'OT'
                then j.othr_juris_desc
             else j.can_jur_typ_cd
          end AS jurisdiction
FROM corporation c
         LEFT OUTER JOIN corp_name corp ON corp.corp_num = c.corp_num
         LEFT OUTER JOIN corp_state cs ON cs.corp_num = corp.corp_num
         LEFT OUTER JOIN corp_op_state op ON op.state_typ_cd = cs.state_typ_cd
         LEFT OUTER JOIN corp_type ct ON ct.corp_typ_cd = c.corp_typ_cd
         LEFT OUTER JOIN jurisdiction j ON j.corp_num = c.corp_num
WHERE corp.end_event_id IS NULL
  AND corp.corp_name_typ_cd IN ('AS')
  AND cs.end_event_id IS NULL
  AND j.end_event_id IS NULL
  AND op.op_state_typ_cd = 'ACT'
  AND ct.corp_class IN ('XPRO');


