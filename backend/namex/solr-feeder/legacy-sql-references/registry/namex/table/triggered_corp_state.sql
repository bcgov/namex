-- noinspection SqlNoDataSourceInspectionForFile

DROP TABLE NAMEX.TRIGGERED_CORP_STATE CASCADE CONSTRAINTS;

CREATE TABLE NAMEX.TRIGGERED_CORP_STATE
(
  ID              INTEGER                       NOT NULL,
  CORP_NUM        VARCHAR2(10)                  NOT NULL,
  START_EVENT_ID  INTEGER                       NOT NULL,
  STATUS_SOLR     CHAR(1 BYTE)                  DEFAULT 'P'                   NOT NULL,
  STATUS_NAMEX    CHAR(1 BYTE)                  DEFAULT 'P'                   NOT NULL
);


GRANT INSERT ON NAMEX.TRIGGERED_CORP_STATE TO COLIN_MGR_UAT;
