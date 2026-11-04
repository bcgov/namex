
import enum
import json
import sys

import psycopg2.extras
import requests


class SolrCore(enum.Enum):
    NAMES = enum.auto()
    CONFLICTS_CORP = enum.auto()
    CONFLICTS_NR = enum.auto()


class Environment(enum.Enum):
    LOCAL = enum.auto()
    DEV = enum.auto()
    TEST = enum.auto()
    PROD = enum.auto()


SolrBaseUrls = {
    Environment.LOCAL: 'http://localhost:8983/solr',
    Environment.DEV: 'https://namex-solr-dev.pathfinder.gov.bc.ca/solr',
    Environment.TEST: 'https://namex-solr-test.pathfinder.gov.bc.ca/solr',
    Environment.PROD: 'https://namex-solr.pathfinder.gov.bc.ca/solr'
}

SolrCoreNames = {
    SolrCore.NAMES: 'names',
    SolrCore.CONFLICTS_CORP: 'possible.conflicts',
    SolrCore.CONFLICTS_NR: 'possible.conflicts'
}

DatabaseConnectionStrings = {
    SolrCore.NAMES: 'dbname=BC_REGISTRIES_NAMES host=localhost port=54323 user={}',
    SolrCore.CONFLICTS_CORP: 'dbname=BC_REGISTRIES host=localhost port=54322 user={}',
    SolrCore.CONFLICTS_NR: 'dbname=BC_REGISTRIES_NAMES host=localhost port=54323 user={}'
}


def get_solr_url(core, environment):
    url = SolrBaseUrls[environment] + '/' + SolrCoreNames[core] + '/select?wt=json&rows=10000000'

    if core == SolrCore.NAMES:
        url += '&q=*:*'
    elif core == SolrCore.CONFLICTS_CORP:
        url += '&q=source:CORP'
    elif core == SolrCore.CONFLICTS_NR:
        url += '&q=source:NR'

    return url


def get_database_connection_string(core, username):
    return DatabaseConnectionStrings[core].format(username)


def get_database_view_name(core):
    if core == SolrCore.NAMES:
        view_name = 'bc_registries_names.solr_dataimport_names_vw'
    elif core == SolrCore.CONFLICTS_CORP:
        view_name = 'bc_registries.solr_dataimport_conflicts_vw'
    elif core == SolrCore.CONFLICTS_NR:
        view_name = 'bc_registries_names.solr_dataimport_conflicts_vw'
    else:
        raise Exception('Unknown core value "{}"'.format(core))

    return view_name


def compare(solr_core, environment, username):
    # Pull down everything.
    connection = psycopg2.connect(get_database_connection_string(solr_core, username))
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT * FROM ' + get_database_view_name(solr_core))
    print("{} results in Oracle".format(cursor.rowcount))
    oracle_results = cursor.fetchall()

    solr_results = requests.get(get_solr_url(solr_core, environment))
    if solr_results.status_code != 200:
        print('Solr: {} ({})'.format(solr_results.reason, solr_results.status_code))

        sys.exit(-1)

    # OK, we have fetched everything from the two sources at roughly the same time. Now compare.

    oracle_results_dict = dict()
    column_names = [description[0] for description in cursor.description]
    for row in oracle_results:
        key = row['id']

        row_data = dict()
        for column_name in column_names:
            row_data[column_name] = row[column_name]

        oracle_results_dict[key] = row_data

    # Free some memory?
    del oracle_results
    connection.close()

    solr_results = json.loads(solr_results.text)
    solr_results_dict = dict()
    for document in solr_results['response']['docs']:
        solr_results_dict[document['id']] = document

    print("{} results in Solr".format(len(solr_results_dict)))

    # Free some memory?
    del solr_results

    oracle_key_set = set(oracle_results_dict)
    solr_key_set = set(solr_results_dict)

    only_in_oracle = oracle_key_set - solr_key_set
    only_in_solr = solr_key_set - oracle_key_set

    print('In view but not in Solr core: ' + str(sorted(only_in_oracle)))
    print('In Solr core but not in view: ' + str(sorted(only_in_solr)))

    # Next: compare the actual data.

    in_both = oracle_key_set.intersection(solr_key_set)
    for key in in_both:
        solr = solr_results_dict[key]
        oracle = oracle_results_dict[key]

        for field_name in oracle.keys():
            # Convert missing values to empty strings.
            try:
                solr_field = solr[field_name]
            except KeyError as error:
                solr_field = ''

            # Convert nulls to empty strings.
            oracle_field = oracle[field_name]
            if oracle_field is None:
                oracle_field = ''

            # Compare as strings, since Solr incorrectly stores some of the numeric fields.
            if str(solr_field) != str(oracle_field):
                print('Error with id={}: field {} has the Solr value "{}", but the value in Oracle is "{}"'
                      .format(key, field_name, solr_field, oracle_field))
                print(solr)
                print(oracle)


# Remember to:
#   C:> start /b oc port-forward postgres-oracle-fdw-registry-<pod_id> 54322:5432
#   C:> start /b oc port-forward postgresql-oracle-fdw-names-<pod_id> 54323:5432

# compare(SolrCore.NAMES, Environment.DEV, 'USER_XXXX')
# compare(SolrCore.CONFLICTS_CORP, Environment.DEV, 'USER_XXXX')
# compare(SolrCore.CONFLICTS_NR, Environment.DEV, 'USER_XXXX')

# compare(SolrCore.NAMES, Environment.TEST, 'USER_XXXX')
# compare(SolrCore.CONFLICTS_CORP, Environment.TEST, 'USER_XXXX')
# compare(SolrCore.CONFLICTS_NR, Environment.TEST, 'USER_XXXX')

# compare(SolrCore.NAMES, Environment.PROD, 'USER_XXXX')
# compare(SolrCore.CONFLICTS_CORP, Environment.PROD, 'USER_XXXX')
compare(SolrCore.CONFLICTS_NR, Environment.PROD, 'USER_XXXX')
