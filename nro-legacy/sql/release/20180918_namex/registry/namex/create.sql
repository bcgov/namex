-- noinspection SqlNoDataSourceInspectionForFile

@ ../../../../object/registry/namex/sequence/solr_feeder_id_seq.sql
@ ../../../../object/registry/namex/sequence/triggered_corp_name_seq.sql
@ ../../../../object/registry/namex/sequence/triggered_corp_state_seq.sql

@ ../../../../object/registry/namex/table/application_log.sql
@ ../../../../object/registry/namex/table/configuration.sql
@ ../../../../object/registry/namex/table/solr_feeder.sql
@ ../../../../object/registry/namex/table/triggered_corp_name.sql
@ ../../../../object/registry/namex/table/triggered_corp_state.sql

@ ../../../../object/registry/namex/view/address_vw.sql
@ ../../../../object/registry/namex/view/corp_jurs_vw.sql
@ ../../../../object/registry/namex/view/corp_nr_num_vw.sql
@ ../../../../object/registry/namex/view/corp_num_dts_class_vw.sql
@ ../../../../object/registry/namex/view/corp_party_vw.sql
@ ../../../../object/registry/namex/view/office_vw.sql
@ ../../../../object/registry/namex/view/solr_dataimport_conflicts_vw.sql

@ ../../../../object/registry/namex/procedure/application_log_insert.sql

@ ../../../../object/registry/namex/package/solr_pks.sql
@ ../../../../object/registry/namex/package/solr_pkb.sql
@ ../../../../object/registry/namex/package/trigger_handler_pks.sql
@ ../../../../object/registry/namex/package/trigger_handler_pkb.sql

@ ../../../../object/registry/namex/job/solr_outbound.sql

INSERT INTO CONFIGURATION (application, name, value, description) VALUES
   ('GLOBAL', 'oracle_wallet', 'file:/dsk01/app/oracle/product/rdbms/11.2.0.4/wallet', NULL);

CREATE PUBLIC SYNONYM namex_trigger_handler FOR namex.trigger_handler;
