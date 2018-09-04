-- noinspection SqlNoDataSourceInspectionForFile


create or replace view request_vw as
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

create or replace view submitter_vw as
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


create or replace view request_party_vw as
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

create or replace view examiner_comments_vw as
select rs.request_id,
    rs.examiner_IDIR,
    rs.examiner_comment,
    rs.state_comment,
    e.event_timestamp
from request_state rs
left outer join event e on e.event_id=rs.start_event_id
/

create or replace view names_vw as
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

create or replace view corp_nob_vw as
select ri.NATURE_BUSINESS_INFO,
    r.nr_num
from request_instance ri
inner join request r ON r.request_id = ri.request_id
/

CREATE or REPLACE VIEW req_instance_max_event
AS
SELECT request_id, MAX (event_timestamp) as last_update
FROM (
		select ri.request_id,
		       ri.start_event_id as event,
			  eri.event_timestamp as event_timestamp
		from request_instance ri
		left outer join event eri on eri.event_id = ri.start_event_id
		where ri.end_event_id IS NULL
	UNION 
		select rs.request_id,
		       rs.start_event_id as event,
			  ers.event_timestamp as event_timestamp
		from request_state rs
		left outer join event ers on ers.event_id = rs.start_event_id
		where rs.end_event_id IS NULL
	 UNION 
		select rp.request_id,
			   rp.start_event_id as event,
			  erp.event_timestamp as event_timestamp
		from request_party rp
		left outer join event erp on erp.event_id = rp.start_event_id
		where rp.end_event_id IS NULL
	UNION 
		select pn.request_id,
			   pn.start_event_id as event,
			  epn.event_timestamp as event_timestamp
		from partner_name_system pn
		left outer join event epn on epn.event_id = pn.start_event_id
		where pn.end_event_id IS NULL
	UNION 
		select n.request_id,
			  ni.start_event_id as event, 
			  eni.event_timestamp as event_timestamp
		from name n
		left outer join  name_instance ni on ni.name_id = n.name_id
		left outer join event eni on eni.event_id = ni.start_event_id
		where ni.end_event_id IS NULL
	UNION 
		select n.request_id,
			  ns.start_event_id as event, 
			  ens.event_timestamp as event_timestamp
		from name n
		left outer join name_state ns on ns.name_id = n.name_id
		left outer join event ens on ens.event_id = ns.start_event_id
		where ns.end_event_id IS NULL
)
GROUP BY request_id
/
