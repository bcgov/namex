-- noinspection SqlNoDataSourceInspectionForFile

INSERT INTO CONFIGURATION (application, name, value, description) VALUES
   ('SOLR_FEEDER', 'destination_url', 'https://namex.pathfinder.gov.bc.ca/api/v1/feeds', NULL);

GRANT INSERT ON application_log TO colin_mgr_prd;
GRANT INSERT ON triggered_corp_name TO colin_mgr_prd;
GRANT INSERT ON triggered_corp_state TO colin_mgr_prd;

GRANT EXECUTE ON trigger_handler TO colin_mgr_prd;
GRANT EXECUTE ON application_log_insert TO colin_mgr_prd;
