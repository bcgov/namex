-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.NR_CREATION_DATE_VW;

CREATE OR REPLACE FORCE VIEW namex.nr_creation_date_vw (request_id,
                                                        nr_num,
                                                        create_date,
                                                        event_timestamp,
                                                        submit_count,
                                                        request_type_cd
                                                        )
AS
    SELECT request_id, nr_num, TRUNC(event_timestamp) AS create_date, event_timestamp, submit_count, request_type_cd
    FROM request
        NATURAL JOIN transaction
        NATURAL JOIN event
        NATURAL JOIN request_instance
    WHERE
        transaction_type_cd = 'NRREQ'
        AND request_instance.start_event_id = event_id;


DROP PUBLIC SYNONYM NR_CREATION_DATE_VW;

CREATE PUBLIC SYNONYM NR_CREATION_DATE_VW FOR NAMEX.NR_CREATION_DATE_VW;
