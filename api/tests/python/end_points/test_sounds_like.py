from namex.models import User
import requests
import json
import pytest
from tests.python import integration_solr, integration_synonym_api
import urllib
from hamcrest import *


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


@pytest.fixture(scope="session", autouse=True)
def reload_schema(solr):
    url = solr + '/solr/admin/cores?action=RELOAD&core=possible.conflicts&wt=json'
    r = requests.get(url)

    assert r.status_code == 200


@integration_solr
def test_solr_available(solr, app, client, jwt):
    url = solr + '/solr/possible.conflicts/admin/ping'
    r = requests.get(url)

    assert r.status_code == 200


def clean_database(solr):
    url = solr + '/solr/possible.conflicts/update?commit=true'
    headers = {'content-type': 'text/xml'}
    data = '<delete><query>id:*</query></delete>'
    r = requests.post(url, headers=headers, data=data)

    assert r.status_code == 200


def seed_database_with(solr, name, id='1', source='CORP'):
    url = solr + '/solr/possible.conflicts/update?commit=true'
    headers = {'content-type': 'application/json'}
    data = '[{"source":"' + source + '", "name":"' + name + '", "id":"'+ id +'"}]'
    r = requests.post(url, headers=headers, data=data)

    assert r.status_code == 200


def verify(data, expected):

    print("Expected: ", expected)

    # remove the search divider(s): ----<query term>
    actual = [{ 'name':doc['name_info']['name'] } for doc in data['names']]

    print("Actual: ", actual)

    assert_that(len(actual), equal_to(len(expected)))
    for i in range(len(actual)):
        assert_that(actual[i]['name'], equal_to(expected[i]['name']))


def verify_results(client, jwt, query, expected):
    data = search(client, jwt, query)
    verify(data, expected)


def search(client, jwt, query):
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token}
    url = '/api/v1/requests/phonetics/' + urllib.parse.quote(query) + '/*'
    print(url)
    rv = client.get(url, headers=headers)

    assert rv.status_code == 200
    return json.loads(rv.data)


@integration_synonym_api
@integration_solr
def test_all_good(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'GOLDSTREAM ELECTRICAL LTD')
    verify_results(client, jwt,
       query='GOLDSMITHS',
       expected=[
           {'name': '----GOLDSMITHS'},
           {'name': 'GOLDSTREAM ELECTRICAL LTD'}
       ]
    )


@pytest.mark.skip(reason="Rhyming not implemented yet")
@integration_synonym_api
@integration_solr
def test_sounds_like(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'GAYLEDESIGNS INC.', id='1')
    seed_database_with(solr, 'GOLDSTREAM ELECTRICAL CORP', id='2')
    seed_database_with(solr, 'GLADSTONE JEWELLERY LTD', id='3')
    seed_database_with(solr, 'GOLDSTEIN HOLDINGS INC.', id='4')
    seed_database_with(solr, 'CLOUDSIDE INN INCORPORATED', id='5')
    seed_database_with(solr, 'GOLDSPRING PROPERTIES LTD', id='6')
    seed_database_with(solr, 'GOLDSTRIPES AVIATION INC', id='7')
    seed_database_with(solr, 'GLADSTONE CAPITAL CORP', id='8')
    seed_database_with(solr, 'KLETAS LAW CORPORATION', id='9')
    seed_database_with(solr, 'COLDSTREAM VENTURES INC.', id='10')
    seed_database_with(solr, 'BLABLA ANYTHING', id='11')
    verify_results(client, jwt,
       query='GOLDSMITHS',
       expected=[
           {'name': '----GOLDSMITHS'},
           {'name': 'COLDSTREAM VENTURES INC.'},
           {'name': 'GOLDSPRING PROPERTIES LTD'},
           {'name': 'GOLDSTEIN HOLDINGS INC.'},
           {'name': 'GOLDSTREAM ELECTRICAL CORP'},
           {'name': 'GOLDSTRIPES AVIATION INC'},
       ]
    )


@integration_synonym_api
@integration_solr
def test_liberti(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'LIBERTI', id='1')
    verify_results(client, jwt,
       query='LIBERTY',
       expected=[
           {'name': '----LIBERTY'},
           {'name': 'LIBERTI'},
       ]
    )


