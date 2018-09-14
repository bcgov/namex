-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.SOLR_DATAIMPORT_NAMES_VW;

CREATE OR REPLACE FORCE VIEW namex.solr_dataimport_names_vw (ID,
                                                             name_instance_id,
                                                             choice_number,
                                                             corp_num,
                                                             NAME,
                                                             nr_num,
                                                             request_id,
                                                             submit_count,
                                                             request_type_cd,
                                                             name_id,
                                                             start_event_id,
                                                             name_state_type_cd
                                                            )
AS
    SELECT r.nr_num || '-' || ni.choice_number AS ID, ni.name_instance_id, ni.choice_number,
           ni.corp_num, ni.NAME, r.nr_num, r.request_id, r.submit_count, ri.request_type_cd,
           n.name_id, ni.start_event_id, ns.name_state_type_cd
      FROM request r INNER JOIN request_instance ri ON ri.request_id = r.request_id
           INNER JOIN request_state rs ON rs.request_id = r.request_id
           INNER JOIN NAME n ON n.request_id = r.request_id
           INNER JOIN name_instance ni ON ni.name_id = n.name_id
           INNER JOIN name_state ns ON ns.name_id = ni.name_id
           INNER JOIN event e ON e.event_id = ns.start_event_id
     WHERE ri.end_event_id IS NULL
       AND rs.end_event_id IS NULL
       AND ni.end_event_id IS NULL
       AND ns.end_event_id IS NULL
       AND ns.name_state_type_cd IN ('A', 'R', 'C')
       AND e.event_type_cd = 'EXAM';


DROP PUBLIC SYNONYM SOLR_DATAIMPORT_NAMES_VW;

CREATE PUBLIC SYNONYM SOLR_DATAIMPORT_NAMES_VW FOR NAMEX.SOLR_DATAIMPORT_NAMES_VW;
