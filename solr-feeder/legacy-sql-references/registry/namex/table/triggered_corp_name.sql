-- noinspection SqlNoDataSourceInspectionForFile

DROP TABLE NAMEX.TRIGGERED_CORP_NAME CASCADE CONSTRAINTS;

CREATE TABLE NAMEX.TRIGGERED_CORP_NAME
(
  ID                INTEGER                       NOT NULL,
  CORP_NUM          VARCHAR2(10 BYTE)             NOT NULL,
  CORP_NAME_TYP_CD  CHAR(2 BYTE)                  NOT NULL,
  START_EVENT_ID    INTEGER                       NOT NULL,
  CORP_NAME_SEQ_NUM INTEGER                       NOT NULL,
  STATUS_SOLR       CHAR(1 BYTE)                  DEFAULT 'P'                   NOT NULL,
  STATUS_NAMEX      CHAR(1 BYTE)                  DEFAULT 'P'                   NOT NULL
);
