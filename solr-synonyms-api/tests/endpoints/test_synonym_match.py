from flask import current_app
from namex.models import User
import os
import requests
import json
import pytest
from tests.python import integration_solr, integration_synonym_api, integration_postgres_solr
import urllib

token_header = {
                "alg": "RS256",
                "typ": "JWT",
                "kid": "flask-jwt-oidc-test-client"
               }
claims = {
            "iss": "https://sso-dev.pathfinder.gov.bc.ca/auth/realms/sbc",
            "sub": "43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc",
            "aud": "NameX-Dev",
            "exp": 31531718745,
            "iat": 1531718745,
            "jti": "flask-jwt-oidc-test-support",
            "typ": "Bearer",
            "username": "test-user",
            "realm_access": {
                "roles": [
                    "{}".format(User.EDITOR),
                    "{}".format(User.APPROVER),
                    "viewer",
                    "user"
                ]
            }
         }
SOLR_URL = os.getenv('SOLR_TEST_URL')
SOLR_SYNONYMS_API_URL = os.getenv('SOLR_SYNONYMS_API_URL')


@pytest.fixture(scope="session", autouse=True)
def reload_schema(request):
    url = SOLR_URL + '/solr/admin/cores?action=RELOAD&core=possible.conflicts&wt=json'
    r = requests.get(url)

    assert r.status_code == 200


@integration_solr
def test_solr_available(app, client, jwt):
    url = SOLR_URL + '/solr/possible.conflicts/admin/ping'
    r = requests.get(url)

    assert r.status_code == 200


def clean_database(client, jwt):
    url = SOLR_URL + '/solr/possible.conflicts/update?commit=true'
    headers = {'content-type': 'text/xml'}
    data = '<delete><query>id:*</query></delete>'
    r = requests.post(url, headers=headers, data=data)

    assert r.status_code == 200

def seed_database_with(client, jwt, name, id='1', source='2', clear=True):
    if clear:
        clean_database(client, jwt)
    url = SOLR_URL + '/solr/possible.conflicts/update?commit=true'
    headers = {'content-type': 'application/json'}
    data = '[{"source":"' + source + '", "name":"' + name + '", "id":"'+ id +'"}]'
    r = requests.post(url, headers=headers, data=data)

    assert r.status_code == 200


def verify(data, expected=None, not_expected=None):

    # expected + not_expected lists should be tested separately
    if expected and not_expected:
        assert False

    verified = False
    current_app.logger.debug(data['names'])
    current_app.logger.debug('EXPECTED ', expected)
    current_app.logger.debug('NOT EXPECTED ', not_expected)
    for result in data['names']:
        name = result['name_info']
        current_app.logger.debug('ACTUAL ', name['name'])

        if expected is []:
            # check that the name is the title of a query sent (no real names were returned from solr)
            if name['name'].find('----') == -1:
                verified = False
                break
            else:
                verified = True
        # if the expected name is in the names returned this will set 'verified' to true before the loop finishes
        elif expected and expected.lower().find(name['name'].lower()) != -1:
            verified = True
            break

        elif not_expected:
            verified = True
            if not_expected.lower().find(name['name'].lower()) != -1:
                verified = False
                break
    assert verified

def verify_synonym_match(client, jwt, query, expected_list=None, not_expected_list=None, exact_phrase='*'):
    data = search_synonym_match(client, jwt, query, exact_phrase)
    if expected_list:
        if expected_list is []:
            verify(data, [])
        else:
            for expected in expected_list:
                verify(data, expected)

    elif not_expected_list:
        for not_expected in not_expected_list:
            verify(data, None, not_expected)

def verify_order(client, jwt, query, expected_order):
    data = search_synonym_match(client, jwt, query)
    current_app.logger.debug('data[names]: ', data['names'])
    for result, expected in zip(data['names'], expected_order):
        actual = result['name_info']['name']
        current_app.logger.debug('Actual: ', actual)
        current_app.logger.debug('Expected: ', expected)
        assert actual.upper() == expected.upper()

def verify_stems(client, jwt, query, stems):
    data = search_synonym_match(client, jwt, query)

    for actual,expected in zip(data['names'][0]['stems'], stems):
        current_app.logger.debug('Actual: ', actual)
        current_app.logger.debug('Expected: ', expected)
        assert actual.upper() == expected.upper()

