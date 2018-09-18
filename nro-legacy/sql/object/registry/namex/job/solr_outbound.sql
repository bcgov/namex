-- noinspection SqlNoDataSourceInspectionForFile

BEGIN
      DBMS_SCHEDULER.create_job (
      job_name => 'SOLR_OUTBOUND',
      job_type => 'STORED_PROCEDURE',
      job_action => 'solr.feed_solr',
      start_date => SYSDATE,
      repeat_interval => 'freq=MINUTELY; INTERVAL=1',
      end_date => NULL,
      enabled => FALSE,
      comments => 'Send to Solr');
END;
/
