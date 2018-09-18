-- noinspection SqlNoDataSourceInspectionForFile

INSERT INTO CONFIGURATION (application, name, value) VALUES
   ('NAMEX_FEEDER', 'destination_url', 'https://namex-dev.pathfinder.gov.bc.ca/api/v1/nro-extract/nro-requests');

INSERT INTO CONFIGURATION (application, name, value) VALUES
   ('SOLR_FEEDER', 'destination_url', 'https://namex-dev.pathfinder.gov.bc.ca/api/v1/feeds');
