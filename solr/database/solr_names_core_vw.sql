
-- Do this as the normal user for the database:

CREATE OR REPLACE VIEW solr_names_core_vw
    (id, name, state, last_modified)
AS
SELECT
    nr_num || '-' || choice AS id,
    name,
    CASE WHEN
        state IN ('APPROVED', 'CONDITION', 'REJECTED')
    THEN
        'ACTIVE'
    ELSE
        'INACTIVE'
    END AS state,
    last_update AS last_modified
FROM
    requests LEFT JOIN names ON requests.id = names.nr_id;

COMMIT;


-- Do the following as user "postgres":

GRANT SELECT ON solr_names_core_vw TO solr;

COMMIT;
