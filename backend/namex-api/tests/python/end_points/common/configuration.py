from namex.models import User

token_header = {'alg': 'RS256', 'typ': 'JWT', 'kid': 'flask-jwt-oidc-test-client'}

claims = {
    'iss': 'https://example.localdomain/auth/realms/example',
    'sub': '43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc',
    'aud': 'example',
    'exp': 31531718745,
    'iat': 1531718745,
    'jti': 'flask-jwt-oidc-test-support',
    'typ': 'Bearer',
    'username': 'test-user',
    'realm_access': {'roles': [User.EDITOR, User.APPROVER, 'viewer', 'user']},
}
