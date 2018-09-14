-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.CORP_JURS_VW;

create or replace view corp_jurs_vw as
select j.corp_num, j.can_jur_typ_cd||'-'||jt.full_desc  home_jurisdiction
from jurisdiction j
inner join jurisdiction_type jt ON jt.can_jur_typ_cd = j.can_jur_typ_cd
where j.end_event_id IS NULL;


DROP PUBLIC SYNONYM CORP_JURS_VW;

CREATE PUBLIC SYNONYM CORP_JURS_VW FOR NAMEX.CORP_JURS_VW;
