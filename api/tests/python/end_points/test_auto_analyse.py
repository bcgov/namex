from flask import jsonify
from flask import json

from namex.models import User

from tests.python import integration_oracle_namesdb


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

API_BASE_URI = '/api/v1/'
ENDPOINT_PATH = 'name-analysis'

def test_get_analysis(client, jwt, app):
    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

    route = API_BASE_URI + ENDPOINT_PATH
    response = client.get(route, headers=headers)
    print(response)


# Test each of the response strategies
# API Returns
# Requires addition of distinctive word
# Requires addition of descriptive word
# Name Contains a Word To Avoid
# Designation Mismatch
# Too Many Words
# Name Requires Consent
# Contains Unclassifiable Word
# Conflicts with the Corporate Database
def test_valid_response(client, jwt, app):
    pass


def test_add_distinctive_word_response(client, jwt, app):
    pass


def test_add_descriptive_word_response(client, jwt, app):
    pass


def test_contains_words_to_avoid_response(client, jwt, app):
    pass


def test_designation_mismatch_response(client, jwt, app):
    pass


def test_too_many_words_response(client, jwt, app):
    pass


def test_name_requires_consent_response(client, jwt, app):
    pass


def test_contains_unclassifiable_word_response(client, jwt, app):
    pass


def test_corporate_name_conflict_response(client, jwt, app):
    pass
