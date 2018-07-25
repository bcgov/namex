-- noinspection SqlNoDataSourceInspectionForFile


create or replace view namex_request_vw as
select  r.request_id,
    r.nr_num,
    r.previous_request_id,
    r.submit_count,
    ri.priority_cd,
    ri.request_type_cd,
    ri.expiration_date,
    ri.additional_info,
    ri.nature_business_info,
    ri.xpro_jurisdiction
from request r
left outer join request_instance ri ON ri.request_id = r.request_id
/

create or replace view namex_submitter_vw as
select t.request_id,
    submit_event.event_timestamp submitted_date,
    CASE
      WHEN (t.BCOL_ACCOUNT_NUM IS NOT NULL)
        THEN  TO_CHAR(t.BCOL_ACCOUNT_NUM)|| '-' ||t.BCOL_RACF_ID
      WHEN (T.STAFF_IDIR IS NOT NULL)
        THEN T.STAFF_IDIR
    END submitter
from transaction t
left outer join event submit_event on submit_event.event_id = t.event_id
where t.transaction_type_cd in ('NRREQ', 'RESUBMIT')
/


create or replace view namex_request_party_vw as
select  rp.request_id,
    rp.last_name,
    rp.first_name,
    rp.middle_name,
    rp.phone_number,
    rp.fax_number,
    rp.email_address,
    rp.contact,
    rp.client_first_name,
    rp.client_last_name,
    rp.decline_notification_ind,
    addr.addr_line_1,
    addr.addr_line_2,
    addr.addr_line_3,
    addr.city,
    addr.postal_cd,
    addr.state_province_cd,
    addr.country_type_cd
from request_party rp
left outer join address@global_readonly addr ON addr.addr_id = rp.address_id
left outer join request r on r.request_id = rp.request_id
where rp.party_type_cd = 'APP'
/

create or replace view namex_examiner_comments_vw as
select rs.request_id,
    rs.examiner_IDIR,
    rs.examiner_comment,
    rs.state_comment,
    e.event_timestamp
from request_state rs
left outer join event e on e.event_id=rs.start_event_id
/

create or replace view namex_names_vw as
select nm.request_id,
    ni.choice_number,
    ni.name,
    ni.designation,
    ns.name_state_type_cd
from name_instance ni
left outer join name nm on nm.name_id=ni.name_id
left outer join name_state ns on ns.name_id=ni.name_id
where ns.end_event_id is null
 and ni.end_event_id is null
/

create or replace view namex_corp_nob_vw as
select ri.NATURE_BUSINESS_INFO,
    r.nr_num
from request_instance ri
inner join request r ON r.request_id = ri.request_id
/