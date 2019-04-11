
-- Do this as the normal user for the database:

CREATE OR REPLACE VIEW solr_conflicts_core_vw
    (id, name, state, last_modified)
AS
SELECT
    nr_num AS id,
    name,
    CASE WHEN
        state_cd IN ('APPROVED', 'CONDITIONAL') AND
        expiration_date > NOW() - INTERVAL '1 day' AND
        consumption_date IS NULL
    THEN
        'ACTIVE'
    ELSE
        'INACTIVE'
    END AS state,
    last_update AS last_modified
FROM
    requests LEFT JOIN names ON requests.id = names.nr_id WHERE
    state IN ('APPROVED', 'CONDITION') AND
    request_type_cd NOT IN ('CEM', 'CFR', 'CLL', 'CLP', 'FR', 'LIB', 'LL', 'LP', 'NON', 'PAR', 'RLY', 'TMY', 'XCLL',
                            'XCLP', 'XLL', 'XLP');

COMMIT;


-- Do the following as user "postgres":

CREATE ROLE solr LOGIN PASSWORD '[YOUR PASSWORD HERE]';
GRANT USAGE ON SCHEMA public TO solr;
GRANT SELECT ON solr_conflicts_core_vw TO solr;

COMMIT;
