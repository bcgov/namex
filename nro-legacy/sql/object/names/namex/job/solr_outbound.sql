begin
      DBMS_SCHEDULER.create_job (
      job_name => 'SOLR_OUTBOUND',
      job_type => 'STORED_PROCEDURE',
      job_action => 'solr.feed_solr',
      start_date => sysdate,
      repeat_interval => 'freq=MINUTELY; INTERVAL=1',
      end_date => NULL,
      enabled => TRUE,
      comments => 'Send to Solr');
end;
/
