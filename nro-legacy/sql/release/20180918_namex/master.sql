-- noinspection SqlNoDataSourceInspectionForFile

-- Dependencies
@ names/namex/create.sql
@ names/namesdb/create.sql

-- Dependencies
@ registry/namex/create.sql
-- One will succeed. Too lazy?
GRANT EXECUTE ON trigger_handler TO colin_mgr_dev
GRANT EXECUTE ON trigger_handler TO colin_mgr_tst
GRANT EXECUTE ON trigger_handler TO colin_mgr_uat
GRANT EXECUTE ON trigger_handler TO colin_mgr_prd
@ registry/colin_mgr/create.sql
