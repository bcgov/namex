-- noinspection SqlNoDataSourceInspectionForFile

DROP VIEW NAMEX.NAMES_VW;

CREATE OR REPLACE FORCE VIEW namex.names_vw (request_id,
                                             choice_number,
                                             NAME,
                                             designation,
                                             name_state_type_cd,
                                             consumption_date,
                                             corp_num
                                            )
AS
    SELECT nm.request_id, ni.choice_number, ni.NAME, ni.designation, ns.name_state_type_cd, ni.consumption_date, ni.corp_num
      FROM name_instance ni LEFT OUTER JOIN NAME nm ON nm.name_id = ni.name_id
           LEFT OUTER JOIN name_state ns ON ns.name_id = ni.name_id
     WHERE ns.end_event_id IS NULL AND ni.end_event_id IS NULL;


DROP PUBLIC SYNONYM NAMES_VW;

CREATE PUBLIC SYNONYM NAMES_VW FOR NAMEX.NAMES_VW;
