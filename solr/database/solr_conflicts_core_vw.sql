-- Do the following as user "postgres":

CREATE ROLE solr LOGIN PASSWORD '[YOUR PASSWORD HERE]';
GRANT USAGE ON SCHEMA public TO solr;


-- Do this as the normal user for the database:

CREATE OR REPLACE VIEW solr_conflicts_core_vw
    (id, name, state, last_modified)
AS
SELECT
    requests.nr_num AS id,
    names.name,
    CASE WHEN
        requests.state_cd IN ('APPROVED', 'CONDITIONAL') AND
        requests.expiration_date > NOW() - INTERVAL '1 day' AND
        names.consumption_date IS NULL
    THEN
        'ACTIVE'
    ELSE
        'INACTIVE'
    END AS state,
    requests.last_update AS last_modified
FROM
    requests LEFT JOIN names ON requests.id = names.nr_id WHERE
    names.state IN ('APPROVED', 'CONDITION') AND
    requests.request_type_cd NOT IN ('CEM', 'CFR', 'CLL', 'CLP', 'FR', 'LIB', 'LL', 'LP', 'NON', 'PAR', 'RLY', 'TMY',
                                     'XCLL', 'XCLP', 'XLL', 'XLP');

GRANT SELECT ON solr_conflicts_core_vw TO solr;

COMMIT;
