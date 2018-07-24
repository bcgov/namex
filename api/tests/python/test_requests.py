from flask import jsonify
from unittest import mock

token_header = {
                "alg": "RS256",
                "typ": "JWT",
                "kid": "flask-jwt-oidc-test-client"
               }
claims = {
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
                    "editor",
                    "approver",
                    "viewer",
                    "user"
                ]
            }
         }


def test_requests_post(client):
    rv = client.post('/')
    pass


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

    assert rv.data == json_msg.data
