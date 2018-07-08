create or replace view namex_corp_nob_vw as 
select ri.NATURE_BUSINESS_INFO, 
    r.nr_num
from request_instance ri
inner join request r ON r.request_id = ri.request_id
/