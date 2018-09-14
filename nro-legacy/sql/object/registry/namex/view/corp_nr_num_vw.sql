-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.CORP_NR_NUM_VW;

create or replace view corp_nr_num_vw as
select e.corp_num, 
    f.nr_num
from filing f
inner join event e ON e.event_id = f.event_id
where f.nr_num IS NOT NULL;

DROP PUBLIC SYNONYM CORP_NR_NUM_VW;

CREATE PUBLIC SYNONYM CORP_NR_NUM_VW FOR NAMEX.CORP_NR_NUM_VW;
