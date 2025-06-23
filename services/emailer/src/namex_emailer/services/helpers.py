from copy import deepcopy
from datetime import datetime
from urllib.parse import urlencode

import pytz
import requests
from cachetools import TTLCache, cached
from flask import current_app, request
from gcp_queue.logging import structured_log

from namex_emailer.constants.notification_options import DECISION_OPTIONS, Option


@staticmethod
@cached(cache=TTLCache(maxsize=1, ttl=180))
def get_bearer_token():
    """Get a valid Bearer token for the service to use."""
    token_url = current_app.config.get("ACCOUNT_SVC_AUTH_URL")
    client_id = current_app.config.get("ACCOUNT_SVC_CLIENT_ID")
    client_secret = current_app.config.get("ACCOUNT_SVC_CLIENT_SECRET")

    # get service account token
    res = requests.post(
        url=token_url,
        data="grant_type=client_credentials",
        headers={"content-type": "application/x-www-form-urlencoded"},
        auth=(client_id, client_secret),
    )

    try:
        return res.json().get("access_token")
    except Exception:
        return None


@staticmethod
def as_legislation_timezone(date_time: datetime) -> datetime:
    """Return a datetime adjusted to the legislation timezone."""
    return date_time.astimezone(pytz.timezone(current_app.config.get("LEGISLATIVE_TIMEZONE")))


@staticmethod
def format_as_report_string(date_time: datetime) -> str:
    """Return a datetime string in this format (eg: `August 5, 2021 at 11:00 am Pacific time`)."""
    # ensure is set to correct timezone
    date_time = as_legislation_timezone(date_time)
    hour = date_time.strftime("%I").lstrip("0")
    # %p provides locale value: AM, PM (en_US); am, pm (de_DE); So forcing it to be lower in any case
    am_pm = date_time.strftime("%p").lower()
    date_time_str = date_time.strftime(f"%B %-d, %Y at {hour}:%M {am_pm} Pacific time")
    return date_time_str


@staticmethod
def get_magic_link(nr_data):
    """Return a magic link."""
    BUSINESS_REGISTRY_URL = current_app.config.get("BUSINESS_REGISTRY_URL")
    magic_link_route = {"NEW": "incorporateNow", "MVE": "continueInNow", "AML": "amalgamateNow"}
    emails, phones = get_contact_info(nr_data)
    route = magic_link_route.get(nr_data["request_action_cd"])
    params = {"nr": nr_data["nrNum"], "email": emails[0], "phone": phones[0]}
    encoded_params = urlencode(params)
    return f"{BUSINESS_REGISTRY_URL}{route}/?{encoded_params}"


@staticmethod
def get_contact_info(nr_data):
    applicants = nr_data.get("applicants", [])

    if isinstance(applicants, dict):  # Handle single applicant case
        applicants = [applicants]

    recipient_emails, recipient_phones = [], []
    for applicant in applicants:
        email = applicant.get("emailAddress")
        phone = applicant.get("phoneNumber")

        if email:  # Exclude empty values
            recipient_emails.append(email)
        if phone:  # Exclude empty values
            recipient_phones.append(phone)

    return recipient_emails, recipient_phones


def get_headers(token: str) -> dict:
    """Return the standard headers for requests."""
    return {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}


@staticmethod
def query_nr_number(identifier: str):
    """Return a JSON object with name request information."""
    namex_url = current_app.config.get("NAMEX_SVC_URL")

    token = get_bearer_token()

    nr_response = requests.get(namex_url + "/requests/" + identifier, headers=get_headers(token))

    return nr_response


@staticmethod
def query_notification_event(event_id: str):
    """Return a JSON object with name request information."""
    namex_url = current_app.config.get("NAMEX_SVC_URL")

    token = get_bearer_token()

    nr_response = requests.get(f"{namex_url}/events/event/{event_id}", headers=get_headers(token))

    return nr_response


@staticmethod
def send_email(email: dict, token: str):
    """Send the email"""
    structured_log(request, "INFO", f"Send Email: {email}")
    return requests.post(
        f"{current_app.config.get('NOTIFY_API_URL', '')}",
        json=email,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )


@staticmethod
def write_to_events(ce, email):
    """
    Log the event as a system-generated notification in the events table.
    """
    # Extract and validate data
    nr_num, option = _extract_event_data(ce)
    if not nr_num or not option:
        return

    # Prepare event JSON
    event_json = _prepare_event_json(nr_num, option, email)

    # Record the notification event
    return _record_event(nr_num, event_json)


@staticmethod
def update_resend_timestamp(event_id: str):
    """
    Update the resend timestamp for the event.
    """
    namex_url = current_app.config.get("NAMEX_SVC_URL")
    token = get_bearer_token()

    try:
        response = requests.patch(f"{namex_url}/events/event/{event_id}", headers=get_headers(token))
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        structured_log(request, "ERROR", f"Failed to update resend timestamp for event {event_id}: {e}")
        return False


@staticmethod
def _extract_event_data(ce):
    """
    Extract and validate the NR number and option from the cloud event.
    """
    nr_num = ce.data.get("request", {}).get("nrNum", None)
    option = ce.data.get("request", {}).get("option", None)

    if not nr_num or option not in {opt.value for opt in Option}:
        structured_log(request, "ERROR", f"Invalid NR number or option: nrNum={nr_num}, option={option}")
        return None, None

    return nr_num, option


@staticmethod
def _prepare_event_json(nr_num, option, email):
    """
    Prepare the event JSON object, including processing attachments if needed.
    """
    event_json = {"option": option}
    email_for_event = deepcopy(email) if email.get("content", {}).get("attachments") else email

    # Process attachments if the option is in DECISION
    if option and Option(option) in DECISION_OPTIONS:
        for attachment in email_for_event["content"].get("attachments", []):
            attachment["fileBytes"] = "<placeholder-for-pdf-report-bytes>"
        try:
            nr_model = query_nr_number(nr_num)
            if nr_model.status_code != 200:
                structured_log(request, "ERROR", f"Failed to query NR number {nr_num}: {nr_model.status_code}")
                return None
            nr_model = nr_model.json()
            event_json["nr_model"] = nr_model
        except Exception as e:
            structured_log(request, "ERROR", f"Failed to query NR number {nr_num}: {e}")
            return None

    event_json["email"] = email_for_event
    return event_json


@staticmethod
def _record_event(nr_num, event_json):
    """
    Record the notification event in the events table.
    """
    payload = {"action": "notification", "eventJson": event_json}
    namex_url = current_app.config.get("NAMEX_SVC_URL")
    token = get_bearer_token()

    try:
        nr_response = requests.post(f"{namex_url}/events/{nr_num}", json=payload, headers=get_headers(token))
        nr_response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        structured_log(request, "DEBUG", f"Successfully recorded notification event for NR {nr_num}")
        return True
    except requests.exceptions.RequestException as e:
        structured_log(request, "ERROR", f"Failed to record notification event for NR {nr_num}: {e}")
        return False
