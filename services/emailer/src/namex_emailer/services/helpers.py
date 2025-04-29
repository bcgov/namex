from datetime import datetime

import pytz
import requests
from flask import current_app
from cachetools import cached, TTLCache
from urllib.parse import urlencode

@staticmethod
@cached(cache=TTLCache(maxsize=1, ttl=180)) 
def get_bearer_token():
    """Get a valid Bearer token for the service to use."""
    token_url = current_app.config.get('ACCOUNT_SVC_AUTH_URL')
    client_id = current_app.config.get('ACCOUNT_SVC_CLIENT_ID')
    client_secret = current_app.config.get('ACCOUNT_SVC_CLIENT_SECRET')

    # get service account token
    res = requests.post(url=token_url,
                        data='grant_type=client_credentials',
                        headers={'content-type': 'application/x-www-form-urlencoded'},
                        auth=(client_id, client_secret))

    try:
        return res.json().get('access_token')
    except Exception:
        return None

@staticmethod
def as_legislation_timezone(date_time: datetime) -> datetime:
    """Return a datetime adjusted to the legislation timezone."""
    return date_time.astimezone(pytz.timezone(current_app.config.get('LEGISLATIVE_TIMEZONE')))


@staticmethod
def format_as_report_string(date_time: datetime) -> str:
    """Return a datetime string in this format (eg: `August 5, 2021 at 11:00 am Pacific time`)."""
    # ensure is set to correct timezone
    date_time = as_legislation_timezone(date_time)
    hour = date_time.strftime('%I').lstrip('0')
    # %p provides locale value: AM, PM (en_US); am, pm (de_DE); So forcing it to be lower in any case
    am_pm = date_time.strftime('%p').lower()
    date_time_str = date_time.strftime(f'%B %-d, %Y at {hour}:%M {am_pm} Pacific time')
    return date_time_str


@staticmethod
def get_magic_link(nr_data):
    """Return a magic link."""
    BUSINESS_REGISTRY_URL = current_app.config.get("BUSINESS_REGISTRY_URL")
    magic_link_route = {
        'NEW': 'incorporateNow',
        'MVE': 'continueInNow',
        'AML': 'amalgamateNow'
    }
    emails, phones = get_contact_info(nr_data)
    route = magic_link_route.get(nr_data["request_action_cd"])
    params = {
        'nr': nr_data['nrNum'],
        'email': emails[0],
        'phone': phones[0]
    }
    encoded_params = urlencode(params)
    return f'{BUSINESS_REGISTRY_URL}{route}/?{encoded_params}'


@staticmethod
def get_contact_info(nr_data):
    applicants = nr_data.get('applicants', [])
    
    if isinstance(applicants, dict):  # Handle single applicant case
        applicants = [applicants]

    recipient_emails, recipient_phones = [], []
    for applicant in applicants:
        email = applicant.get('emailAddress')
        phone = applicant.get('phoneNumber')

        if email:  # Exclude empty values
            recipient_emails.append(email)
        if phone:  # Exclude empty values
            recipient_phones.append(phone)

    return recipient_emails, recipient_phones


def get_headers(token: str) -> dict:
    """Return the standard headers for requests."""
    return {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }


@staticmethod
def query_nr_number(identifier: str):
    """Return a JSON object with name request information."""
    namex_url = current_app.config.get('NAMEX_SVC_URL')

    token = get_bearer_token()

    nr_response = requests.get(namex_url + '/requests/' + identifier, headers=get_headers(token))

    return nr_response


@staticmethod
def query_notification_event(event_id: str):
    """Return a JSON object with name request information."""
    namex_url = current_app.config.get('NAMEX_SVC_URL')

    token = get_bearer_token()

    nr_response = requests.get(namex_url + '/events/event/' + event_id, headers=get_headers(token))

    return nr_response

@staticmethod
def record_notification_event(nr_num: str, email: str):
    payload = {
        "action": "notification",
        "eventJson": email
    }

    namex_url = current_app.config.get('NAMEX_SVC_URL')
    token = get_bearer_token()

    try:
        nr_response = requests.post(
            namex_url + '/events/' + nr_num,
            json=payload,
            headers=get_headers(token)
        )
        nr_response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return nr_response
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Failed to record notification event for NR {nr_num}: {e}")
        return None