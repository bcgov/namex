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


"""Wrapper methods to call the namex-solr-api reindex endpoints."""

from http import HTTPStatus

import requests
from flask import current_app

from namex_solr_api.exceptions import SolrException
from namex_solr_importer import auth


def _call_reindex_endpoint(endpoint: str, timeout: int = 1800) -> bool:
    """Helper to call a reindex endpoint via HTTP."""
    token = auth.get_bearer_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{current_app.config['SOLR_API_URL']}/internal/solr/reindex/{endpoint}"

    current_app.logger.debug(f"Calling reindex endpoint: '{endpoint}' ...")
    try:
        resp = requests.post(url, headers=headers, timeout=timeout)
        if resp.status_code not in (
            HTTPStatus.OK,
            HTTPStatus.CREATED,
            HTTPStatus.ACCEPTED,
        ):
            raise SolrException(
                f"Reindex endpoint '{endpoint}' failed.",
                (
                    resp.json()
                    if resp.headers.get("Content-Type") == "application/json"
                    else resp.text
                ),
                resp.status_code,
            )
        current_app.logger.debug(
            f"Reindex endpoint '{endpoint}' completed successfully."
        )
        return True
    except Exception as err:
        current_app.logger.error(f"Reindex endpoint '{endpoint}' failed: {err}")
        raise


def reindex_optimize() -> bool:
    """Trigger Solr optimize via the API."""
    return _call_reindex_endpoint("optimize")


def reindex_prep() -> bool:
    """Trigger pre-reindex operations via the API."""
    return _call_reindex_endpoint("prep")


def reindex_post() -> bool:
    """Trigger post-reindex operations via the API."""
    return _call_reindex_endpoint("post")


def reindex_recovery() -> bool:
    """Trigger reindex recovery operations via the API."""
    return _call_reindex_endpoint("recovery")
