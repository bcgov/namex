-- noinspection SqlNoDataSourceInspectionForFile

BEGIN
      DBMS_SCHEDULER.create_job (
      job_name => 'NAMEX_OUTBOUND',
      job_type => 'STORED_PROCEDURE',
      job_action => 'namex.feed_namex',
      start_date => SYSDATE,
      repeat_interval => 'freq=MINUTELY; INTERVAL=1',
      end_date => NULL,
      enabled => FALSE,
      comments => 'Send a NR to NameX');
END;
/
