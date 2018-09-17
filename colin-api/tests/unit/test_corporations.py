from unittest import mock
import sys
from namex.models import User


def test_readyz(client):
    print('got to readyz')
    url = 'api/v1/corporations/readyz'
    response = client.get(url)
    assert response.status_code == 200

def test_healthz(client):
    url = 'api/v1/corporations/healthz'
    response = client.get(url)
    assert response.status_code == 200
    assert response.json['message'] == 'api is healthy'

def test_not_authenticated(client):
    url = 'api/v1/corporations/A0003650'

    response = client.get(url)

    assert response.status_code == 401


token_header = {
                "alg": "RS256",
                "typ": "JWT",
                "kid": "flask-jwt-oidc-test-client"
               }
claims = {
            "iss": "https://sso-dev.pathfinder.gov.bc.ca/auth/realms/sbc",
            "sub": "43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc",
            "aud": "NameX-Dev",
            "exp": 99999999999,
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


def test_get_corpinfo(client, jwt, app):

    # try:
        token = jwt.create_jwt(claims, token_header)
        headers = {'Authorization': 'Bearer ' + token}
        url = 'api/v1/corporations/A0003650'

        response = client.get(url, headers=headers)
        print(response)

        assert response.status_code == 200
    # except Exception as err:
    #     print(err)
