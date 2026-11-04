-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.OFFICE_VW;

CREATE OR REPLACE FORCE VIEW namex.office_vw (corp_num,
                                              office_typ_cd,
                                              start_event_id,
                                              end_event_id,
                                              mailing_addr_id,
                                              delivery_addr_id,
                                              dd_corp_num,
                                              email_address
                                             )
AS
    SELECT corp_num, office_typ_cd, start_event_id,
            end_event_id, mailing_addr_id, delivery_addr_id,
           dd_corp_num, email_address
      FROM office;


DROP PUBLIC SYNONYM OFFICE_VW;

CREATE PUBLIC SYNONYM OFFICE_VW FOR NAMEX.OFFICE_VW;