@integration_synonym_api
@integration_solr
def test_deeper(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'LABORATORY', id='1')
    seed_database_with(solr, 'LAPORTE', id='2')
    seed_database_with(solr, 'LIBERTI', id='3')
    verify_results(client, jwt,
       query='LIBERTY',
       expected=[
           {'name': '----LIBERTY'},
           {'name': 'LIBERTI'},
       ]
    )


@integration_synonym_api
@integration_solr
def test_jasmine(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'JASMINE', id='1')
    verify_results(client, jwt,
       query='OSMOND',
       expected=[
           {'name': '----OSMOND'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_fey(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'FEY', id='1')
    verify_results(client, jwt,
       query='FAY',
       expected=[
           {'name': '----FAY'},
           {'name': 'FEY'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_venizia(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'VENIZIA', id='1')
    seed_database_with(solr, 'VENEZIA', id='2')
    seed_database_with(solr, 'VANSEA', id='3')
    seed_database_with(solr, 'WENSO', id='4')
    verify_results(client, jwt,
       query='VENIZIA',
       expected=[
           {'name': '----VENIZIA'},
           {'name': 'VENEZIA'},
       ]
    )


@integration_synonym_api
@integration_solr
def test_ys_and_is(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'CRYSTAL', id='1')
    verify_results(client, jwt,
       query='CRISTAL',
       expected=[
           {'name': '----CRISTAL'},
           {'name': 'CRYSTAL'},
       ]
    )


@integration_synonym_api
@integration_solr
def test_cs_and_ks(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'KOLDSMITHS', id='1')
    verify_results(client, jwt,
       query='COLDSTREAM',
       expected=[
           {'name': '----COLDSTREAM'},
           {'name': 'KOLDSMITHS'},
       ]
    )


@integration_synonym_api
@integration_solr
def test_cs_and_ks_again(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'CRAZY', id='1')
    seed_database_with(solr, 'KAIZEN', id='2')
    verify_results(client, jwt,
       query='CAYZEN',
       expected=[
           {'name': '----CAYZEN'},
           {'name': 'KAIZEN'},
       ]
    )


@integration_synonym_api
@integration_solr
def test_resist_short_word(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'FE', id='1')
    verify_results(client, jwt,
       query='FA',
       expected=[
           {'name': '----FA'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_resist_single_vowel(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'FEDS', id='1')
    verify_results(client, jwt,
       query='FADS',
       expected=[
           {'name': '----FADS'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_feel(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'FEEL', id='1')
    verify_results(client, jwt,
       query='FILL',
       expected=[
           {'name': '----FILL'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_bear(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'BEAR', id='1')
    verify_results(client, jwt,
       query='BARE',
       expected=[
           {'name': '----BARE'},
           {'name': 'BEAR'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_ignore_corp(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'GLADSTONE CAPITAL corp', id='1')
    verify_results(client, jwt,
       query='GOLDSMITHS',
       expected=[
           {'name': '----GOLDSMITHS'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_designation_in_query_is_ignored(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'FINGER LIMATED', id='1')
    verify_results(client, jwt,
       query='SUN LIMITED',
       expected=[
           {'name': '----SUN'}
       ]
    )


@integration_synonym_api
@integration_solr
def leak(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'LEAK', id='1')
    verify_results(client, jwt,
       query='LEEK',
       expected=[
           {'name': 'LEAK'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_plank(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'PLANCK', id='1')
    verify_results(client, jwt,
       query='PLANK',
       expected=[
           {'name': '----PLANK'},
           {'name': 'PLANCK'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_krystal(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'KRYSTAL', id='1')
    verify_results(client, jwt,
       query='CRISTAL',
       expected=[
           {'name': '----CRISTAL'},
           {'name': 'KRYSTAL'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_christal(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'KRYSTAL', id='1')
    verify_results(client, jwt,
       query='CHRISTAL',
       expected=[
           {'name': '----CHRISTAL'},
           {'name': 'KRYSTAL'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_kl(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'KLASS', id='1')
    verify_results(client, jwt,
       query='CLASS',
       expected=[
           {'name': '----CLASS'},
           {'name': 'KLASS'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_pheel(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'PHEEL', id='1')
    verify_results(client, jwt,
       query='FEEL',
       expected=[
           {'name': '----FEEL'},
           {'name': 'PHEEL'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_ghable(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'GHABLE', id='1')
    verify_results(client, jwt,
       query='GABLE',
       expected=[
           {'name': '----GABLE'},
           {'name': 'GHABLE'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_gnat(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'GNAT', id='1')
    verify_results(client, jwt,
       query='NAT',
       expected=[
           {'name': '----NAT'},
           {'name': 'GNAT'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_kn(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'KNAT', id='1')
    verify_results(client, jwt,
       query='NAT',
       expected=[
           {'name': '----NAT'},
           {'name': 'KNAT'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_pn(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'PNEU', id='1')
    verify_results(client, jwt,
       query='NEU',
       expected=[
           {'name': '----NEU'},
           {'name': 'PNEU'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_wr(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'WREN', id='1')
    verify_results(client, jwt,
       query='REN',
       expected=[
           {'name': '----REN'},
           {'name': 'WREN'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_rh(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'RHEN', id='1')
    verify_results(client, jwt,
       query='REN',
       expected=[
           {'name': '----REN'},
           {'name': 'RHEN'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_soft_c_is_not_k(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'KIRK', id='1')
    verify_results(client, jwt,
       query='CIRCLE',
       expected=[
           {'name': '----CIRCLE'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_oi_oy(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'OYSTER', id='1')
    verify_results(client, jwt,
       query='OISTER',
       expected=[
           {'name': '----OISTER'},
           {'name': 'OYSTER'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_dont_add_match_twice(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'RHEN GNAT', id='1')
    verify_results(client, jwt,
       query='REN NAT',
       expected=[
           {'name': '----REN NAT'},
           {'name': 'RHEN GNAT'},
           {'name': '----REN'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_neighbour(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'NEIGHBOUR', id='1')
    verify_results(client, jwt,
       query='NAYBOR',
       expected=[
           {'name': '----NAYBOR'},
           {'name': 'NEIGHBOUR'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_mac_mc(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'MCGREGOR', id='1')
    verify_results(client, jwt,
       query='MACGREGOR',
       expected=[
           {'name': '----MACGREGOR'},
           {'name': 'MCGREGOR'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_ex_x(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'EXTREME', id='1')
    verify_results(client, jwt,
       query='XTREME',
       expected=[
           {'name': '----XTREME'},
           {'name': 'EXTREME'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_wh(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'WHITE', id='1')
    verify_results(client, jwt,
       query='WITE',
       expected=[
           {'name': '----WITE'},
           {'name': 'WHITE'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_qu(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'KWIK', id='1')
    verify_results(client, jwt,
       query='QUICK',
       expected=[
           {'name': '----QUICK'},
           {'name': 'KWIK'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_ps(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'PSYCHO', id='1')
    verify_results(client, jwt,
       query='SYCHO',
       expected=[
           {'name': '----SYCHO'},
           {'name': 'PSYCHO'}
       ]
    )


@pytest.mark.skip(reason="not handled yet")
@integration_synonym_api
@integration_solr
def test_terra(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'TERRA', id='1')
    verify_results(client, jwt,
       query='TARA',
       expected=[
           {'name': 'TERRA'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_ayaan(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'AYAAN', id='1')
    verify_results(client, jwt,
       query='AYAN',
       expected=[
           {'name': '----AYAN'},
           {'name': 'AYAAN'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_aggri(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'AGGRI', id='1')
    verify_results(client, jwt,
       query='AGRI',
       expected=[
           {'name': '----AGRI'},
           {'name': 'AGGRI'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_kofi(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'KOFI', id='1')
    verify_results(client, jwt,
       query='COFFI',
       expected=[
           {'name': '----COFFI'},
           {'name': 'KOFI'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_tru(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'TRU', id='1')
    verify_results(client, jwt,
       query='TRUE',
       expected=[
           {'name': '----TRUE'},
           {'name': 'TRU'}
       ]
    )


@pytest.mark.skip(reason="not handled yet")
@integration_synonym_api
@integration_solr
def test_dymond(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'DYMOND', id='1')
    verify_results(client, jwt,
       query='DIAMOND',
       expected=[
           {'name': 'DYMOND'}
       ]
    )


@pytest.mark.skip(reason="compound words not handled yet")
@integration_synonym_api
@integration_solr
def test_bee_kleen(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'BEE KLEEN', id='1')
    verify_results(client, jwt,
       query='BE-CLEAN',
       expected=[
           {'name': 'BEE KLEEN'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_ignore_exact_match_keep_phonetic(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'BODY BLUEPRINT FITNESS INC.', id='1')
    seed_database_with(solr, 'BLUEPRINT BEAUTEE', id='2')
    verify_results(client, jwt,
       query='BLUEPRINT BEAUTY',
       expected=[
           {'name': '----BLUEPRINT BEAUTY'},
           {'name': 'BLUEPRINT BEAUTEE'},
           {'name': '----BLUEPRINT synonyms:(BEAUTI)'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_match_both_words(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'ANDERSON BEHAVIOR CONSULTING', id='1')
    verify_results(client, jwt,
       query='INTERVENTION BEHAVIOUR',
       expected=[
           {'name': '----INTERVENTION BEHAVIOUR'},
           {'name': '----INTERVENTION'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_match_at_right_level(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'ANDERSON BEHAVIOR CONSULTING INC.', id='1')
    verify_results(client, jwt,
       query='BEHAVIOUR INTERVENTION',
       expected=[
           {'name': '----BEHAVIOUR INTERVENTION'},
           {'name': '----BEHAVIOUR'},
           {'name': 'ANDERSON BEHAVIOR CONSULTING INC.'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_resists_qword_matching_several_words(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'ANDERSON BEHAVIOR BEHAVIOR', id='1')
    verify_results(client, jwt,
       query='BEHAVIOUR INTERVENTION',
       expected=[
           {'name': '----BEHAVIOUR INTERVENTION'},
           {'name': '----BEHAVIOUR'},
           {'name': 'ANDERSON BEHAVIOR BEHAVIOR'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_leading_vowel_a(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'AILEEN ENTERPRISES', id='1')
    verify_results(client, jwt,
       query='ALAN HARGREAVES CORPORATION',
       expected=[
           {'name': '----ALAN HARGREAVES'},
           {'name': '----ALAN'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_leading_vowel_e(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'ACME', id='1')
    verify_results(client, jwt,
       query='EQUIOM',
       expected=[
           {'name': '----EQUIOM'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_leading_vowel_not_match_consonant(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'HELENAH WU & CO. INC.', id='1')
    seed_database_with(solr, 'A BETTER WAY HERBALS LTD.', id='2')
    verify_results(client, jwt,
       query='EH',
       expected=[
           {'name': '----EH'}
       ]
    )


@integration_synonym_api
@integration_solr
def test_unusual_result(solr, client, jwt, app):
    clean_database(solr)
    seed_database_with(solr, 'DOUBLE J AVIATION LTD.', id='1')
    verify_results(client, jwt,
       query='TABLE',
       expected=[
           {'name': '----TABLE'}
       ]
    )

@integration_synonym_api
@integration_solr
def test_stack_ignores_wildcards(client, jwt, app):
    verify_results(client, jwt,
        query="TESTING* @WILDCARDS",
        expected=[
            {'name': '----TESTING WILDCARDS'},
            {'name': '----TESTING'}
        ]
    )

@integration_synonym_api
@integration_solr
@pytest.mark.parametrize("query", [
    ('T.H.E.'),
    ('COMPANY'),
    ('ASSN'),
    ('THAT'),
    ('LIMITED CORP.'),
])
def test_query_stripped_to_empty_string(solr,client, jwt, query):
    clean_database(solr)
    seed_database_with(solr, 'JM Van Damme inc', id='1')
    seed_database_with(solr, 'SOME RANDOM NAME', id='2')
    verify_results(client, jwt,
        query=query,
        expected=[{'name':'----*'}]
    )
