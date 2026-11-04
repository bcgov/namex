-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.CORP_NR_NUM_VW;

CREATE OR REPLACE FORCE VIEW namex.corp_nr_num_vw (corp_num, nr_num)
AS
    SELECT e.corp_num, f.nr_num
      FROM filing f INNER JOIN event e ON e.event_id = f.event_id
     WHERE f.nr_num IS NOT NULL;


DROP PUBLIC SYNONYM CORP_NR_NUM_VW;

CREATE PUBLIC SYNONYM CORP_NR_NUM_VW FOR NAMEX.CORP_NR_NUM_VW;