def search_synonym_match(client, jwt, query, exact_phrase='*'):
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token}
    url = '/api/v1/requests/synonymbucket/' + query + '/' + exact_phrase
    current_app.logger.debug(url)
    rv = client.get(url, headers=headers)

    assert rv.status_code == 200
    return json.loads(rv.data)


@integration_synonym_api
@integration_solr
def test_find_with_first_word(client, jwt):
    seed_database_with(client, jwt, 'JM Van Damme inc')
    verify_synonym_match(client, jwt,
        query='JM',
        expected_list=['----JM - PROXIMITY SEARCH','JM Van Damme inc ']
    )


@integration_synonym_api
@integration_solr
def test_resist_empty(client, jwt):
    seed_database_with(client, jwt, 'JM Van Damme inc')
    seed_database_with(client, jwt, 'SOME RANDOM NAME',id='2', source='2', clear=False)
    verify_synonym_match(client, jwt,
        query='*',
        expected_list=['----* - EXACT WORD ORDER', 'JM Van Damme inc', 'SOME RANDOM NAME']
    )


@integration_synonym_api
@integration_solr
def test_case_insensitive(client, jwt):
    seed_database_with(client, jwt, 'JacKlEs')
    verify_synonym_match(client, jwt,
        query='jackles',
        expected_list=['----JACKLES ', 'JacKlEs']
    )


@integration_synonym_api
@integration_solr
def test_no_match(client, jwt):
    seed_database_with(client, jwt, 'JM VAN DAMME INC')
    verify_synonym_match(client, jwt,
        query='Hello BC inc',
        expected_list=None
    )


@integration_synonym_api
@integration_solr
def test_numbers_preserved(client, jwt):
    seed_database_with(client, jwt, 'VAN 4 TRUCKING INC')
    verify_synonym_match(client, jwt,
       query='VAN 4 TRUCKING',
       expected_list=['VAN 4 TRUCKING INC']
    )


@integration_synonym_api
@integration_solr
def test_designation_removal(client, jwt):
    seed_database_with(client, jwt, 'DESIGNATION TEST')
    verify_synonym_match(client, jwt,
        query='DESIGNATION LIMITED',
        expected_list=['----DESIGNATION - PROXIMITY SEARCH', 'DESIGNATION TEST'],
        not_expected_list=['----DESIGNATION LIMITED ']
    )


@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("criteria, seed", [
    ('JAM\'S HOLDING', 'JAM HOLDING'),
    ('JAM\'S HOLDING', 'JAM\'S HOLDING'),
    ('JAMS HOLDING', 'JAM HOLDING'),
    ('JAMS HOLDINGS', 'JAM HOLDING'),
    ('JAMS\' HOLDINGS\'', 'JAM HOLDINGS'),
    ('JAM HOLDINGS', 'JAMS\' HOLDINGS\''),
    ('JASONS HOLSTERS', 'JASON HOLSTER'),
    ('A.S. HOLDERS', 'AS HOLDER'),
    ('H.A.S\'S HOLDERS', 'HASS HOLDER'),
])
def test_handles_s_and_possession(client, jwt, criteria, seed):
    seed_database_with(client, jwt, seed)
    verify_synonym_match(client, jwt,
        query=criteria,
        expected_list=[seed]
    )


@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("criteria, seed", [
    ('MY $ $TORE$', 'MY DOLLAR STORES'),
])
def test_handles_dollar_cent(client, jwt, criteria, seed):
    seed_database_with(client, jwt, seed)
    verify_synonym_match(client, jwt,
        query=criteria,
        expected_list=[seed]
    )


# TODO: fill out tests for all stop words
@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("criteria, seed", [
    ('JM AND HOLDING', 'JM HOLDING'),
    ('AN ART HOLDING', 'ART HOLDING'),
    ('THE HOLDING', 'HOLDING'),
    ('WE ARE HOLD', 'WE HOLD'),
    ('THERE IS HOLDING', 'HOLDING'),
])
def test_stopwords(client, jwt, criteria, seed):
    seed_database_with(client, jwt, seed)
    verify_synonym_match(client, jwt,
        query=criteria,
        expected_list=[seed]
    )


@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("criteria, seed", [
    ('TESTING COMPANY', 'SCARY TESTING COMPANY'),
    ('TESTS ARE GOOD', 'MANY TESTS ARE GOOD'),
])
def test_finds_names_with_word_to_left_of_distinctive(client, jwt, criteria, seed):
    seed_database_with(client, jwt, seed)
    verify_synonym_match(client, jwt,
        query=criteria,
        expected_list=[seed]
    )


