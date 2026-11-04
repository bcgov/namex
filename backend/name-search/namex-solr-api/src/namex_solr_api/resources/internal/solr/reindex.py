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

"""API endpoints for granular reindex operations in SOLR."""

from datetime import UTC, datetime
from http import HTTPStatus
from time import sleep

from flask import Blueprint, current_app, jsonify
from flask_cors import cross_origin

from namex_solr_api.exceptions import SolrException, exception_response
from namex_solr_api.models import User
from namex_solr_api.services import jwt, solr

bp = Blueprint("REINDEX", __name__, url_prefix="/reindex")


# -----------------------------
# Helper function
# -----------------------------
def get_replication_detail(field: str, leader: bool):
    """Return the replication detail for the core, safely handling optional follower."""
    details: dict = solr.replication("details", leader).json().get("details", {})

    # Remove unwanted data
    if field != "commits" and "commits" in details:
        del details["commits"]

    follower_details = details.get("follower", {})  # safe fallback
    if not leader and field != "leaderDetails" and "leaderDetails" in follower_details:
        del follower_details["leaderDetails"]

    current_app.logger.debug("Full replication details: %s", details)

    if leader:
        return details.get(field)
    return follower_details.get(field)


# -----------------------------
# Optimize
# -----------------------------
@bp.post("/optimize")
@cross_origin(origins="*")
@jwt.requires_roles([User.Role.system.value])
def reindex_optimize_endpoint():
    """Run Solr optimize to merge all index segments into one."""
    try:
        current_app.logger.debug("Optimizing leader index to merge segments...")
        solr.optimize()
        return jsonify({"message": "Optimize completed successfully."}), HTTPStatus.OK
    except Exception as err:
        current_app.logger.warning(f"Optimize request failed (may be running in background): {err}")
        return exception_response(err)


# -----------------------------
# Reindex Prep
# -----------------------------
@bp.post("/prep")
@cross_origin(origins="*")
@jwt.requires_roles([User.Role.system.value])
def reindex_prep_endpoint():
    """Execute pre-reindex operations (backup, disable polling, delete index)."""
    try:
        backup_trigger_time = datetime.now(UTC)
        current_app.logger.debug("Triggering leader backup...")
        backup = solr.replication("backup", True)
        current_app.logger.debug(backup.json())

        if current_app.config.get("HAS_FOLLOWER", True):
            disable_polling = solr.replication("disablepoll", False)
            current_app.logger.debug(disable_polling.json())

        current_app.logger.debug("Pausing 60s for backup/polling...")
        sleep(60)

        # Verify backup
        backup_succeeded = False
        for i in range(20):
            current_app.logger.debug(f"Checking new backup {i+1}/20...")
            if backup_detail := get_replication_detail("backup", True):
                start_time_str = backup_detail.get("startTime")
                if start_time_str and backup_detail.get("status") == "success":
                    backup_start_time = datetime.fromisoformat(start_time_str)
                    if backup_trigger_time < backup_start_time:
                        backup_succeeded = True
                        break
            sleep(30 + (i*2))

        if not backup_succeeded:
            raise SolrException("Failed to backup leader index", HTTPStatus.INTERNAL_SERVER_ERROR)

        if current_app.config.get("HAS_FOLLOWER", True):
            is_polling_disabled = get_replication_detail("isPollingDisabled", False)
            if is_polling_disabled is None:
                current_app.logger.warning("Follower details missing; cannot verify polling status.")
            elif not bool(is_polling_disabled):
                raise SolrException(
                    "Failed to disable polling on follower",
                    str(is_polling_disabled),
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                )

            disable_replication = solr.replication("disablereplication", True)
            current_app.logger.debug(disable_replication.json())

        # Delete index
        current_app.logger.debug("Deleting all documents in SOLR core...")
        solr.delete_all_docs()

        return jsonify({"message": "Pre-reindex steps completed successfully."}), HTTPStatus.OK
    except Exception as err:
        current_app.logger.exception("Pre-reindex failed.")
        return exception_response(err)


# -----------------------------
# Reindex Post
# -----------------------------
@bp.post("/post")
@cross_origin(origins="*")
@jwt.requires_roles([User.Role.system.value])
def reindex_post_endpoint():
    """Execute post-reindex operations on the follower."""
    try:
        if current_app.config.get("HAS_FOLLOWER", True):
            enable_replication = solr.replication("enablereplication", True)
            current_app.logger.debug(enable_replication.json())
            sleep(5)

            fetch_new_idx = solr.replication("fetchindex", False)
            current_app.logger.debug(fetch_new_idx.json())
            sleep(10)

            enable_polling = solr.replication("enablepoll", False)
            current_app.logger.debug(enable_polling.json())

        return jsonify({"message": "Post-reindex steps completed successfully."}), HTTPStatus.OK
    except Exception as err:
        current_app.logger.exception("Post-reindex failed.")
        return exception_response(err)


# -----------------------------
# Reindex Recovery
# -----------------------------
@bp.post("/recovery")
@cross_origin(origins="*")
@jwt.requires_roles([User.Role.system.value])
def reindex_recovery_endpoint():
    """Restore leader index and re-enable follower polling if needed."""
    try:
        restore = solr.replication("restore", True)
        current_app.logger.debug(restore.json())
        current_app.logger.debug("Awaiting restore completion...")

        for i in range(100):
            current_app.logger.debug(f"Checking restore status {i+1}/100...")
            status = solr.replication("restorestatus", True)
            current_app.logger.debug(status.json())
            status_json = status.json()
            restore_status = status_json.get("restorestatus", {}).get("status")
            if restore_status == "success":
                current_app.logger.debug("Restore complete.")
                enable_replication = solr.replication("enablereplication", True)
                current_app.logger.debug(enable_replication.json())
                sleep(5)

                enable_polling = solr.replication("enablepolling", False)
                current_app.logger.debug(enable_polling.json())
                return jsonify({"message": "Recovery completed successfully."}), HTTPStatus.OK
            if status_json.get("status") == "failed":
                break
            sleep(10 + (i*2))

        current_app.logger.error("Possible failure to restore leader index. Manual intervention required.")
        return jsonify({"message": "Recovery may have failed; check logs."}), HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as err:
        current_app.logger.exception("Recovery failed.")
        return exception_response(err)
