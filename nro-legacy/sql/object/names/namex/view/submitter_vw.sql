-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.SUBMITTER_VW;

create or replace view submitter_vw as
select t.request_id,
    submit_event.event_timestamp submitted_date,
    CASE
      WHEN (t.BCOL_ACCOUNT_NUM IS NOT NULL)
        THEN  TO_CHAR(t.BCOL_ACCOUNT_NUM)|| '-' ||t.BCOL_RACF_ID
      WHEN (T.STAFF_IDIR IS NOT NULL)
        THEN T.STAFF_IDIR
    END submitter
from transaction t
left outer join event submit_event on submit_event.event_id = t.event_id
where t.transaction_type_cd in ('NRREQ', 'RESUBMIT');


DROP PUBLIC SYNONYM NAMEX_SUBMITTER_VW;

CREATE PUBLIC SYNONYM NAMEX_SUBMITTER_VW FOR NAMEX.SUBMITTER_VW;