@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("criteria, seed", [
    ('KIALS TESTING COMPANY', 'TESTING KIALS COMPANY'),
    ('TESTS GOOD COMPANY', 'COMPANY GOOD TESTS'),
])
def test_word_order_mixed(client, jwt, criteria, seed):
    seed_database_with(client, jwt, seed)
    verify_synonym_match(client, jwt,
        query=criteria,
        expected_list=[seed]
    )


@pytest.mark.skip(reason="duplicates not handled yet")
@integration_synonym_api
@integration_solr
def test_duplicated_letters(client, jwt):
    seed_database_with(client, jwt, 'Damme Trucking Inc')
    verify_synonym_match(client, jwt,
       query='Dame Trucking Inc',
       expected_list=None
    )


@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("criteria, seed", [
    ("Jameisons four two zero process server", '----JAMEISONS FOUR TWO ZERO synonyms:(PROCESS, SERVER, PROCESSSERVER) - PROXIMITY SEARCH'),
    ("pacific real estate", "----PACIFIC REALESTATE - PROXIMITY SEARCH"),
    ("pacific real estate", "----PACIFIC synonyms:(REALEST) - PROXIMITY SEARCH")
])
def test_multi_word_synonyms(client, jwt, criteria, seed):
    verify_synonym_match(client, jwt,
                         query=criteria,
                         expected_list=[seed]
                         )


@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("criteria, seed", [
    ('J.M. HOLDING', 'JM HOLDING'),
    ('J M HOLDING', 'JM HOLDING'),
    ('J. M. HOLDING', 'JM HOLDING'),
    ('J&M HOLDING', 'JM HOLDING'),
    ('J & M HOLDING', 'JM HOLDING'),
    ('J. & M. HOLDING', 'JM HOLDING'),
    ('J-M HOLDING', 'JM HOLDING'),
])
def test_finds_variations_on_initials(client, jwt, criteria, seed):
    seed_database_with(client, jwt, seed)
    verify_synonym_match(client, jwt,
        query=criteria,
        expected_list=[seed]
    )


@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("criteria, seed", [
    ('WEST FOR* TIMBER', 'WEST FOREST TIMBER'),
    ('W* FORE* TIMBER', 'WEST FOREST TIMBER'),
    ('W*T FOR*T TI*BER', 'WEST FOREST TIMBER'),
    ('W*T FORE* TI*BER', 'WEST FOREST TIMBER'),
    ('WEST FORE*T TIMBER', 'WEST FOREST TIMBER'),
    ('WE** FOREST TIMBER', 'WEST FOREST TIMBER'),
    ('WE** FORE*T TI**ER', 'WEST FOREST TIMBER'),
    ('W*S* F**ST T*M*R', 'WEST FOREST TIMBER'),
])
def test_wildcard_operator(client, jwt, criteria, seed):
    seed_database_with(client, jwt, seed)
    verify_synonym_match(client, jwt,
        query=criteria,
        expected_list=[seed]
    )


@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("criteria, seed", [
    ('J M HOLDINGS', 'J M HOLDINGS INC'),
    ('JM Van Damme Inc', 'J&M & Van Damme Inc'),
    ('J&M HOLDINGS', 'JM HOLDINGS INC'),
    ('J. & M. HOLDINGS', 'JM HOLDING INC'),
    ('J AND M HOLDINGS', 'J AND M HOLDINGS'),
    ('J-M HOLDINGS', 'J. & M. HOLDINGS'),
    ('J\'M HOLDINGS', 'J. & M. HOLDINGS'),
    ('J_M HOLDINGS', 'J. & M. HOLDINGS'),
    ('J_\'_-M HOLDINGS', 'J.M. HOLDINGS'),
    ('J@M HOLDINGS', 'J.M. HOLDINGS'),
    ('J=M HOLDINGS', 'J. M. HOLDINGS'),
    ('J!M HOLDINGS', 'J. & M. HOLDINGS'),
    ('J!=@_M HOLDINGS', 'J. M. HOLDINGS'),
    ('J+M HOLDINGS', 'J. & M. HOLDING\'S'),
    ('J\M HOLDINGS', 'J. & M. HOLDINGS'),
])
def test_explore_complex_cases(client, jwt, criteria, seed):
    seed_database_with(client, jwt, seed)
    verify_synonym_match(client, jwt,
       query=criteria,
       expected_list=[seed]
    )

