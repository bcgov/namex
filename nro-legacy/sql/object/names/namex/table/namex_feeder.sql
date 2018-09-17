-- noinspection SqlNoDataSourceInspectionForFile

DROP TABLE NAMEX.NAMEX_FEEDER CASCADE CONSTRAINTS;

CREATE TABLE NAMEX.NAMEX_FEEDER
(
  ID              NUMBER(10)                    NOT NULL,
  TRANSACTION_ID  NUMBER(10)                    NOT NULL,
  STATUS          CHAR(1 BYTE)                  DEFAULT 'P'                   NOT NULL,
  NR_NUM          VARCHAR2(10 BYTE),
  ACTION          CHAR(1 BYTE),
  SEND_COUNT      NUMBER(10)                    DEFAULT 0,
  SEND_TIME       TIMESTAMP(6),
  ERROR_MSG       VARCHAR2(4000 BYTE)
);
