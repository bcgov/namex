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
"""This module wraps the solr classes/fields for using solr."""

from contextlib import suppress
from http import HTTPStatus

from flask import Flask, current_app
from requests import Response, Session
from requests.adapters import HTTPAdapter, Retry
from requests.exceptions import ConnectionError as SolrConnectionError

from namex_solr_api.common.base_enum import BaseEnum
from namex_solr_api.exceptions import SolrException


class Solr:
    """Wrapper class around the solr instance."""

    def __init__(self, config_prefix: str, app: Flask = None):
        """Initialize the solr class."""
        self.app = None
        self.config_prefix = config_prefix

        # solr cores
        self.follower_core = None
        self.leader_core = None
        # solr urls
        self.follower_url = None
        self.leader_url = None
        # retry settings
        self.retry_total = None
        self.retry_backoff = 0
        # request timeout (seconds)
        self.solr_timeout = 60

        self.default_start = 0
        self.default_rows = 10

        # base urls
        self.reload_url = "{url}/admin/cores?action=RELOAD&core={core}"
        self.replication_url = "{url}/{core}/replication"
        self.search_url = "{url}/{core}/query"
        self.analysis_url = "{url}/{core}/analysis/field"
        self.synonyms_url = "{url}/{core}/schema/analysis/synonyms"
        self.update_url = "{url}/{core}/update?commit=true&overwrite=true&wt=json"
        self.bulk_update_url = "{url}/{core}/update?overwrite=true&wt=json"
        self.optimize_url = "{url}/{core}/update?optimize=true&maxSegments=1&waitFlush=false&wt=json"

        if app:
            self.init_app(app)

    def init_app(self, app: Flask):
        """Initialize the Solr environment."""
        self.app = app
        self.retry_total = app.config.get("SOLR_RETRY_TOTAL", 2)
        self.retry_backoff = app.config.get("SOLR_RETRY_BACKOFF_FACTOR", 5)
        self.solr_timeout = app.config.get(f"{self.config_prefix}_TIMEOUT", 60)
        # NOTE: for a single core implementation set leader/follower cores the same
        self.leader_core = app.config.get(f"{self.config_prefix}_LEADER_CORE")
        self.follower_core = app.config.get(f"{self.config_prefix}_FOLLOWER_CORE")
        # NOTE: for a single node implementation set the leader/follower urls the same
        self.leader_url = app.config.get(f"{self.config_prefix}_LEADER_URL")
        self.follower_url = app.config.get(f"{self.config_prefix}_FOLLOWER_URL")

    def call_solr(self,  # noqa: PLR0913
                  method: str,
                  query: str,
                  params: dict | None = None,
                  json_data: dict | None = None,
                  xml_data: str | None = None,
                  leader=True,
                  timeout=None) -> Response:
        """Call solr instance with given params."""
        base_url = self.leader_url if leader else self.follower_url
        core = self.leader_core if leader else self.follower_core
        url = query.format(url=base_url, core=core)
        if timeout is None:
            timeout = self.solr_timeout
        retries = Retry(total=self.retry_total,
                        backoff_factor=self.retry_backoff,
                        status_forcelist=[413, 429, 502, 503, 504],
                        allowed_methods=["GET", "POST"])
        session = Session()
        session.mount(url, HTTPAdapter(max_retries=retries))

        response = None
        try:
            if method == "GET":
                response = session.get(url, params=params, timeout=timeout)
            elif method == "POST" and json_data:
                response = session.post(url=url, json=json_data, timeout=timeout)
            elif method == "PUT" and json_data:
                response = session.put(url=url, json=json_data, timeout=timeout)
            elif method == "POST" and xml_data:
                headers = {"Content-Type": "application/xml"}
                response = session.post(url=url, data=xml_data, headers=headers, timeout=timeout)
            else:
                current_app.logger.debug(
                    f"Invalid function params: {method}, {query}, {params}, {json_data}, {xml_data}")
                raise Exception("Invalid params given.")  # pylint: disable=broad-exception-raised
            # check for error
            if response.status_code != HTTPStatus.OK:
                error = response.json().get("error", {}).get("msg", "Error handling Solr request.")
                raise Exception(error)  # pylint: disable=broad-exception-raised;

            return response

        except SolrConnectionError as err:
            current_app.logger.debug(err.with_traceback(None))
            raise SolrException(
                error="Connection error while handling Solr request.",
                status_code=HTTPStatus.GATEWAY_TIMEOUT) from err
        except Exception as err:
            current_app.logger.debug(err.with_traceback(None))
            current_app.logger.debug("method: %s, query: %s, params: %s, data: %s",
                                     method, query, params, xml_data or json_data)
            msg = "Error handling Solr request."
            status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            with suppress(Exception):
                status_code = response.status_code
                msg = response.json().get("error", {}).get("msg", msg)
            current_app.logger.debug(msg)
            raise SolrException(error=msg, status_code=status_code) from err

    def analyze_field(self, field_value: str, field_type: str, *, timeout: int = 5, fail_soft: bool = True) -> dict:
        """Return Solr analysis for a field type (follower).

        - fail_soft returns an empty dict when analysis is down (search callers fall back to raw terms)
        - fail_soft=False re-raises for write paths that must never persist unstemmed data.
        """
        try:
            response = self.call_solr(
                "GET",
                self.analysis_url,
                params={
                    "wt": "json",
                    "analysis.fieldvalue": field_value,
                    "analysis.fieldtype": field_type,
                },
                leader=False,
                timeout=timeout,
            )
            return response.json()
        except Exception:
            if not fail_soft:
                raise
            current_app.logger.warning("Solr analysis unavailable; synonym stem fallback skipped.")
            return {}

    def create_or_update_synonyms(self, synonym_type: BaseEnum, synonyms: dict[str: list[str]]):
        """Create or update solr docs in the core."""
        return self.call_solr("PUT", f"{self.synonyms_url}/{synonym_type.value}", json_data=synonyms, timeout=180)

    def delete_all_docs(self):
        """Delete all solr docs from the core."""
        payload = "<delete><query>*:*</query></delete>"
        response = self.call_solr("POST", self.update_url, xml_data=payload, timeout=60)
        return response

    def delete_docs(self, unique_keys: list[str]):
        """Delete solr docs from the core."""
        payload = "<delete><query>"
        if unique_keys:
            payload += f"id:{unique_keys[0].upper()}"
        for key in unique_keys[1:]:
            payload += f" OR id:{key.upper()}"
        payload += "</query></delete>"

        response = self.call_solr("POST", self.update_url, xml_data=payload, timeout=60)
        return response

    def query(self, payload: dict[str, str], start: int | None = None, rows: int | None = None) -> dict:
        """Return a list of solr docs from the solr query handler for the given params."""
        payload["offset"] = start if start else self.default_start
        payload["limit"] = rows if rows else self.default_rows
        response = self.call_solr("POST", self.search_url, json_data=payload, leader=False)
        return response.json()

    def optimize(self):
        """Trigger Solr optimize in the background (fire-and-forget)."""
        current_app.logger.info("Triggering Solr optimize in background...")
        resp = self.call_solr(method="GET", query=self.optimize_url, timeout=60)
        current_app.logger.info("Solr optimize triggered.")
        return resp

    def reload_core(self):
        """Reload the solr core."""
        current_app.logger.info("Reloading core...")
        reload = self.call_solr(method="GET", query=self.reload_url)
        current_app.logger.info("Core reloaded.")
        return reload

    def replication(self, command: str, leader=True):
        """Send a replication command to solr."""
        current_app.logger.info(f'Sending {command} command to {"leader" if leader else "follower"}')
        resp = self.call_solr(method="GET",
                              query=self.replication_url,
                              params={"command": command},
                              leader=leader)
        current_app.logger.info(f"{command} command executed.")
        return resp
