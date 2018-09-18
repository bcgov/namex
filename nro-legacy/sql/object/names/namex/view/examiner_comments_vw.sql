-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.EXAMINER_COMMENTS_VW;

CREATE OR REPLACE FORCE VIEW namex.examiner_comments_vw (request_id,
                                                         examiner_idir,
                                                         examiner_comment,
                                                         state_comment,
                                                         event_timestamp
                                                        )
AS
    SELECT rs.request_id, rs.examiner_idir, rs.examiner_comment, rs.state_comment,
           e.event_timestamp
      FROM request_state rs LEFT OUTER JOIN event e ON e.event_id = rs.start_event_id
           ;


DROP PUBLIC SYNONYM EXAMINER_COMMENTS_VW;

CREATE PUBLIC SYNONYM EXAMINER_COMMENTS_VW FOR NAMEX.EXAMINER_COMMENTS_VW;
