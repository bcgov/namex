-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.REQUEST_PARTY_VW;

CREATE OR REPLACE FORCE VIEW namex.request_party_vw (request_id,
                                                     last_name,
                                                     first_name,
                                                     middle_name,
                                                     phone_number,
                                                     fax_number,
                                                     email_address,
                                                     contact,
                                                     client_first_name,
                                                     client_last_name,
                                                     decline_notification_ind,
                                                     addr_line_1,
                                                     addr_line_2,
                                                     addr_line_3,
                                                     city,
                                                     postal_cd,
                                                     state_province_cd,
                                                     country_type_cd
                                                    )
AS
    SELECT rp.request_id, rp.last_name, rp.first_name, rp.middle_name, rp.phone_number,
           rp.fax_number, rp.email_address, rp.contact, rp.client_first_name, rp.client_last_name,
           rp.decline_notification_ind, addr.addr_line_1, addr.addr_line_2, addr.addr_line_3,
           addr.city, addr.postal_cd, addr.state_province_cd, addr.country_type_cd
      FROM request_party rp LEFT OUTER JOIN address@global_readonly addr
           ON addr.addr_id = rp.address_id
           LEFT OUTER JOIN request r ON r.request_id = rp.request_id
     WHERE rp.party_type_cd = 'APP';


DROP PUBLIC SYNONYM REQUEST_PARTY_VW;

CREATE PUBLIC SYNONYM REQUEST_PARTY_VW FOR NAMEX.REQUEST_PARTY_VW;
