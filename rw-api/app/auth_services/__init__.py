"""Keycloak Auth Services
"""
from app import api
from flask import jsonify, request
from jose import jwt


class AuthError(Exception):
    def __int__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@api.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


def get_token_auth_header():
    """Obtains access token from the Authorizatio Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                         "description": "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                         "description":
                            "Authorization header must start with" 
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                         "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                         "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    return token


def required_scope(required_scope):
    """Determines if the required scope is present in the access token
    Args:
        required_scope(str): scope needed to access resource
    """
    token = get_token_auth_header()
    unverified_claims = jwt.get_unverified_claims(token)

    if unverified_claims.get("scope"):  # is this a boolean or just checking if its there or ?
        # pass
        token_scopes = unverified_claims["scope"].split()
        for token_scope in token_scopes:
            if token_scope == required_scope:
                return True

    if unverified_claims.get('realm_access'):
        roles = unverified_claims.get('realm_access').get('roles')
        if roles and required_scope in roles:
            return True

    return False
