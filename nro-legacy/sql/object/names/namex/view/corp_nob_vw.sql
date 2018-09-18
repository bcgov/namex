-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.CORP_NOB_VW;

CREATE OR REPLACE FORCE VIEW namex.corp_nob_vw (nature_business_info, nr_num)
AS
    SELECT ri.nature_business_info, r.nr_num
      FROM request_instance ri INNER JOIN request r ON r.request_id = ri.request_id
           ;


DROP PUBLIC SYNONYM CORP_NOB_VW;

CREATE PUBLIC SYNONYM CORP_NOB_VW FOR NAMEX.CORP_NOB_VW;
