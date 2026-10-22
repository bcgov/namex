# Copyright © 2023 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Data for the JWT tokens."""

from typing import List


def helper_create_jwt(
    jwt_manager,
    roles: List[str] = [],
    username: str = 'test-user',
    email: str = None,
    firstname: str = None,
    lastname: str = None,
    login_source: str = None,
    sub: str = None,
    idp_userid: str = None,
):
    """Create a jwt bearer token with the correct keys, roles and username."""
    token_header = {'alg': 'RS256', 'typ': 'JWT', 'kid': 'flask-jwt-oidc-test-client'}
    claims = {
        'iss': 'https://example.localdomain/auth/realms/example',
        'sub': sub,
        'aud': 'example',
        'exp': 2539722391,
        'iat': 1539718791,
        'jti': 'flask-jwt-oidc-test-support',
        'typ': 'Bearer',
        'username': f'{username}',
        'firstname': firstname,
        'lastname': lastname,
        'email': email,
        'loginSource': login_source,
        'idp_userid': idp_userid,
        'realm_access': {'roles': [] + roles},
    }
    return jwt_manager.create_jwt(claims, token_header)


def create_header(
    jwt_manager,
    roles: List[str] = [],
    username: str = 'test-user',
    firstname: str = None,
    lastname: str = None,
    email: str = None,
    login_source: str = None,
    sub: str = '43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc',
    idp_userid: str = '123',
    **kwargs,
):
    """Return a header containing a JWT bearer token."""
    token = helper_create_jwt(
        jwt_manager,
        roles=roles,
        username=username,
        firstname=firstname,
        lastname=lastname,
        email=email,
        login_source=login_source,
        idp_userid=idp_userid,
        sub=sub,
    )
    headers = {**kwargs, **{'Authorization': 'Bearer ' + token}}
    return headers
