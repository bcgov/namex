-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.REQ_INSTANCE_MAX_EVENT;

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
GROUP BY request_id;


DROP PUBLIC SYNONYM REQ_INSTANCE_MAX_EVENT;

CREATE PUBLIC SYNONYM REQ_INSTANCE_MAX_EVENT FOR NAMEX.REQ_INSTANCE_MAX_EVENT;