@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("criteria, seed", [
    ('TESTING AND TRYING', 'TESTING TRYING'),
    ('TESTING + TRYING', 'TESTING TRYING'),
    ('TESTING & TRYING', 'TESTING TRYING'),
    ('TESTING\'N TRYING', 'TESTING TRYING'),
    ('TESTING\'N TRYING', 'TESTING AND TRYING'),
    ('TESTING AND TRYING', 'TESTING & TRYING'),
    ('TESTING + TRYING', 'TESTING\'N TRYING'),
    ('TESTING & TRYING', 'TESTING + TRYING'),
])
def test_strips_and_variations(client, jwt, criteria, seed):
    seed_database_with(client, jwt, seed)
    verify_synonym_match(client, jwt,
       query=criteria,
       expected_list=[seed]
    )

@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("criteria, seed", [
    ('TESTING RUNNING TRYING', 'TESTINGRUNNING TRYING'),
    ('TESTING RUNNING TRYING', 'TESTING RUNNINGTRYING'),
    ('TESTING RUNNING TRYING', 'TESTINGRUNNINGTRYING'),
])
def test_compound_concat(client, jwt, criteria, seed):
    seed_database_with(client, jwt, seed)
    verify_synonym_match(client, jwt,
       query=criteria,
       expected_list=[seed]
    )

@pytest.mark.skip(reason="dont know how to make solr handle those scenarios")
@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("criteria, seed", [
    ('{JM} HOLDINGS', 'J. & M. HOLDINGS'),
    ('[JM] HOLDINGS', 'J. & M. HOLDINGS'),
    ('(JM) HOLDINGS', 'J.M HOLDINGS'),
    ('J^M HOLDINGS', 'J. & M. HOLDINGS'),
    ('J~M HOLDINGS', 'J. & M. HOLDINGS'),
    ('J*M HOLDINGS', 'J. & M. HOLDINGS'),
    ('J:M HOLDINGS', 'J. & M. HOLDINGS'),
    ('J?M HOLDINGS', 'J. & M. HOLDINGS')
])
def test_special_characters(client, jwt, criteria, seed):
    seed_database_with(client, jwt, seed)
    verify_synonym_match(client, jwt,
       query=criteria,
       expected_list=[seed]
    )


@integration_synonym_api
@integration_solr
def test_prox_search_ignores_wildcards(client, jwt):
    seed_database_with(client, jwt, 'TESTING WILDCARDS')
    verify_synonym_match(client, jwt,
        query="TESTING* @WILDCARDS",
        expected_list=['----TESTING WILDCARDS - PROXIMITY SEARCH', 'TESTING WILDCARDS'],
        not_expected_list=['----TESTING* @WILDCARDS - PROXIMITY SEARCH']
    )


@integration_synonym_api
@integration_solr
def test_exact_word_order_stack_title_with_wilcards(client, jwt):
    verify_synonym_match(client, jwt,
        query="TESTING* WILDCARDS",
        expected_list=['----TESTING* WILDCARDS* - EXACT WORD ORDER', '----TESTING* - EXACT WORD ORDER'],
        not_expected_list=['----TESTING** - EXACT WORD ORDER']
    )


@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("criteria, seed", [
    ('TJ´S BACKCOUNTRY ADVENTURES.', '----TJC2B4S BACKCOUNTRY ADVENTURES - PROXIMITY SEARCH'),
    ('HOUSE BÜBÜ DA WOLF.', '----HOUSE BC39CBC39C DA WOLF - PROXIMITY SEARCH'),
    ('DIAMANTÉ DIAMOND SETTING', '----DIAMANTC389 DIAMOND SETTING - PROXIMITY SEARCH'),
    ('MICHELLE¿S BEAR ESSENTIALS.', '----MICHELLEC2BFS BEAR ESSENTIALS - PROXIMITY SEARCH'),
    ('TEST àâçèéêëîïôöùûü BEAR.', '----TEST C380C382C387C388C389C38AC38BC38EC38FC394C396C399C39BC39C BEAR - PROXIMITY SEARCH'),
    ('TEST ÀÂÇÈÉÊËÎÏÔÖÙÛÜS BEAR.', '----TEST C380C382C387C388C389C38AC38BC38EC38FC394C396C399C39BC39CS BEAR - PROXIMITY SEARCH'),
    ('TEST °£÷¥·©§¶¼½`¾¢!¦«ª¡¹²³»¿¬±¤®× BEAR.', '----TEST C2B0C2A3C3B7C2A5C2B7C2A9C2A7C2B6C2BCC2BD`C2BEC2A2C2A6C2ABC2AAC2A1C2B9C2B2C2B3C2BBC2BFC2ACC2B1C2A4C2AEC397 BEAR - PROXIMITY SEARCH'),
])
def test_bypass_nonascii_characters(client, jwt, criteria, seed):
    verify_synonym_match(client,
                         jwt,
                         query=criteria,
                         expected_list=[seed])

