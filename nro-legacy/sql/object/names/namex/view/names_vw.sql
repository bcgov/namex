-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.NAMES_VW;

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
 and ni.end_event_id is null;


DROP PUBLIC SYNONYM NAMES_VW;

CREATE PUBLIC SYNONYM NAMES_VW FOR NAMEX.NAMES_VW;
