-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.NR_MAX_EVENT;

CREATE OR REPLACE FORCE VIEW namex.nr_max_event (nr_num, last_update)
AS
    SELECT   nr_num, MAX (event_timestamp) AS last_update
        FROM (SELECT r.nr_num, ri.start_event_id AS event, eri.event_timestamp AS event_timestamp
                FROM request r LEFT OUTER JOIN request_instance ri ON ri.request_id = r.request_id
                     LEFT OUTER JOIN event eri ON eri.event_id = ri.start_event_id
               WHERE ri.end_event_id IS NULL
              UNION
              SELECT r.nr_num, rs.start_event_id AS event, ers.event_timestamp AS event_timestamp
                FROM request r LEFT OUTER JOIN request_state rs ON rs.request_id = r.request_id
                     LEFT OUTER JOIN event ers ON ers.event_id = rs.start_event_id
               WHERE rs.end_event_id IS NULL
              UNION
              SELECT r.nr_num, rp.start_event_id AS event, erp.event_timestamp AS event_timestamp
                FROM request r LEFT OUTER JOIN request_party rp ON rp.request_id = r.request_id
                     LEFT OUTER JOIN event erp ON erp.event_id = rp.start_event_id
               WHERE rp.end_event_id IS NULL
              UNION
              SELECT r.nr_num, pn.start_event_id AS event, epn.event_timestamp AS event_timestamp
                FROM request r LEFT OUTER JOIN partner_name_system pn ON pn.request_id =
                                                                                        r.request_id
                     LEFT OUTER JOIN event epn ON epn.event_id = pn.start_event_id
               WHERE pn.end_event_id IS NULL
              UNION
              SELECT r.nr_num, ni.start_event_id AS event, eni.event_timestamp AS event_timestamp
                FROM request r LEFT OUTER JOIN NAME n ON n.request_id = r.request_id
                     LEFT OUTER JOIN name_instance ni ON ni.name_id = n.name_id
                     LEFT OUTER JOIN event eni ON eni.event_id = ni.start_event_id
               WHERE ni.end_event_id IS NULL
              UNION
              SELECT r.nr_num, ns.start_event_id AS event, ens.event_timestamp AS event_timestamp
                FROM request r LEFT OUTER JOIN NAME n ON n.request_id = r.request_id
                     LEFT OUTER JOIN name_state ns ON ns.name_id = n.name_id
                     LEFT OUTER JOIN event ens ON ens.event_id = ns.start_event_id
               WHERE ns.end_event_id IS NULL)
    GROUP BY nr_num;


DROP PUBLIC SYNONYM NR_MAX_EVENT;

CREATE PUBLIC SYNONYM NR_MAX_EVENT FOR NAMEX.NR_MAX_EVENT;
