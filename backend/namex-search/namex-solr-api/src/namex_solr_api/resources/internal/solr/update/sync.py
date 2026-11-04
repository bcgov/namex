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
"""API endpoint for syncing records in solr."""
from datetime import UTC, datetime, timedelta
from http import HTTPStatus

from flask import Blueprint, current_app, jsonify
from flask_cors import cross_origin

from namex_solr_api.exceptions import exception_response
from namex_solr_api.models import SolrDoc, SolrDocEvent
from namex_solr_api.services import solr
from namex_solr_api.services.namex_solr.doc_models import NameField, PCField, PossibleConflict

bp = Blueprint("SYNC", __name__, url_prefix="/sync")


@bp.get("")
@cross_origin(origins="*")
def sync_solr():
    """Sync docs in the DB that haven't been applied to SOLR yet."""
    try:
        pending_update_events: list[SolrDocEvent] = SolrDocEvent.get_events_by_status(
            statuses=[SolrDocEvent.Status.PENDING, SolrDocEvent.Status.ERROR],
            event_types=[SolrDocEvent.Type.UPDATE],
            limit=current_app.config["MAX_BATCH_UPDATE_NUM"])

        entity_ids_to_sync = [(SolrDoc.get_by_id(event.solr_doc_id)).entity_id for event in pending_update_events]
        current_app.logger.debug(f"Syncing: {entity_ids_to_sync}")
        if entity_ids_to_sync:
            _update_solr(entity_ids_to_sync, pending_update_events)
        return jsonify({"message": "Sync successful."}), HTTPStatus.OK

    except Exception as exception:
        return exception_response(exception)


@bp.get("/heartbeat")
@cross_origin(origins="*")
def sync_follower_heartbeat():  
    """Verify the solr follower instance is serving updated/synced records."""
    try:
        now = datetime.now(UTC)
        if errors := _validate_follower(now):
            current_app.logger.error(errors)
            return jsonify({"errors": errors}), HTTPStatus.INTERNAL_SERVER_ERROR

        # verify an update that happened in the last hour (if there is one)
        events_to_verify: list[SolrDocEvent] = SolrDocEvent.get_events_by_status(statuses=[SolrDocEvent.Status.COMPLETE],
                                                                                 event_types=[SolrDocEvent.Type.UPDATE],
                                                                                 start_date=now - timedelta(minutes=60),
                                                                                 limit=2)

        if len(events_to_verify) == 0 or events_to_verify[0].event_date + timedelta(minutes=5) > now:
            # either no updates to check or the event may not be reflected in the search yet
            current_app.logger.debug("No update events to verify in the last hour.")
        else:
            # there was an update in the last hour and it is at least 5 minutes old
            doc_obj_to_verify = SolrDoc.get_by_id(events_to_verify[0].solr_doc_id)

            most_recent_business_doc = SolrDoc.find_most_recent_by_entity_id(doc_obj_to_verify.entity_id)
            if most_recent_business_doc.id != doc_obj_to_verify.id:
                # there's been an update since so skip verification of this event
                current_app.logger.debug("Update event has been altered since. Skipping verification.")
            else:
                current_app.logger.debug(f"Verifying sync for: {doc_obj_to_verify.entity_id}...")
                expected_doc: dict = doc_obj_to_verify.doc
                response = solr.query({"query": f"id:{expected_doc['id']}", "fields": "*, [child]"})
                actual_doc: dict = response["response"]["docs"][0] if response["response"]["docs"] else {}

                if not _is_synced(actual_doc, expected_doc):
                    # data returned from the follower does match the update or is not there
                    current_app.logger.debug(f"Business expected: {expected_doc}")
                    current_app.logger.debug(f"Business served: {actual_doc}")
                    message = f"Follower failed to update entity: {doc_obj_to_verify.entity_id}."
                    current_app.logger.error(message)
                    return jsonify({"message": message}), HTTPStatus.INTERNAL_SERVER_ERROR

                current_app.logger.debug(f"Sync verified for: {doc_obj_to_verify.entity_id}")

        return jsonify({"message": "Follower synchronization is healthy."}), HTTPStatus.OK

    except Exception as exception:
        return exception_response(exception)


def _update_solr(entity_ids: list[str], doc_events: list[SolrDocEvent]):
    """Update the docs for the entity_ids in the solr instance."""
    possible_conflicts: list[PossibleConflict] = []
    for entity_id in entity_ids:
        doc_update = SolrDoc.find_most_recent_by_entity_id(entity_id)
        possible_conflicts.append(PossibleConflict(**doc_update.doc))
    try:
        # update people
        solr.create_or_replace_docs(possible_conflicts, additive=False)
        SolrDocEvent.update_events_status(SolrDocEvent.Status.COMPLETE, doc_events)

    except Exception as err:
        # log / update event / pass err
        current_app.logger.debug("Failed to UPDATE solr for %s", entity_ids)
        SolrDocEvent.update_events_status(SolrDocEvent.Status.ERROR, doc_events)
        raise err


def _validate_follower(now: datetime):
    """Return validation errors to do with the follower Solr instance."""
    errors = []
    if solr.follower_url != solr.leader_url:
        # verify the follower core details
        details: dict = (solr.replication("details", False)).json()["details"]
        # NOTE: replace tzinfo needed because strptime %Z is not working as documented
        #   - issue: accepts the tz in the string but doesn't add it to the dateime obj
        last_replication = (datetime.strptime(details["follower"]["indexReplicatedAt"],
                                                "%a %b %d %H:%M:%S %Z %Y")).replace(tzinfo=UTC)
        current_app.logger.debug(f"Last replication was at {last_replication.isoformat()}")

        # verify polling is active
        if details["follower"]["isPollingDisabled"] == "true":
            errors.append("Follower polling disabled when it should be enabled.")

        # verify last_replication datetime is within a reasonable timeframe
        if last_replication + timedelta(hours=current_app.config.get("LAST_REPLICATION_THRESHOLD")) < now:
            # its been too long since a replication. Log / return error
            errors.append("Follower last replication datetime is longer than expected.")

    return errors


def _is_synced(actual_doc: dict, expected_doc: dict):
    """Return if True if the actual_doc and expected_doc are synced."""
    def _compare_data(actual: dict, expected: dict, fields: dict[NameField | PCField, any]):
        """Return if True if the actual and expected are the same for the given fields."""
        for field in fields:
            if actual.get(field.value) != expected.get(field.value):
                current_app.logger.debug(f"{field} mismatch")
                return False
        return True

    pc_fields = [
        PCField.CORP_NUM, PCField.TYPE, PCField.STATE, PCField.JURISDICTION, PCField.START_DATE
    ]
    name_fields = [NameField.NAME, NameField.SUBMIT_COUNT, NameField.NAME_STATE]
    return (_compare_data(actual_doc, expected_doc, pc_fields) and
            _compare_data(actual_doc['names'][0], expected_doc['names'][0], name_fields))