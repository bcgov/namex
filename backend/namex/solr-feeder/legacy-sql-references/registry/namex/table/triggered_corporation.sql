-- noinspection SqlNoDataSourceInspectionForFile

DROP TABLE NAMEX.TRIGGERED_CORPORATION CASCADE CONSTRAINTS;

CREATE TABLE NAMEX.TRIGGERED_CORPORATION
(
  ID              INTEGER                       NOT NULL,
  CORP_NUM        VARCHAR2(10)                  NOT NULL,
  STATUS_SOLR     CHAR(1 BYTE)                  DEFAULT 'P'                   NOT NULL
);
