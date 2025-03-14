-- noinspection SqlNoDataSourceInspectionForFile

--
-- For every corporation with a class of BC, SOC, OT, or XPRO list the following fields:
--  - id: corporation number
--  - name: the most recent name of the corporation, ignoring future effective dated filings.
--  - state: either ACTIVE or INACTIVE, reflecting whether or not the more recent state of the corporation, ignoring
--        future effective dated filings, is ACT or HIS.
--  - last_modified: the timestamp of the most recent name or state change, ignoring future effective dated filings.
--
CREATE OR REPLACE FORCE VIEW namex.solr_conflicts_core_vw (
    id,
    name,
    state,
    last_modified
) AS
    SELECT id, name, state, last_modified FROM
    (
        SELECT
            corp_num AS id,
            name,
            DECODE(op_state_typ_cd, 'ACT', 'ACTIVE', 'HIS', 'INACTIVE') AS state,
            SYS_EXTRACT_UTC(CAST(GREATEST(state_timestmp, name_timestmp) AS TIMESTAMP)) AS last_modified,
            --
            -- This is a bit of a hack.
            --
            -- Background: corporations may have the following types of names: NB (numbered company), CO (corporation
            -- name), or CO and AS (assumed name). The business rule is that in the last case the AS name is the name
            -- to be used.
            --
            -- What this does is basically group the result set by corporation number, and then sort them by name_type,
            -- such that in the case of both AS and CO names, the AS name is in row number 1. At the bottom of this
            -- query is a clause that only selects row number 1, which excludes the CO names only in the case that an
            -- AS name exists.
            ROW_NUMBER() OVER (PARTITION BY corp_num ORDER BY name_type) AS name_ranking
        FROM (
            SELECT
                corp_num,
                -- Exclude future effective dated filings by comparing timestamps against the current time.
                CASE WHEN final_state_timestmp < SYSDATE THEN
                    final_state_typ_cd ELSE previous_state_typ_cd END AS state_type_cd,
                CASE WHEN final_state_timestmp < SYSDATE THEN
                    final_state_timestmp ELSE previous_state_timestmp END AS state_timestmp,
                CASE WHEN final_name_timestmp < SYSDATE THEN
                    final_corp_name ELSE previous_corp_name END AS name,
                CASE WHEN final_name_timestmp < SYSDATE THEN
                    final_name_timestmp ELSE previous_name_timestmp END AS name_timestmp,
                CASE WHEN final_name_timestmp < SYSDATE THEN
                    final_name_type ELSE previous_name_type END AS name_type
            FROM (
                SELECT
                    corporation.corp_num,
                    final_state.state_typ_cd AS final_state_typ_cd,
                    CASE
                        WHEN final_state.state_typ_cd IN
                            -- These states have a trigger_dts value, but it does NOT indicate a future effective date.
                            ('D1A', 'D1F', 'D1T', 'D2A', 'D2F', 'D2T', 'HDA', 'HIS', 'LIQ', 'LRS', 'NST')
                        THEN
                            final_state_event.event_timestmp
                        ELSE
                            nvl(final_state_event.trigger_dts, final_state_event.event_timestmp)
                        END AS final_state_timestmp,
                    previous_state.state_typ_cd AS previous_state_typ_cd,
                    CASE
                        WHEN previous_state.state_typ_cd IN
                            -- These states have a trigger_dts value, but it does NOT indicate a future effective date.
                            ('D1A', 'D1F', 'D1T', 'D2A', 'D2F', 'D2T', 'HDA', 'HIS', 'LIQ', 'LRS', 'NST')
                        THEN
                            previous_state_event.event_timestmp
                        ELSE
                            nvl(previous_state_event.trigger_dts, previous_state_event.event_timestmp)
                        END AS previous_state_timestmp,
                    final_name.corp_nme AS final_corp_name,
                    final_name.corp_name_typ_cd AS final_name_type,
                    nvl(final_name_event.trigger_dts, final_name_event.event_timestmp) AS final_name_timestmp,
                    previous_name.corp_nme AS previous_corp_name,
                    previous_name.corp_name_typ_cd AS previous_name_type,
                    nvl(previous_name_event.trigger_dts, previous_name_event.event_timestmp) AS previous_name_timestmp
                FROM
                    corporation
                    INNER JOIN corp_type ON
                        corporation.corp_typ_cd = corp_type.corp_typ_cd
                    INNER JOIN corp_state final_state ON
                        corporation.corp_num = final_state.corp_num AND final_state.end_event_id IS NULL
                    INNER JOIN event final_state_event ON
                        final_state.start_event_id = final_state_event.event_id
                    LEFT JOIN corp_state previous_state ON
                        corporation.corp_num = previous_state.corp_num AND
                        previous_state.end_event_id = final_state.start_event_id
                    LEFT JOIN event previous_state_event ON
                        previous_state.start_event_id = previous_state_event.event_id
                    INNER JOIN corp_name final_name ON
                        corporation.corp_num = final_name.corp_num AND final_name.end_event_id IS NULL
                    INNER JOIN event final_name_event ON
                        final_name.start_event_id = final_name_event.event_id
                    LEFT JOIN corp_name previous_name ON
                        corporation.corp_num = previous_name.corp_num AND
                        previous_name.end_event_id = final_name.start_event_id
                    LEFT JOIN event previous_name_event ON
                        previous_name.start_event_id = previous_name_event.event_id
                WHERE
                    corp_type.corp_class IN ('BC', 'SOC', 'OT', 'XPRO') AND
                    final_name.corp_name_typ_cd IN ('AS', 'CO', 'NB') AND
                    (previous_name.corp_name_typ_cd IS NULL OR previous_name.corp_name_typ_cd IN ('AS', 'CO', 'NB'))
            )
        ) INNER JOIN corp_op_state ON state_type_cd = corp_op_state.state_typ_cd
    )
    -- Exclude the CO name if an AS name exists. See the definition of the PARTITION, above, for details.
    WHERE name_ranking = 1;
