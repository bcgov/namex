from namex.models import User
import os
import requests
import json
import pytest
from tests.python import integration_solr, integration_synonym_api
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


def seed_database_with(client, jwt, name, id='1', source='2'):
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
    print(data['names'])

    for result in data['names']:
        name = result['name_info']
        print('ACTUAL ', name['name'])
        print('EXPECTED ',expected)
        print('NOT EXPECTED ', not_expected)

        if expected is []:
            # check that the name is the title of a query sent (no real names were returned from solr)
            if name['name'].find('----') == -1:
                verified = False
                break
            else:
                verified = True
        # if the expected name is in the names returned this will set 'verified' to true before the loop finishes
        elif expected.lower().find(name['name'].lower()) != -1:
            verified = True
            break

        elif not_expected:
            verified = True
            if not_expected.lower().find(name['name'].lower()) != -1:
                verified = False
                break

    assert verified

# def verify_synonym_match_results(client, jwt, query, expected):
#     data = search_synonym_match(client, jwt, query)
#     verify(data, expected)


def verify_synonym_match(client, jwt, query, expected_list=None, not_expected_list=None):
    data = search_synonym_match(client, jwt, query)
    if expected_list:
        if expected_list is []:
            verify(data, [])
        else:
            for expected in expected_list:
                verify(data, expected)

    elif not_expected_list:
        for not_expected in not_expected_list:
            verify(data, None, not_expected)


def search_synonym_match(client, jwt, query):
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token}
    url = '/api/v1/requests/synonymbucket/' + query
    print(url)
    rv = client.get(url, headers=headers)

    assert rv.status_code == 200
    return json.loads(rv.data)


@integration_synonym_api
@integration_solr
def test_find_with_first_word(client, jwt, app):
    seed_database_with(client, jwt, 'JM Van Damme inc')
    verify_synonym_match(client, jwt,
        query='JM',
        expected_list=['----JM - PROXIMITY SEARCH','JM Van Damme inc ']
    )


@pytest.mark.skip(reason="frontend handles empty string for now")
@integration_synonym_api
@integration_solr
def test_resist_empty(client, jwt, app):
    seed_database_with(client, jwt, 'JM Van Damme inc')
    verify_synonym_match(client, jwt,
        query='',
        expected_list=[]
    )


@integration_synonym_api
@integration_solr
def test_case_insensitive(client, jwt, app):
    seed_database_with(client, jwt, 'JacKlEs')
    verify_synonym_match(client, jwt,
        query='jackles',
        expected_list=['----JACKLES ', 'JacKlEs']
    )


@integration_synonym_api
@integration_solr
def test_no_match(client, jwt, app):
    seed_database_with(client, jwt, 'JM VAN DAMME INC')
    verify_synonym_match(client, jwt,
        query='Hello BC inc',
        expected_list=None
    )


@integration_synonym_api
@integration_solr
def test_numbers_preserved(client, jwt, app):
    seed_database_with(client, jwt, 'VAN 4 TRUCKING INC')
    verify_synonym_match(client, jwt,
       query='VAN 4 TRUCKING',
       expected_list=['VAN 4 TRUCKING INC']
    )


@integration_synonym_api
@integration_solr
def test_designation_removal(client, jwt, app):
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
def test_handles_s_and_possession(client, jwt, app, criteria, seed):
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
def test_handles_dollar_cent(client, jwt, app, criteria, seed):
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
def test_stopwords(client, jwt, app, criteria, seed):
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
def test_finds_names_with_word_to_left_of_distinctive(client, jwt, app, criteria, seed):
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
def test_word_order_mixed(client, jwt, app, criteria, seed):
    seed_database_with(client, jwt, seed)
    verify_synonym_match(client, jwt,
        query=criteria,
        expected_list=[seed]
    )


@pytest.mark.skip(reason="duplicates not handled yet")
@integration_synonym_api
@integration_solr
def test_duplicated_letters(client, jwt, app):
    seed_database_with(client, jwt, 'Damme Trucking Inc')
    verify_synonym_match(client, jwt,
       query='Dame Trucking Inc',
       expected_list=None
    )


