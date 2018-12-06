-- noinspection SqlNoDataSourceInspectionForFile

DECLARE
   job_doesnt_exist EXCEPTION;
   PRAGMA EXCEPTION_INIT( job_doesnt_exist, -27475 );
BEGIN
   dbms_scheduler.drop_job(job_name => 'NAMEX_OUTBOUND');
EXCEPTION WHEN job_doesnt_exist THEN
   null;
END;
/


BEGIN
      DBMS_SCHEDULER.create_job (
      job_name => 'NAMEX_OUTBOUND',
      job_type => 'STORED_PROCEDURE',
      job_action => 'namex.queue_data_for_namex',
      start_date => SYSDATE,
      repeat_interval => 'freq=MINUTELY; INTERVAL=1',
      end_date => NULL,
      enabled => FALSE,
      comments => 'Send a NR to NameX');
END;
/
