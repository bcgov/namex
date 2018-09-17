DROP VIEW NAMEX.REQUEST_STATE_VW;

CREATE OR REPLACE FORCE VIEW namex.request_state_vw (request_state_id,
                                                     request_id,
                                                     state_type_cd,
                                                     start_event_id,
                                                     end_event_id,
                                                     examiner_idir,
                                                     examiner_comment,
                                                     state_comment,
                                                     batch_id
                                                    )
AS
    SELECT request_state_id, request_id, state_type_cd, start_event_id, end_event_id,
           examiner_idir, examiner_comment, state_comment, batch_id
      FROM request_state;


DROP PUBLIC SYNONYM REQUEST_STATE_VW;

CREATE PUBLIC SYNONYM REQUEST_STATE_VW FOR NAMEX.REQUEST_STATE_VW;
