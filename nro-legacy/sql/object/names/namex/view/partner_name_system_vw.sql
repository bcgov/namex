-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.PARTNER_NAME_SYSTEM_VW;

create or replace view partner_name_system_vw as
select  *
from partner_name_system;


DROP PUBLIC SYNONYM PARTNER_NAME_SYSTEM_VW;

CREATE PUBLIC SYNONYM PARTNER_NAME_SYSTEM_VW FOR NAMEX.PARTNER_NAME_SYSTEM_VW;
