-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.REQUEST_VW;

CREATE OR REPLACE FORCE VIEW namex.request_vw (request_id,
                                               nr_num,
                                               previous_request_id,
                                               submit_count,
                                               priority_cd,
                                               request_type_cd,
                                               expiration_date,
                                               additional_info,
                                               nature_business_info,
                                               xpro_jurisdiction
                                              )
AS
    SELECT r.request_id, r.nr_num, r.previous_request_id, r.submit_count, ri.priority_cd,
           ri.request_type_cd, ri.expiration_date, ri.additional_info, ri.nature_business_info,
           ri.xpro_jurisdiction
      FROM request r LEFT OUTER JOIN request_instance ri ON ri.request_id = r.request_id
      WHERE ri.end_event_id IS NULL
           ;


DROP PUBLIC SYNONYM REQUEST_VW;

CREATE PUBLIC SYNONYM REQUEST_VW FOR NAMEX.REQUEST_VW;
