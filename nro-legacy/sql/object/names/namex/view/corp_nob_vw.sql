-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.CORP_NOB_VW;

create or replace view corp_nob_vw as
select ri.NATURE_BUSINESS_INFO,
    r.nr_num
from request_instance ri
inner join request r ON r.request_id = ri.request_id;


DROP PUBLIC SYNONYM CORP_NOB_VW;

CREATE PUBLIC SYNONYM CORP_NOB_VW FOR NAMEX.CORP_NOB_VW;
