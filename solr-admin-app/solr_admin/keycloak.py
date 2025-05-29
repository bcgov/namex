import requests
from flask import current_app, session
from authlib.jose import jwt, JsonWebKey


# Manages Keycloak auth via OIDC using well-known config and JWKS for token validation.
# Used by SecuredView to protect admin views.
class Keycloak:
    _cached_well_known_config = None
    _cached_jwks_key_set = None

    '''
    Determines whether or not the user is authorized to use the application. True if the user is logged in.
    '''
    def has_access(self) -> bool:
        claims = self._get_validated_token_claims()
        roles = claims.get("realm_access", {}).get("roles", []) if claims else []
        return "names_manager" in roles

    '''
    Gets the redirect URL that is used to transfer the browser to the identity provider.
    '''
    def get_redirect_url(self, request_url: str) -> str:
        config = self._fetch_well_known_config()
        return (
            f"{config['authorization_endpoint']}?response_type=code"
            f"&client_id={current_app.config['JWT_OIDC_AUDIENCE']}"
            f"&redirect_uri={current_app.config['OIDC_REDIRECT_URI']}"
            f"&scope=openid"
            f"&state={request_url}"
        )

    '''
    Gets the username for the currently logged in user. This will be prefixed with the authentication scheme, such as
    "idir/" or "github/" - no prefix indicates that authentication is performed by the identity provider.
    '''
    def get_username(self) -> str:
        claims = self._get_validated_token_claims()
        return claims.get("preferred_username", "") if claims else ""

    '''
    Safely decode and validate the access token from session. Return the token claims if valid, or None if the token
    is missing, expired, invalid, or fails audience/issuer checks. Removes the token from session on failure.
    '''
    def _get_validated_token_claims(self):
        token = session.get("access_token")
        if not token:
            return None

        try:
            config = self._fetch_well_known_config()
            key_set = self._fetch_jwks_key_set()
            claims = jwt.decode(token, key_set, claims_params={
                "aud": current_app.config["JWT_OIDC_AUDIENCE"],
                "iss": config["issuer"]
            })
            claims.validate()
            return claims
        except Exception as e:
            current_app.logger.warning(f"Token decode failed: {e}")
            session.pop("access_token", None)
            return None

    '''
    Fetch and cache the OpenID Connect well-known configuration document.
    This includes endpoints and metadata like the issuer and JWKS URI.
    '''
    def _fetch_well_known_config(self):
        if not self._cached_well_known_config:
            response = requests.get(current_app.config["JWT_OIDC_WELL_KNOWN_CONFIG"], timeout=5)
            self._cached_well_known_config = response.json()
        return self._cached_well_known_config

    """
    Fetch and cache the JSON Web Key Set (JWKS) used to verify JWT signatures.
    Retrieves the keys from the JWKS URI in the well-known config and parses them into a usable format.
    """
    def _fetch_jwks_key_set(self):
        if not self._cached_jwks_key_set:
            config = self._fetch_well_known_config()
            jwks = requests.get(config["jwks_uri"], timeout=5).json()
            self._cached_jwks_key_set = JsonWebKey.import_key_set(jwks)
        return self._cached_jwks_key_set
