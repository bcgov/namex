from http import HTTPStatus

from flask import Blueprint, request
from gcp_queue.logging import structured_log
from simple_cloudevent import from_queue_message

from namex_emailer.resources.worker import process_email
from namex_emailer.services import ce_cache
from namex_emailer.services.helpers import get_bearer_token, send_email, write_to_events

bp = Blueprint("tasks", __name__)


@bp.route("/handle-send", methods=["POST"])
def deliver_scheduled_email():
    """Callback for Cloud Tasks: idempotently send the email and trigger retries on error."""
    ce = from_queue_message(request.data)
    nr_num = ce.data.get("request", {}).get("nrNum", "unknown-NR")
    structured_log(request, "INFO", f"Received scheduled email send for '{nr_num}' from Cloud Tasks")

    if ce_cache.get(ce.id):
        structured_log(request, "INFO", f"Skipping duplicate scheduled send for '{nr_num}'")
        return {}, HTTPStatus.OK

    email = process_email(ce)
    token = get_bearer_token()

    resp = send_email(email, token)
    if resp.status_code != HTTPStatus.OK:
        structured_log(request, "ERROR", f"Scheduled send failed for '{nr_num}'. Trying again...")
        # Non-2xx → Cloud Tasks will retry (3x total before giving up)
        return {}, HTTPStatus.INTERNAL_SERVER_ERROR

    # Success
    ce_cache[ce.id] = ce  # mark as done so any further retries get skipped
    write_to_events(ce, email)
    structured_log(request, "INFO", f"Scheduled email send completed for '{nr_num}'")
    return {}, HTTPStatus.OK
