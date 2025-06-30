import os
from typing import Optional
from urllib.parse import urlparse

from flask import current_app
from google.auth.transport.requests import Request
from google.oauth2 import id_token


def _synonyms_api_url() -> Optional[str]:
    return current_app.config.get('SOLR_SYNONYMS_API_URL')


def _is_synonyms_api_request(url: str) -> bool:
    target = _synonyms_api_url()
    return bool(target) and urlparse(url).netloc == urlparse(target).netloc


def _get_identity_token() -> Optional[str]:
    audience = _synonyms_api_url()
    if not audience:
        return None

    if os.getenv('FLASK_ENV') == 'development':
        # JWT tokens can be generated on GCP console and returned as a string here for testing or in development.
        # 1. Go to the correct env on GCP console: -dev, -test, -prod.
        # 2. Launch the Goolge Cloud Shell from the GCP console.
        # 3. Enter: gcloud auth print-identity-token --audiences=<entry-your-target-url>
        # 4. Copy the token and paste it here as the return string value.
        return 'dev-dummy-token'

    try:
        return id_token.fetch_id_token(Request(), audience)
    except Exception as exc:
        current_app.logger.warning('Synonyms-API token fetch failed: %s', exc)
        return None


def patch_synonyms_api_requests():
    """Monkey-patch swagger_client to add Bearer token to Synonyms API calls."""
    import swagger_client
    from swagger_client.rest import RESTClientObject

    if getattr(swagger_client, "_synonyms_auth_patched", False):
        return

    real_request = RESTClientObject.request

    def custom_request(self, method, url, *args, **kwargs):
        if _is_synonyms_api_request(url):
            token = _get_identity_token()
            if token:
                headers = kwargs.get("headers") or {}
                headers["Authorization"] = f"Bearer {token}"
                kwargs["headers"] = headers
        return real_request(self, method, url, *args, **kwargs)

    RESTClientObject.request = custom_request
    swagger_client._synonyms_auth_patched = True

