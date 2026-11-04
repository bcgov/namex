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
"""Manages util methods for updating possible conflict records via the namex solr api."""

import time
from datetime import datetime
from http import HTTPStatus

import requests
from flask import current_app

from namex_solr_api.exceptions import SolrException
from namex_solr_importer import auth


def _get_wait_interval(err: Exception):
    """Return the base wait interval for the exception."""
    if (
        isinstance(err.args, tuple | list)
        and err.args
        and isinstance(err.args[0], dict)
        and "408" in err.args[0].get("error", {}).get("detail", "")
    ):
        # increased base wait time for solr 408 error
        return 60
    return 20


def import_conflicts(docs: list[dict], data_name: str, partial=False) -> int:
    """Import data via namex solr api."""
    current_app.logger.debug("Getting token for Import...")
    token = auth.get_bearer_token()
    headers = {"Authorization": "Bearer " + token}
    current_app.logger.debug("Token set.")
    count = 0
    offset = 0
    rows = current_app.config["BATCH_SIZE"]
    retry_count = 0
    while count < len(docs) and rows > 0 and len(docs) - offset > 0:
        batch_amount = int(min(rows, len(docs) - offset) / (retry_count + 1))
        count += batch_amount
        # call api import endpoint
        try:
            current_app.logger.debug("Importing batch...")
            import_resp = requests.put(
                url=f"{current_app.config.get('SOLR_API_URL')}/internal/solr/import",
                headers=headers,
                json={
                    "possibleConflicts": docs[offset:count],
                    "timeout": "60",
                    "type": "partial" if partial else "full",
                },
                timeout=90,
            )

            if import_resp.status_code != HTTPStatus.CREATED:
                if import_resp.status_code == HTTPStatus.UNAUTHORIZED:
                    # renew token for next try
                    current_app.logger.debug("Getting new token for Import...")
                    token = auth.get_bearer_token()
                    headers = {"Authorization": "Bearer " + token}
                    current_app.logger.debug("New Token set.")
                # try again
                raise Exception(  # pylint: disable=broad-exception-raised
                    {
                        "error": import_resp.json(),
                        "status_code": import_resp.status_code,
                    }
                )  # pylint: disable=broad-exception-raised
            retry_count = 0
        except Exception as err:
            current_app.logger.debug(err)
            if retry_count < 5:  # noqa: PLR2004
                # retry
                current_app.logger.debug(
                    "Failed to update solr with batch. Trying again (%s of 5)...",
                    retry_count + 1,
                )
                retry_count += 1
                # await some time before trying again
                base_wait_time = _get_wait_interval(err)
                current_app.logger.debug(
                    "Awaiting %s seconds before trying again...",
                    base_wait_time * retry_count,
                )
                time.sleep(base_wait_time * retry_count)
                # set count back
                count -= batch_amount
                continue
            if retry_count == 5:  # noqa: PLR2004
                # wait x minutes and then try one more time
                current_app.logger.debug(
                    "Max retries for batch exceeded. Awaiting 2 mins before trying one more time..."
                )
                time.sleep(120)
                # renew token for next try
                current_app.logger.debug("Getting new token for Import...")
                token = auth.get_bearer_token()
                headers = {"Authorization": "Bearer " + token}
                current_app.logger.debug("New Token set.")
                # try again
                retry_count += 1
                count -= batch_amount
                continue
            # log and raise error
            current_app.logger.error("Retry count exceeded for batch.")
            raise SolrException(
                "Retry count exceeded for updating SOLR. Aborting import."
            ) from err
        offset = count
        current_app.logger.debug(
            f"Total batch {data_name} doc records imported: {count}"
        )
    return count


def resync(since: datetime | None = None):
    """Resync to catch any records that had an update during the import."""
    current_app.logger.debug("Getting token for Resync...")
    token = auth.get_bearer_token()
    headers = {"Authorization": "Bearer " + token}

    payload = {"minutesOffset": current_app.config.get("RESYNC_OFFSET")}
    if since:
        payload = {"since": since.isoformat()}
        current_app.logger.debug("Using explicit resync watermark: %s", payload["since"])

    current_app.logger.debug("Resyncing any overwritten docs during import...")
    resync_resp = requests.post(
        url=f"{current_app.config.get('SOLR_API_URL')}/internal/solr/update/resync",
        headers=headers,
        json=payload,
        timeout=60,
    )
    if resync_resp.status_code != HTTPStatus.CREATED:
        if resync_resp.status_code == HTTPStatus.GATEWAY_TIMEOUT:
            current_app.logger.debug(
                "Resync timed out -- check api for any individual failures."
            )
        else:
            current_app.logger.error(
                "Resync failed: %s, %s", resync_resp.status_code, resync_resp.json()
            )
    else:
        current_app.logger.debug("Resync complete.")


def update_synonyms(payload: dict):
    """Update synonyms via the solr api endpoint."""
    current_app.logger.debug("Getting token for Synonym Update...")
    token = auth.get_bearer_token()
    headers = {"Authorization": "Bearer " + token}
    current_app.logger.debug("Token set.")
    current_app.logger.debug("Updating Synonyms...")
    try:
        resp = requests.put(
            url=f"{current_app.config.get('SOLR_API_URL')}/internal/solr/update/synonyms?prune=true",
            headers=headers,
            json={"ALL": payload},
            timeout=1200,
        )

        if resp.status_code != HTTPStatus.OK:
            raise Exception(  # pylint: disable=broad-exception-raised
                {
                    "error": resp.json(),
                    "status_code": resp.status_code,
                }
            )
    except Exception as err:
        current_app.logger.debug(f"Error updating synonyms: {err.with_traceback(None)}")
        raise err
