-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.CORP_PARTY_VW;

CREATE OR REPLACE FORCE VIEW namex.corp_party_vw (corp_party_id,
                                                  mailing_addr_id,
                                                  delivery_addr_id,
                                                  corp_num,
                                                  party_typ_cd,
                                                  start_event_id,
                                                  end_event_id,
                                                  prev_party_id,
                                                  corr_typ_cd,
                                                  last_report_dt,
                                                  appointment_dt,
                                                  cessation_dt,
                                                  last_nme,
                                                  middle_nme,
                                                  first_nme,
                                                  business_nme,
                                                  bus_company_num,
                                                  email_address,
                                                  corp_party_seq_num,
                                                  office_notification_dt,
                                                  phone,
                                                  reason_typ_cd
                                                 )
AS
    SELECT corp_party_id, mailing_addr_id, delivery_addr_id, corp_num, party_typ_cd, start_event_id,
           end_event_id, prev_party_id, corr_typ_cd, last_report_dt, appointment_dt, cessation_dt,
           last_nme, middle_nme, first_nme, business_nme, bus_company_num, email_address,
           corp_party_seq_num, office_notification_dt, phone, reason_typ_cd
      FROM corp_party;


DROP PUBLIC SYNONYM CORP_PARTY_VW;

CREATE PUBLIC SYNONYM CORP_PARTY_VW FOR NAMEX.CORP_PARTY_VW;
