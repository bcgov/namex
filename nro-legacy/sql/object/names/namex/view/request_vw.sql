-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.REQUEST_VW;

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
left outer join request_instance ri ON ri.request_id = r.request_id;


DROP PUBLIC SYNONYM REQUEST_VW;

CREATE PUBLIC SYNONYM REQUEST_VW FOR NAMEX.REQUEST_VW;
