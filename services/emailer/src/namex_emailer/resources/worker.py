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
"""This Module processes simple cloud event messages for possible filing payments"""

from http import HTTPStatus

from flask import Blueprint, request
from sbc_common_components.utils.enums import QueueMessageTypes
from simple_cloudevent import SimpleCloudEvent
from structured_logging import StructuredLogging

import namex_emailer.services.helpers
from namex_emailer.constants.notification_options import DECISION_OPTIONS, NOTIFICATION_OPTIONS, Option
from namex_emailer.email_processors import name_request, nr_notification, nr_result
from namex_emailer.email_processors.resend import process_resend_email
from namex_emailer.services import ce_cache, queue
from namex_emailer.services.email_scheduler import (
    cancel_any_in_flight_email_tasks,
    is_reset,
    is_schedulable,
    schedule_email,
)

bp = Blueprint("worker", __name__)

logger = StructuredLogging.get_logger()


@bp.route("/", methods=("POST",))
def worker():
    """Process the incoming cloud event"""
    logger.info(f"Incoming raw msg: {request.data}")

    if not (ce := queue.get_simple_cloud_event(request, wrapped=True)):
        #
        # Decision here is to return a 200,
        # so the event is removed from the Queue
        return {}, HTTPStatus.OK

    item = ce_cache.get(ce.id, None)

    if item is not None:
        logger.info(f"skipping duplicate ce: {str(ce)}")
        return {}, HTTPStatus.OK

    # Check if it's a resend
    resend_event_id = ce.data.get("request", {}).get("resendEventId")
    if resend_event_id:
        return process_resend_email(resend_event_id)

    logger.info(f"received ce: {str(ce)}")

    # Check if it's a reset
    if is_reset(ce):
        try:
            cancel_any_in_flight_email_tasks(ce)
            ce_cache[ce.id] = ce
            return {}, HTTPStatus.OK
        except Exception as err:
            logger.warning(f"Error cancelling cloud task from reset: {err}")

    # If approved, conditional, or rejected - schedule a cloud task to send the email in 5 minutes
    if is_schedulable(ce):
        try:
            schedule_email(ce)
            ce_cache[ce.id] = ce
            return {}, HTTPStatus.OK
        except Exception as err:
            logger.warning(f"Scheduling failed, falling back to immediate send: {err}")

    token = namex_emailer.services.helpers.get_bearer_token()
    if not (email := process_email(ce)):
        # no email to send, take off queue
        logger.info(f"No email to send for: {ce}")
        return {}, HTTPStatus.OK

    if not email or "recipients" not in email or "content" not in email or "body" not in email["content"]:
        # email object(s) is empty, take off queue
        logger.info("Send email: email object(s) is empty")
        return {}, HTTPStatus.OK

    if not email["recipients"] or not email["content"] or not email["content"]["body"]:
        # email object(s) is missing, take off queue
        logger.info("Send email: email object(s) is missing")
        return {}, HTTPStatus.OK

    resp = namex_emailer.services.helpers.send_email(email, token)

    if resp.status_code != HTTPStatus.OK:
        # log the error and put the email msg back on the queue
        logger.error(
            f"Queue Error - email failed to send: {str(ce)}"
            "\n\nThis message has been put back on the queue for reprocessing.",
        )
        return {}, HTTPStatus.NOT_FOUND
    ce_cache[ce.id] = ce

    namex_emailer.services.helpers.write_to_events(ce, email)

    logger.info(f"completed ce: {str(ce)}")

    return {}, HTTPStatus.OK


def process_email(email_msg: SimpleCloudEvent):
    """Process the email contained in the submission."""

    logger.debug(f"Attempting to process email: {email_msg}")
    etype = email_msg.type
    if etype and etype == QueueMessageTypes.NAMES_MESSAGE_TYPE.value:
        option = email_msg.data.get("request", {}).get("option", None)
        if option and Option(option) in NOTIFICATION_OPTIONS:
            email = nr_notification.process(email_msg, option)
        elif option and Option(option) in DECISION_OPTIONS:
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
