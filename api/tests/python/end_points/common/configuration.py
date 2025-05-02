from namex.models import User

token_header = {'alg': 'RS256', 'typ': 'JWT', 'kid': 'flask-jwt-oidc-test-client'}

claims = {
    'iss': 'https://sso-dev.pathfinder.gov.bc.ca/auth/realms/sbc',
    'sub': '43e6a245-0bf7-4ccf-9bd0-e7fb85fd18cc',
    'aud': 'NameX-Dev',
    'exp': 31531718745,
    'iat': 1531718745,
    'jti': 'flask-jwt-oidc-test-support',
    'typ': 'Bearer',
    'username': 'test-user',
    'realm_access': {'roles': ['{}'.format(User.EDITOR), '{}'.format(User.APPROVER), 'viewer', 'user']},
}
