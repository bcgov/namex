-- noinspection SqlNoDataSourceInspectionForFile

INSERT INTO CONFIGURATION (application, name, value, description) VALUES
   ('NAMEX_FEEDER', 'destination_url', 'https://namex-dev.pathfinder.gov.bc.ca/api/v1/nro-extract/nro-requests', NULL);

INSERT INTO CONFIGURATION (application, name, value, description) VALUES
   ('SOLR_FEEDER', 'destination_url', 'https://namex-dev.pathfinder.gov.bc.ca/api/v1/feeds', NULL);