@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("criteria, seed", [
    ('AN AND ARE AS AT TEST', '----TEST - PROXIMITY SEARCH'),
    ('BE BUT BY FOR IF TO TEST', '----TEST - PROXIMITY SEARCH'),
    ('IN INTO IS IT NO NOT TEST', '----TEST - PROXIMITY SEARCH'),
    ('OF ON OR SUCH THAT THE TEST', '----TEST - PROXIMITY SEARCH'),
    ('THEIR THEN THERE THESE THEY THIS TEST', '----TEST - PROXIMITY SEARCH'),
])
def test_strips_stop_words(client, jwt, criteria, seed):
    verify_synonym_match(client, jwt,
        query=criteria,
        expected_list=[seed]
    )

@integration_postgres_solr
@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("query, ordered_list", [
    ('TESTING ORDER DEVELOPMENT SYNONYMS', ['----TESTING ORDER DEVELOPMENT SYNONYMS - PROXIMITY SEARCH',
                                                  'TESTING ORDER DEVELOPMENT SYNONYMS',
                                                  'TESTING ORDER CONSTRUCTION SYNONYMS',
                                                  'TESTING ORDER LAND SYNONYMS',
                                                  ]),
])
def test_order(client, jwt, query, ordered_list):
    #  for loop didn't work for seeding so manual
    seed_database_with(client, jwt, 'TESTING ORDER CONSTRUCTION SYNONYMS', id='1', source='2')
    seed_database_with(client, jwt, 'TESTING ORDER DEVELOPMENT SYNONYMS', id='2', source='4', clear=False)
    seed_database_with(client, jwt, 'TESTING ORDER LAND SYNONYMS', id='3', source='3', clear=False)
    verify_order(client, jwt, query=query, expected_order=ordered_list)

@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("query, stems", [
    ('CONSTRUCTION', ['CONSTRUCT']),
    ('DEVELOPMENT', ['DEVELOP']),
    ('CONSULTING', ['CONSULT']),
    ('CONSTRUCTION DEVELOPMENT', ['CONSTRUCT', 'DEVELOP']),
    ('CONSULTING CONSTRUCTION DEVELOPMENT', ['CONSULT', 'CONSTRUCT', 'DEVELOP']),
    ('PROPERTY', ['PROPERTI','PROPERT']),
    ('PROPERTIES', ['PROPERTI']),
    ('MANAGEMENT PROPERTY', ['MANAG','PROPERTI','PROPERT']),
])
def test_stems(client, jwt, query, stems):
    verify_stems(client, jwt, query=query, stems=stems)

@integration_postgres_solr
@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("query, expected_list", [
    ('PACIFIC TAKEOUT', ['PACIFIC FASTFOOD', 'PACIFIC DINER']),
])
def test_synonyms_match_on_all_synonym_lists(client, jwt, query, expected_list):
    #  some synonyms are part of multiple lists so check that they return matches on both
    seed_database_with(client, jwt, 'PACIFIC FASTFOOD', id='1', source='2')
    seed_database_with(client, jwt, 'PACIFIC DINER', id='2', source='2', clear=False)
    verify_synonym_match(client, jwt, query=query, expected_list=expected_list)

@integration_postgres_solr
@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("query, expected_list, not_expected_list", [
    ('ON THE BALL RIGGING', ['ON THE BALL RIGGING'], None),
    ('ON THE BALL RIGGING', None, ['BALL RIGGING']),
    ('ON THE BALL RIGGING', ['ON THE BALL TEST NO SYNONYM'], None),
])
def test_search_exact_phrase(client, jwt, query, expected_list, not_expected_list):
    #  some synonyms are part of multiple lists so check that they return matches on both
    seed_database_with(client, jwt, 'ON THE BALL RIGGING', id='1', source='2')
    seed_database_with(client, jwt, 'BALL RIGGING', id='2', source='2', clear=False)
    seed_database_with(client, jwt, 'ON THE BALL TEST NO SYNONYM', id='3', source='2', clear=False)
    verify_synonym_match(client, jwt, query=query, expected_list=expected_list, not_expected_list=not_expected_list, exact_phrase='ON THE')

