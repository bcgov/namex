-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.EXAMINER_COMMENTS_VW;

create or replace view examiner_comments_vw as
select rs.request_id,
    rs.examiner_IDIR,
    rs.examiner_comment,
    rs.state_comment,
    e.event_timestamp
from request_state rs
left outer join event e on e.event_id=rs.start_event_id;


DROP PUBLIC SYNONYM EXAMINER_COMMENTS_VW;

CREATE PUBLIC SYNONYM EXAMINER_COMMENTS_VW FOR NAMEX.EXAMINER_COMMENTS_VW;
