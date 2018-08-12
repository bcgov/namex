from flask import jsonify
from unittest import mock
import sys
from namex.models import User

token_header = {
                "alg": "RS256",
                "typ": "JWT",
                "kid": "flask-jwt-oidc-test-client"
               }
claims = {
            "iss": "https://dev-sso.pathfinder.gov.bc.ca/auth/realms/nest",
            "sub": "43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc",
            "aud": "namex-DEV",
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


def test_get_next(client, jwt, app):

    # add NR to database
    from namex.models import Request as RequestDAO, State
    nr = RequestDAO()
    nr.nrNum='NR 0000001'
    nr.stateCd = State.DRAFT
    nr.save_to_db()

    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token}

    # The message expected to be returned
    json_msg = jsonify(nameRequest='NR 0000001')

    # get the resource (this is the test)
    rv = client.get('/api/v1/requests/queues/@me/oldest', headers=headers)

    assert json_msg.data == rv.data


def test_get_next_oldest(client, jwt, app):

    # add NR to database
    from namex.models import Request as RequestDAO, State
    nr = RequestDAO()
    nr.nrNum='NR 0000001'
    nr.stateCd = State.DRAFT
    nr.save_to_db()

    for i in range(2,12):
        nr = RequestDAO()
        nr.nrNum = 'NR {0:07d}'.format(i)
        nr.stateCd = State.DRAFT
        nr.save_to_db()

    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    headers = {'Authorization': 'Bearer ' + token}

    # The message expected to be returned
    json_msg = jsonify(nameRequest='NR 0000001')

    # get the resource (this is the test)
    rv = client.get('/api/v1/requests/queues/@me/oldest', headers=headers)

    print('the client returned:', rv.data)

    assert  json_msg.data == rv.data


claims_editor_only = {
            "iss": "https://dev-sso.pathfinder.gov.bc.ca/auth/realms/nest",
            "sub": "43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc",
            "aud": "namex-DEV",
            "exp": 21531718745,
            "iat": 1531718745,
            "jti": "flask-jwt-oidc-test-support",
            "typ": "Bearer",
            "username": "test-user",
            "realm_access": {
                "roles": [
                    "viewer",
                    "user"
                ]
            }
         }

def test_get_next_not_approver(client, jwt, app):

    # add NR to database
    from namex.models import Request as RequestDAO, State
    nr = RequestDAO()
    nr.nrNum='NR 0000001'
    nr.stateCd = State.DRAFT
    nr.save_to_db()

    # create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims_editor_only, token_header)
    headers = {'Authorization': 'Bearer ' + token}

    # The message expected to be returned
    json_msg = jsonify(message='Error: You do not have access to the Name Request queue.')

    # get the resource (this is the test)
    rv = client.get('/api/v1/requests/queues/@me/oldest', headers=headers)

    assert rv.data == json_msg.data
