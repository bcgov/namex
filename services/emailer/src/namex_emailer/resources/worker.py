# Copyright © 2023 Province of British Columbia
#
# Licensed under the BSD 3 Clause License, (the 'License');
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
#
"""This Module processes simple cloud event messages for possible filing payments
"""
from http import HTTPStatus

import requests
from flask import Blueprint, current_app, request
from gcp_queue.logging import structured_log
from sbc_common_components.utils.enums import QueueMessageTypes
from simple_cloudevent import SimpleCloudEvent

import namex_emailer.services.helpers
from namex_emailer.email_processors import name_request, nr_notification, nr_result
from namex_emailer.services import ce_cache, queue

bp = Blueprint("worker", __name__)


@bp.route("/", methods=("POST",))
def worker():
    """Process the incoming cloud event
    """
    structured_log(request, "INFO", f"Incoming raw msg: {request.data}")

    if not (ce := queue.get_simple_cloud_event(request)):
        #
        # Decision here is to return a 200,
        # so the event is removed from the Queue
        return {}, HTTPStatus.OK

    # Check if it's a resend
    resend_event_id = ce.data.get("resend_event_id")
    if resend_event_id:
        # RESEND PATH
        return resend_email(resend_event_id)

    item =ce_cache.get(ce.id, None)

    if item is None:
        structured_log(request, "INFO", f"received ce: {str(ce)}")
        token = namex_emailer.services.helpers.get_bearer_token()
        if not (email := process_email(ce)):
            # no email to send, take off queue
            structured_log(request, "INFO", f"No email to send for: {ce}")
            return {}, HTTPStatus.OK

        if not email or "recipients" not in email or "content" not in email or "body" not in email["content"]:
            # email object(s) is empty, take off queue
            structured_log(request, "INFO", "Send email: email object(s) is empty")
            return {}, HTTPStatus.OK

        if not email["recipients"] or not email["content"] or not email["content"]["body"]:
            # email object(s) is missing, take off queue
            structured_log(request, "INFO", "Send email: email object(s) is missing")
            return {}, HTTPStatus.OK

        resp = send_email(email, token)

        if resp.status_code != HTTPStatus.OK:
            # log the error and put the email msg back on the queue
            structured_log(
                request,
                "ERROR",
                f"Queue Error - email failed to send: {str(ce)}"
                "\n\nThis message has been put back on the queue for reprocessing.",
            )
            return {}, HTTPStatus.NOT_FOUND
        ce_cache[ce.id] = ce

        write_to_events(ce, email)
        structured_log(request, "INFO", f"completed ce: {str(ce)}")
    else:
        structured_log(request, "INFO", f"skipping duplicate ce: {str(ce)}")

    return {}, HTTPStatus.OK


def write_to_events(ce: SimpleCloudEvent, email: dict):
    # write_to_events only when it is notification
    # Extract the Name Request number from the incoming cloud event
    nr_num = ce.data.get("request", {}).get("header", {}).get("nrNum", "")
    option = ce.data.get("request", {}).get("option", None)

    if (option in nr_notification.Option) and (nr_num is not None):
        # Log the event as a system-generated notification in the events table,
        namex_emailer.services.helpers.record_notification_event(nr_num, email)
        structured_log(request, "INFO", f"Event recorded: {str(email)}")

def resend_email(event_id: int):
    """
    Given an event id, retrieve the saved email and resend it.
    """
    # Query the event record
    event = namex_emailer.services.helpers.query_notification_event(event_id)

    if not event:
        structured_log(request, "ERROR", f"No event found for ID: {event_id}")
        return {"error": "Event not found"}, HTTPStatus.NOT_FOUND

    email = event.eventJson
    if not email:
        structured_log(request, "ERROR", f"No email content in event: {event_id}")
        return {"error": "No email content found"}, HTTPStatus.BAD_REQUEST

    token = namex_emailer.services.helpers.get_bearer_token()
    resp = send_email(email, token)

    if resp.status_code != HTTPStatus.OK:
        structured_log(
            request,
            "ERROR",
            f"Failed to resend email for event {event_id}: {resp.status_code} - {resp.text}",
        )
        return {"error": "Failed to resend email"}, resp.status_code

    structured_log(request, "INFO", f"Successfully resent email for event {event_id}")
    return {"success": True}, HTTPStatus.OK


def process_email(email_msg: SimpleCloudEvent):  # pylint: disable=too-many-branches, too-many-statements
    """Process the email contained in the submission."""

    structured_log(request, "DEBUG", f"Attempting to process email: {email_msg}")
    etype = email_msg.type
    if etype and etype == QueueMessageTypes.NAMES_MESSAGE_TYPE.value:
        option = email_msg.data.get("request", {}).get("option", None)
        if option and option in [
            nr_notification.Option.BEFORE_EXPIRY.value,
            nr_notification.Option.EXPIRED.value,
            nr_notification.Option.RENEWAL.value,
            nr_notification.Option.UPGRADE.value,
            nr_notification.Option.REFUND.value,
        ]:
            email = nr_notification.process(email_msg, option)
        elif option and option in [
            nr_notification.Option.APPROVED.value,
            nr_notification.Option.REJECTED.value,
            nr_notification.Option.CONDITIONAL.value,
        ]:
            email = nr_result.email_report(email_msg)
        elif option and option in [
            nr_notification.Option.CONSENT_RECEIVED.value,
        ]:
            email = nr_result.email_consent_letter(email_msg)
        else:
            email = name_request.process(email_msg)
    else:
        return None
    return email


def send_email(email: dict, token: str):
    """Send the email"""
    structured_log(request, "INFO", f"Send Email: {email}")
    return requests.post(
        f'{current_app.config.get("NOTIFY_API_URL", "")}',
        json=email,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )
