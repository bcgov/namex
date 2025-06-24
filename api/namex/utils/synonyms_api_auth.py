"""
Synonyms API Authentication Middleware.

This module provides a automatic identity token injection for requests to the synonyms-api. 
"""

import urllib.request
from typing import Optional
from urllib.parse import urlparse

from flask import current_app
from google.auth.transport.requests import Request
from google.oauth2 import id_token


class SynonymsAPIAuthHandler(urllib.request.HTTPHandler, urllib.request.HTTPSHandler):
    """
    HTTP/HTTPS handler that injects service account identity token for synonyms API requests. 
    """

    def __init__(self):
        self._synonyms_api_url: Optional[str] = None
        self._synonyms_api_host: Optional[str] = None
    
    def _get_synonyms_api_url(self) -> Optional[str]:
        """Get the synonyms API URL from configutation."""
        if self._synonyms_api_url is None:
            self._synonyms_api_url = current_app.config.get('SOLR_SYNONYMS_API_URL', None)
        return self._synonyms_api_url

    def _get_synonyms_api_host(self) -> Optional[str]:
        """Get the synonyms API host from the URL."""
        if self._synonyms_api_host is None:
            url = self._get_synonyms_api_url()
            if url:
                parsed = urlparse(url)
                self._synonyms_api_host = parsed.netloc
        return self._synonyms_api_host
    
    def _is_synonyms_api_request(self, url: str) -> bool:
        """Check if the str contains the synonyms-api host."""
        synonyms_host = self._get_synonyms_api_host()
        if not synonyms_host:
            return False
        
        parsed = urlparse(url)
        return parsed.netloc == synonyms_host

    def _get_identity_token(self, audience: str) -> Optional[str]:
        """Get service account identity token for synonyms-api request authentication."""
        try:
            token = id_token.fetch_id_token(Request(), audience)

            if not token or not isinstance(token, str):
                current_app.logger.warning(f'Failed to get identity token.')
                return None

            return token
        except Exception as e:
            current_app.logger.warning(f'Error in gettting identity token: {str(e)}')
            return None
        
    def _inject_token_for_synonyms_api(self, request, url: str) -> None:
        """Injects the identity token for all synonyms-api requests."""
        if not self._is_synonyms_api_request(url):
            return
        
        synonyms_url = self._get_synonyms_api_url()
        if not synonyms_url:
            current_app.logger.warning('SOLR_SYNONYMS_API_URL not set.')
            return

        id_token = self._get_identity_token(synonyms_url)
        if id_token: 
            request.add_header('Authorization', f'Bearer {id_token}')
        else:
            current_app.logger.warning('Failed to get identity token for synonyms-api request.')

    def http_open(self, req): 
        """Injects identity token for synonyms HTTP requests."""
        self._add_auth_to_request(req, req.full_url)
        return super().http_open(req)

    def https_open(self, req):
        """Injects identity token for synonyms HTTPS requests."""
        self._add_auth_to_request(req, req.full_url)
        return super().https_open(req)


def install_synonyms_api_auth():
    """
    Install the synonyms API authentication interceptor.

    This function is called during application initialization.
    Once installed, all requests to the synonyms-api will include the identity token.
    """

    # Create custom opener with authenticated handler
    opener = urllib.request.build_opener(SynonymsAPIAuthHandler())

    # Install the opener as the default
    urllib.request.install_opener(opener)

    current_app.logger.info('Synonyms API authentication interceptor installed.')

def uninstall_synonyms_api_auth():
    """Uninstall the synonyms API authentication interceptor."""
    # Reinstall the default opener
    urllib.request.install_opener(urllib.request.build_opener())
    
    current_app.logger.info('Synonyms API authentication interceptor uninstalled')