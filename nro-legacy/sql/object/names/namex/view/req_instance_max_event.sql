-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.REQ_INSTANCE_MAX_EVENT;

CREATE OR REPLACE FORCE VIEW namex.req_instance_max_event (request_id, last_update)
AS
    SELECT   request_id, MAX (event_timestamp) AS last_update
        FROM (SELECT ri.request_id, ri.start_event_id AS event,
                     eri.event_timestamp AS event_timestamp
                FROM request_instance ri LEFT OUTER JOIN event eri ON eri.event_id =
                                                                                   ri.start_event_id
               WHERE ri.end_event_id IS NULL
              UNION
              SELECT rs.request_id, rs.start_event_id AS event,
                     ers.event_timestamp AS event_timestamp
                FROM request_state rs LEFT OUTER JOIN event ers ON ers.event_id = rs.start_event_id
               WHERE rs.end_event_id IS NULL
              UNION
              SELECT rp.request_id, rp.start_event_id AS event,
                     erp.event_timestamp AS event_timestamp
                FROM request_party rp LEFT OUTER JOIN event erp ON erp.event_id = rp.start_event_id
               WHERE rp.end_event_id IS NULL
              UNION
              SELECT pn.request_id, pn.start_event_id AS event,
                     epn.event_timestamp AS event_timestamp
                FROM partner_name_system pn LEFT OUTER JOIN event epn
                     ON epn.event_id = pn.start_event_id
               WHERE pn.end_event_id IS NULL
              UNION
              SELECT n.request_id, ni.start_event_id AS event,
                     eni.event_timestamp AS event_timestamp
                FROM NAME n LEFT OUTER JOIN name_instance ni ON ni.name_id = n.name_id
                     LEFT OUTER JOIN event eni ON eni.event_id = ni.start_event_id
               WHERE ni.end_event_id IS NULL
              UNION
              SELECT n.request_id, ns.start_event_id AS event,
                     ens.event_timestamp AS event_timestamp
                FROM NAME n LEFT OUTER JOIN name_state ns ON ns.name_id = n.name_id
                     LEFT OUTER JOIN event ens ON ens.event_id = ns.start_event_id
               WHERE ns.end_event_id IS NULL)
    GROUP BY request_id;


DROP PUBLIC SYNONYM REQ_INSTANCE_MAX_EVENT;

CREATE PUBLIC SYNONYM REQ_INSTANCE_MAX_EVENT FOR NAMEX.REQ_INSTANCE_MAX_EVENT;
