-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.SOLR_DATAIMPORT_CONFLICTS_VW;

CREATE OR REPLACE FORCE VIEW namex.solr_dataimport_conflicts_vw (ID, NAME, state_type_cd, SOURCE)
AS
    SELECT r.nr_num AS ID, ni.NAME, ns.name_state_type_cd AS state_type_cd, 'NR' AS SOURCE
      FROM request r INNER JOIN request_instance ri ON ri.request_id = r.request_id
           INNER JOIN NAME n ON n.request_id = r.request_id
           INNER JOIN name_instance ni ON ni.name_id = n.name_id
           INNER JOIN name_state ns ON ns.name_id = ni.name_id
           INNER JOIN request_state rs ON rs.request_id = r.request_id
     WHERE ri.end_event_id IS NULL
       AND ni.end_event_id IS NULL
       AND ns.end_event_id IS NULL
       AND rs.end_event_id IS NULL
       AND rs.state_type_cd = 'COMPLETED'
       AND ns.name_state_type_cd IN ('A', 'C')
       AND ni.consumption_date IS NULL
       AND TRUNC (ri.expiration_date) >= TRUNC (SYSDATE)
       AND ri.request_type_cd NOT IN
               ('CEM', 'CFR', 'CLL', 'CLP', 'FR', 'LIB', 'LL', 'LP', 'NON', 'PAR', 'RLY', 'TMY',
                'XCLL', 'XCLP', 'XLL', 'XLP');
