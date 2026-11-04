# Copyright © 2025 Province of British Columbia
#
# Licensed under the BSD 3 Clause License, (the "License");
# you may not use this file except in compliance with the License.
# The template for the license can be found here
#    https://opensource.org/license/bsd-3-clause/
#
# Redistribution and use in source and binary forms,
# with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS”
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
"""Manages auth service interactions."""
from http import HTTPStatus

import requests
from flask import Flask, current_app, request
from flask_caching import Cache
from requests import Session, exceptions
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from namex_solr_api.exceptions import ExternalServiceException
from namex_solr_api.services.jwt import jwt

auth_cache = Cache()


class AuthService:
    """Provides utility functions for connecting with the BC Registries auth-api and SSO service."""

    app: Flask = None
    svc_url: str = None
    timeout: int = None
    sso_svc_token_url: str = None
    sso_svc_timeout: int = None
    svc_acc_id: str = None
    svc_acc_secret: str = None

    def __init__(self, app: Flask = None):
        """Initialize the auth service."""
        if app:
            self.init_app(app)

    def init_app(self, app: Flask):
        """Initialize app dependent variables."""
        self.app = app
        self.svc_url = app.config.get('AUTH_SVC_URL')
        self.timeout = app.config.get('AUTH_SVC_TIMEOUT', 20)
        self.sso_svc_token_url = app.config.get('ACCOUNT_SVC_AUTH_URL')
        self.sso_svc_timeout = app.config.get('ACCOUNT_SVC_TIMEOUT', 20)
        self.svc_acc_id = app.config.get('ACCOUNT_SVC_CLIENT_ID')
        self.svc_acc_secret = app.config.get('ACCOUNT_SVC_CLIENT_SECRET')
        auth_cache.init_app(app)

    @auth_cache.cached(timeout=300, key_prefix='view/token')
    def get_bearer_token(self):
        """Get a valid Bearer token for the service to use."""
        data = 'grant_type=client_credentials'
        try:
            res = requests.post(
                url=self.sso_svc_token_url,
                data=data,
                headers={'content-type': 'application/x-www-form-urlencoded'},
                auth=(self.svc_acc_id, self.svc_acc_secret),
                timeout=self.sso_svc_timeout,
            )
            if res.status_code != HTTPStatus.OK:
                raise ConnectionError({'statusCode': res.status_code, 'json': res.json()})
            return res.json().get('access_token')
        except exceptions.Timeout as err:
            self.app.logger.debug('SSO SVC connection timeout: %s', err.with_traceback(None))
            raise ExternalServiceException(
                status_code=HTTPStatus.GATEWAY_TIMEOUT,
                error=err.with_traceback(None),
                message='Unable to get service account token.',
            ) from err
        except Exception as err:
            self.app.logger.debug('SSO SVC connection failure: %s', err.with_traceback(None))
            raise ExternalServiceException(
                status_code=HTTPStatus.GATEWAY_TIMEOUT,
                error=err.with_traceback(None),
                message='Unable to get service account token.',
            ) from err
    
    def get_cache_key(self, *args, **kwargs):
        """Return the cache key for the given args.

        Expects all values as args OR all values as kwargs.
        """
        try:
            token: str = jwt.get_token_auth_header()
            key: str = kwargs.get('path', args[0])
            return 'auth' + token + str(key)
        except Exception:
            current_app.logger.error('Unable to build cache key from user header.')

    @auth_cache.cached(timeout=600, make_cache_key=get_cache_key)
    def _call_auth_api(self, path: str) -> dict:
        """Return the auth api response for the given endpoint path."""
        response = None
        # Expects to be called within the context of a request
        if not request:
            return response

        current_app.logger.debug(f"Auth getting {path}...")
        api_url = self.svc_url + "/" if self.svc_url[-1] != "/" else self.svc_url
        api_url += path

        try:
            headers = {
                # Uses the authorization header from the user request
                "Authorization": request.headers.get('Authorization'),
                "Content-Type": "application/json"
            }
            with Session() as http:
                retries = Retry(total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
                http.mount("http://", HTTPAdapter(max_retries=retries))
                ret_val = http.get(url=api_url, headers=headers)
                current_app.logger.debug(f"Auth get {path} response status: {ret_val.status_code!s}")
                response = ret_val.json()
        except (
            exceptions.ConnectionError,
            exceptions.Timeout,
            ValueError,
            Exception,
        ) as err:
            current_app.logger.debug(f"Auth api connection failure using svc:{api_url}", err)
            raise ExternalServiceException(
                HTTPStatus.SERVICE_UNAVAILABLE,
                [{"message": "Unable to get information from auth.", "reason": err.with_traceback(None)}],
            ) from err
        return response
    
    def get_user_info(self):
        """Return basic user info from auth based on the request context."""
        return self._call_auth_api('users/@me')
