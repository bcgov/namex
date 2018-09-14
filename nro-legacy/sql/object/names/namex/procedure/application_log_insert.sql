-- noinspection SqlNoDataSourceInspectionForFile

CREATE OR REPLACE PROCEDURE NAMEX."APPLICATION_LOG_INSERT"
  --
  -- This was lifted in whole from NAMESDB.
  --
  ( p_program_name VARCHAR2
  , p_log_date     DATE
  , p_error_code   NUMBER
  , p_log_message  VARCHAR2) AS

  PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
  DBMS_OUTPUT.PUT_LINE('APPLICATION_LOG> Program Name: ' || p_program_name || ', Log Date: ' || TO_CHAR(p_log_date, 'DD-MON-YYYY HH24:MI:SS'));

  INSERT INTO application_log
  VALUES
  ( p_program_name
  , p_log_date
  , p_error_code
  , p_log_message);

  COMMIT;

EXCEPTION
  WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('EXCEPTION in APPLICATION_LOG_INSERT> sqlcode: ' || SQLCODE);

END application_log_insert;
/
