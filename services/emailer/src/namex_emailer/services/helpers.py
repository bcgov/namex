from datetime import datetime

import pytz
import requests
from flask import current_app
from cachetools import cached, TTLCache
from urllib.parse import urlencode
from namex.constants import RequestAction

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
def query_nr_number(identifier: str):
    """Return a JSON object with name request information."""
    namex_url = current_app.config.get('NAMEX_SVC_URL')

    token = get_bearer_token()

    nr_response = requests.get(namex_url + '/requests/' + identifier, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    })

    return nr_response


@staticmethod
def get_magic_link(nr_number, email, phone):
    """Return a magic link."""
    BUSINESS_REGISTRY_URL = current_app.config.get("BUSINESS_REGISTRY_URL")
    params = {
        'nr': nr_number,
        'email': email,
        'phone': phone
    }
    encoded_params = urlencode(params)
    return f'{BUSINESS_REGISTRY_URL}incorporateNow/?{encoded_params}'
