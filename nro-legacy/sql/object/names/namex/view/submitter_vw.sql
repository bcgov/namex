-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.SUBMITTER_VW;

CREATE OR REPLACE FORCE VIEW namex.submitter_vw (request_id, submitted_date, submitter)
AS
    SELECT t.request_id, submit_event.event_timestamp submitted_date,
           CASE
               WHEN (t.bcol_account_num IS NOT NULL)
                   THEN TO_CHAR (t.bcol_account_num) || '-' || t.bcol_racf_id
               WHEN (t.staff_idir IS NOT NULL)
                   THEN t.staff_idir
           END submitter
      FROM TRANSACTION t LEFT OUTER JOIN event submit_event ON submit_event.event_id = t.event_id
     WHERE t.transaction_type_cd IN ('NRREQ', 'RESUBMIT');


DROP PUBLIC SYNONYM NAMEX_SUBMITTER_VW;

CREATE PUBLIC SYNONYM NAMEX_SUBMITTER_VW FOR NAMEX.SUBMITTER_VW;