@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("criteria, seed", [
    ("Jameisons four two zero process server", '----JAMEISONS FOUR TWO ZERO PROCESS synonyms:(server) - PROXIMITY SEARCH'),
    ("Jameisons four two zero process server", '----JAMEISONS FOUR TWO ZERO synonyms:(process, server, processserver) - PROXIMITY SEARCH'),
    ("Jameisons four two zero process server", '----JAMEISONS FOUR TWO synonyms:(process, server, processserver) - PROXIMITY SEARCH'),
    ("Jameisons four two zero process server", '----JAMEISONS FOUR synonyms:(two, process, server, twozero, processserver) - PROXIMITY SEARCH'),
    ("Jameisons four two zero process server", '----JAMEISONS synonyms:(four, two, process, server, fourtwo, fourtwozero, twozero, processserver) - PROXIMITY SEARCH'),
])
def test_multi_word_synonyms(client, jwt, app, criteria, seed):
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
def test_finds_variations_on_initials(client, jwt, app, criteria, seed):
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
    ('WEST FORE?T TIMBER', 'WEST FOREST TIMBER'),
    ('WE?? FOREST TIMBER', 'WEST FOREST TIMBER'),
    ('WE?? FORE?T TI??ER', 'WEST FOREST TIMBER'),
    ('WE?? FO*ST T?M*R', 'WEST FOREST TIMBER'),
])
def test_wildcard_operator(client, jwt, app, criteria, seed):
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
def test_explore_complex_cases(client, jwt, app, criteria, seed):
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
def test_strips_and_variations(client, jwt, app, criteria, seed):
    seed_database_with(client, jwt, seed)
    verify_synonym_match(client, jwt,
       query=criteria,
       expected_list=[seed]
    )

@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("criteria, seed", [
    ('TESTING AND TRYING', 'TESTINGAND TRYING'),
    ('TESTING AND TRYING', 'TESTING ANDTRYING'),
    ('TESTING AND TRYING', 'TESTINGANDTRYING'),
])
def test_compound_concat(client, jwt, app, criteria, seed):
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
def test_special_characters(client, jwt, app, criteria, seed):
    seed_database_with(client, jwt, seed)
    verify_synonym_match(client, jwt,
       query=criteria,
       expected_list=[seed]
    )


@integration_synonym_api
@integration_solr
def test_prox_search_ignores_wildcards(client, jwt, app):
    seed_database_with(client, jwt, 'TESTING WILDCARDS')
    verify_synonym_match(client, jwt,
        query="TESTING* @WILDCARDS",
        expected_list=['----TESTING WILDCARDS - PROXIMITY SEARCH', 'TESTING WILDCARDS'],
        not_expected_list=['----TESTING* @WILDCARDS - PROXIMITY SEARCH']
    )


@integration_synonym_api
@integration_solr
def test_exact_word_order_stack_title_with_wilcards(client, jwt, app):
    verify_synonym_match(client, jwt,
        query="TESTING* WILDCARDS",
        expected_list=['----TESTING* WILDCARDS* - EXACT WORD ORDER', '----TESTING* - EXACT WORD ORDER'],
        not_expected_list=['----TESTING** - EXACT WORD ORDER']
    )


@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("criteria, seed", [
    ('TJ´S BACKCOUNTRY ADVENTURES.', '----TJ´S BACKCOUNTRY ADVENTURES. - PROXIMITY SEARCH'),
    ('THE HOUSE OF BÜBÜ AN DA WOLF.', '----THE HOUSE OF BÜBÜ AN DA WOLF. - PROXIMITY SEARCH'),
    ('DIAMANTÉ DIAMOND SETTING', '----DIAMANTÉ DIAMOND SETTING - PROXIMITY SEARCH'),
    ('MICHELLE¿S BEAR ESSENTIALS.', '----MICHELLE¿S BEAR ESSENTIALS. - PROXIMITY SEARCH'),
    ('TEST àâçèéêëîïôöùûü BEAR.', '----TEST àâçèéêëîïôöùûü BEAR. - PROXIMITY SEARCH'),
    ('TEST ÀÂÇÈÉÊËÎÏÔÖÙÛÜS BEAR.', '----TEST ÀÂÇÈÉÊËÎÏÔÖÙÛÜS BEAR. - PROXIMITY SEARCH'),
    ('TEST °£÷¥·©§¶¼½`¾¢!¦«ª¡¹²³»¿¬±¤®× BEAR.', '----TEST °£÷¥·©§¶¼½`¾¢!¦«ª¡¹²³»¿¬±¤®× BEAR. - PROXIMITY SEARCH'),
])
def test_bypass_nonascii_characters(client, jwt, app, criteria, seed):
    seed_database_with(client, jwt, seed)
    verify_synonym_match(client,
                         jwt,
                         query=criteria,
                         expected_list=[seed])
