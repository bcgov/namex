-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.PARTNER_NAME_SYSTEM_VW;

CREATE OR REPLACE FORCE VIEW namex.partner_name_system_vw (partner_name_system_id,
                                                           request_id,
                                                           start_event_id,
                                                           end_event_id,
                                                           partner_name_type_cd,
                                                           partner_name_number,
                                                           partner_jurisdiction_type_cd,
                                                           partner_name_date,
                                                           partner_name,
                                                           partner_transaction_id,
                                                           last_update_id
                                                          )
AS
    SELECT partner_name_system_id, request_id, start_event_id, end_event_id, partner_name_type_cd,
           partner_name_number, partner_jurisdiction_type_cd, partner_name_date, partner_name,
           partner_transaction_id, last_update_id
      FROM partner_name_system;


DROP PUBLIC SYNONYM PARTNER_NAME_SYSTEM_VW;

CREATE PUBLIC SYNONYM PARTNER_NAME_SYSTEM_VW FOR NAMEX.PARTNER_NAME_SYSTEM_VW;