@integration_postgres_solr
@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("query, expected_list", [
    ('TRUCKING', ['BARGE', 'TRANSPORT', 'EXPRESS']),
])
def test_stems_of_synonyms_match_on_synonyms_list(client, jwt, query, expected_list):
    # i.e. 'trucking' is not in the synonym list but stems to 'truck', which is in the list
    seed_database_with(client, jwt, 'BARGE', id='1', source='2')
    seed_database_with(client, jwt, 'EXPRESS', id='2', source='2', clear=False)
    seed_database_with(client, jwt, 'TRANSPORT', id='3', source='2', clear=False)
    verify_synonym_match(client, jwt, query=query, expected_list=expected_list)

@integration_postgres_solr
@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("query, expected_list", [
    ('5TH TESTZZZ', ['----5TH - PROXIMITY SEARCH', 'FIFTH ZZZZZ']),
])
def test_number_synonyms(client, jwt, query, expected_list):
    seed_database_with(client, jwt, 'FIFTH ZZZZZ', id='1', source='2')
    verify_synonym_match(client, jwt, query=query, expected_list=expected_list)

@integration_postgres_solr
@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("query, ordered_list", [
    ('PACIFIC WEST CONSTRUCTION', ['----PACIFIC WEST CONSTRUCTION - PROXIMITY SEARCH',
                                    '----PACIFIC WEST CONSTRUCTION* - EXACT WORD ORDER',
                                    '----PACIFIC WEST synonyms:(CONSTRUCT) - PROXIMITY SEARCH',
                                    '----PACIFIC WEST* synonyms:(CONSTRUCT) - EXACT WORD ORDER',
                                    '----PACIFIC synonyms:(CONSTRUCT) - PROXIMITY SEARCH',
                                    'PACIFIC DEVELOPMENT',
                                                  ]),
])
def test_synonym_clause_stemmed(client, jwt, query, ordered_list):
    #  for loop didn't work for seeding so manual
    seed_database_with(client, jwt, 'PACIFIC DEVELOPMENT', id='1', source='2')
    verify_order(client, jwt, query=query, expected_order=ordered_list)

@integration_postgres_solr
@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("query, expected_list", [
    ('KM CONTRACTING', ['K & M CONSTRUCTION']),
])
def test_number_synonyms(client, jwt, query, expected_list):
    seed_database_with(client, jwt, 'K & M CONSTRUCTION', id='1', source='2')
    verify_synonym_match(client, jwt, query=query, expected_list=expected_list)

@integration_postgres_solr
@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("query, expected_list", [
    ('MISSED TEST INTERIOR', ['MISSEDEXACTWORDORDER1 LIVING FOUND','MISSEDEXACTWORDORDER2 LIVING FOUND',
                              'FOUND MISSED LIVING PROXIMITY1', 'LIVING MISSED FOUND PROXIMITY2']),
])
def test_full_resultset_returned(client, jwt, query, expected_list):
    seed_database_with(client, jwt, 'MISSEDEXACTWORDORDER1 LIVING FOUND', id='1', source='2')
    seed_database_with(client, jwt, 'MISSEDEXACTWORDORDER2 LIVING FOUND', id='2', source='2', clear=False)
    seed_database_with(client, jwt, 'FOUND MISSED LIVING PROXIMITY1', id='3', source='2', clear=False)
    seed_database_with(client, jwt, 'LIVING MISSED FOUND PROXIMITY2', id='4', source='2', clear=False)
    verify_synonym_match(client, jwt, query=query, expected_list=expected_list)

@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("query", [
    ('T.H.E.'),
    ('COMPANY'),
    ('ASSN'),
    ('THAT'),
    ('LIMITED CORP.'),
])
def test_query_stripped_to_empty_string(client, jwt, query):
    seed_database_with(client, jwt, 'JM Van Damme inc')
    seed_database_with(client, jwt, 'SOME RANDOM NAME',id='2', source='2', clear=False)
    verify_synonym_match(client, jwt,
        query=query,
        expected_list=['----* - EXACT WORD ORDER', 'JM Van Damme inc', 'SOME RANDOM NAME']
    )
