-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.SOLR_DATAIMPORT_CONFLICTS_VW;

CREATE OR REPLACE FORCE VIEW namex.solr_dataimport_conflicts_vw (ID, NAME, state_type_cd, SOURCE)
AS
    SELECT r.nr_num AS ID, ni.NAME, ns.name_state_type_cd AS state_type_cd, 'NR' AS SOURCE
      FROM request r INNER JOIN request_instance ri ON ri.request_id = r.request_id
           INNER JOIN NAME n ON n.request_id = r.request_id
           INNER JOIN name_instance ni ON ni.name_id = n.name_id
           INNER JOIN name_state ns ON ns.name_id = ni.name_id
           INNER JOIN event e ON e.event_id = ns.start_event_id
     WHERE ri.end_event_id IS NULL
       AND ni.end_event_id IS NULL
       AND ns.end_event_id IS NULL
       AND ns.name_state_type_cd IN ('A', 'C')
       AND e.event_type_cd = 'EXAM'
       AND ni.consumption_date IS NULL
       AND ri.expiration_date > SYSDATE
       AND ri.request_type_cd NOT IN
               ('CEM', 'CFR', 'CLL', 'CLP', 'FR', 'LIB', 'LL', 'LP', 'NON', 'PAR', 'RLY', 'TMY',
                'XCLL', 'XCLP', 'XLL', 'XLP');


DROP PUBLIC SYNONYM SOLR_DATAIMPORT_CONFLICTS_VW;

CREATE PUBLIC SYNONYM SOLR_DATAIMPORT_CONFLICTS_VW FOR NAMEX.SOLR_DATAIMPORT_CONFLICTS_VW;
