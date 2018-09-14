-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.REQUEST_STATE_VW;

create or replace view request_state_vw as
select  *
from request_state;


DROP PUBLIC SYNONYM REQUEST_STATE_VW;

CREATE PUBLIC SYNONYM REQUEST_STATE_VW FOR NAMEX.REQUEST_STATE_VW;
