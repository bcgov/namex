from functools import wraps

import jwt as pyjwt
import requests
from flask import Flask, abort, current_app, request
from flask_jwt_oidc import JwtManager
from jwt import PyJWKClient

jwt = JwtManager()


def setup_jwt_manager(app: Flask):
    """Initialize JWT configuration on the Flask app."""

    def get_roles(a_dict):
        return a_dict["realm_access"]["roles"]

    app.config["JWT_ROLE_CALLBACK"] = get_roles
    jwt.init_app(app)


def get_public_key(token: str) -> str:
    """Retrieve the public key for verifying the token from the JWKS endpoint."""
    config = requests.get(current_app.config.get("JWT_OIDC_WELL_KNOWN_CONFIG")).json()
    jwks_uri = config["jwks_uri"]
    jwks_client = PyJWKClient(jwks_uri)
    signing_key = jwks_client.get_signing_key_from_jwt(token)
    return signing_key.key


def requires_role(required_role: str):
    """Decorator to enforce that the JWT token received contains the required role."""

    def role_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                abort(401, description="Missing Authorization header")
            try:
                token = auth_header.split()[1]
                decoded_token = pyjwt.decode(
                    token,
                    get_public_key(token),
                    algorithms=["RS256"],
                    audience=current_app.config.get("JWT_OIDC_AUDIENCE"),
                )
            except Exception as e:
                abort(401, description=f"Token decoding failed: {str(e)}")

            roles = decoded_token.get("roles", [])
            if required_role not in roles:
                abort(403, description=f"Token missing '{required_role}' role")
            return func(*args, **kwargs)

        return wrapper

    return role_decorator
