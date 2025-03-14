-- noinspection SqlNoDataSourceInspectionForFile

@ ../../../../object/names/namex/sequence/namex_feeder_id_seq.sql
@ ../../../../object/names/namex/sequence/solr_feeder_id_seq.sql

@ ../../../../object/names/namex/table/application_log.sql
@ ../../../../object/names/namex/table/configuration.sql
@ ../../../../object/names/namex/table/name_transaction.sql
@ ../../../../object/names/namex/table/namex_feeder.sql
@ ../../../../object/names/namex/table/solr_feeder.sql

@ ../../../../object/names/namex/view/corp_jurs_vw.sql
@ ../../../../object/names/namex/view/corp_nob_vw.sql
@ ../../../../object/names/namex/view/corp_nr_num_vw.sql
@ ../../../../object/names/namex/view/corp_num_dts_class_vw.sql
@ ../../../../object/names/namex/view/examiner_comments_vw.sql
@ ../../../../object/names/namex/view/names_vw.sql
@ ../../../../object/names/namex/view/nr_max_event.sql
@ ../../../../object/names/namex/view/partner_name_system_vw.sql
@ ../../../../object/names/namex/view/req_instance_max_event.sql
@ ../../../../object/names/namex/view/request_party_vw.sql
@ ../../../../object/names/namex/view/request_state_vw.sql
@ ../../../../object/names/namex/view/request_vw.sql
@ ../../../../object/names/namex/view/solr_dataimport_conflicts_vw.sql
@ ../../../../object/names/namex/view/solr_dataimport_names_vw.sql
@ ../../../../object/names/namex/view/submitter_vw.sql

@ ../../../../object/names/namex/procedure/application_log_insert.sql

@ ../../../../object/names/namex/package/namex_pks.sql
@ ../../../../object/names/namex/package/namex_pkb.sql
@ ../../../../object/names/namex/package/solr_pks.sql
@ ../../../../object/names/namex/package/solr_pkb.sql
@ ../../../../object/names/namex/package/trigger_handler_pks.sql
@ ../../../../object/names/namex/package/trigger_handler_pkb.sql

@ ../../../../object/names/namex/job/namex_outbound.sql
@ ../../../../object/names/namex/job/solr_outbound.sql

INSERT INTO CONFIGURATION (application, name, value, description) VALUES
   ('GLOBAL', 'oracle_wallet', 'file:/dsk01/app/oracle/product/rdbms/11.2.0.4/wallet', NULL);

GRANT EXECUTE ON application_log_insert TO namesdb;
GRANT EXECUTE ON trigger_handler TO namesdb;
CREATE PUBLIC SYNONYM namex_trigger_handler FOR namex.trigger_handler;
