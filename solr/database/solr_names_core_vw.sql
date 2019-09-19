
-- Do this as the normal user for the database:

CREATE OR REPLACE VIEW solr_names_core_vw
    (id, name, state, last_modified)
AS
SELECT
    requests.nr_num || '-' || names.choice AS id,
    names.name,
    CASE WHEN
        requests.state_cd != 'HOLD' AND
        names.state IN ('APPROVED', 'CONDITION', 'REJECTED')
    THEN
        'ACTIVE'
    ELSE
        'INACTIVE'
    END AS state,
    requests.last_update AS last_modified
FROM
    requests LEFT JOIN names ON requests.id = names.nr_id;

GRANT SELECT ON solr_names_core_vw TO solr;

COMMIT;
