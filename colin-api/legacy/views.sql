
create or replace view namex_corp_nr_num_vw as 
select e.corp_num, 
    f.nr_num
from filing f
inner join event e ON e.event_id = f.event_id
where f.nr_num IS NOT NULL
/

create or replace view namex_corp_nob_vw as 
select ri.NATURE_BUSINESS_INFO, 
    r.nr_num
from request_instance ri
inner join request r ON r.request_id = ri.request_id
/

create or replace view namex_corp_num_dts_class_vw as
select c.corp_num, 
    c.recognition_dts, 
    ct.corp_class 
from corporation c
left outer join corp_name corp on corp.corp_num = c.corp_num
left outer join corp_type ct ON ct.corp_typ_cd = c.corp_typ_cd
where corp.end_event_id IS NULL and corp.corp_name_seq_num = 0
/

create or replace view namex_corp_jurs_vw as
select j.corp_num, j.can_jur_typ_cd||'-'||jt.full_desc  home_jurisdiction
from jurisdiction j
inner join jurisdiction_type jt ON jt.can_jur_typ_cd = j.can_jur_typ_cd
where j.end_event_id IS NULL
/