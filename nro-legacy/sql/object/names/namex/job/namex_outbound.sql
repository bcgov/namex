begin
      DBMS_SCHEDULER.create_job (
      job_name => 'NAMEX_OUTBOUND',
      job_type => 'STORED_PROCEDURE',
      job_action => 'namex.feed_namex',
      start_date => sysdate,
      repeat_interval => 'freq=MINUTELY; INTERVAL=1',
      end_date => NULL,
      enabled => TRUE,
      comments => 'Send a NR to NameX');
end;
/
