-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.SOLR_DATAIMPORT_NAMES_VW;

CREATE OR REPLACE FORCE VIEW namex.solr_dataimport_names_vw (id,
                                                             name,
                                                             nr_num,
                                                             submit_count,
                                                             name_state_type_cd,
                                                             start_date,
                                                             jurisdiction
                                                            )
AS
    SELECT r.nr_num || '-' || ni.choice_number AS ID, 
            ni.NAME, r.nr_num, r.submit_count, ns.name_state_type_cd, te.event_timestamp as start_date,
      case 
             when ri.xpro_jurisdiction is not null
                then  ri.xpro_jurisdiction
                else 'BC'
           end AS JURISDICTION
      FROM request r 
           INNER JOIN request_instance ri ON ri.request_id = r.request_id
           INNER JOIN request_state rs ON rs.request_id = r.request_id
           INNER JOIN NAME n ON n.request_id = r.request_id
           INNER JOIN name_instance ni ON ni.name_id = n.name_id
           INNER JOIN name_state ns ON ns.name_id = ni.name_id
           INNER JOIN event e ON e.event_id = ns.start_event_id
           INNER JOIN transaction t ON t.request_id = r.request_id
           INNER JOIN event te ON te.event_id = t.event_id
     WHERE ri.end_event_id IS NULL
       AND rs.end_event_id IS NULL
       AND ni.end_event_id IS NULL
       AND ns.end_event_id IS NULL
       AND ns.name_state_type_cd IN ('A', 'R', 'C')
       AND t.transaction_type_cd = 'NRREQ';
