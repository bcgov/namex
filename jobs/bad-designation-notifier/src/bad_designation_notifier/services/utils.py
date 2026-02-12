"""Utility functions for database queries, date handling, and API requests."""

from datetime import datetime, timedelta
from json import JSONDecodeError

import pytz
import requests
from cachetools import TTLCache, cached
from flask import current_app

# Column definitions: (Key, Header, Width)
# Column definitions: (Key, Header)
columns = [
    ("event_time", "EVENT TIME"),
    ("nr_num", "NR NUM"),
    ("name", "NAME"),
    ("entity_type_cd", "ENTITY_TYPE"),
    ("status", "STATUS"),
    ("consumed_date", "CONSUMED_DATE"),
    ("consumed_by", "CONSUMED BY"),
]

# Extract only the keys and headers
column_keys = [col[0] for col in columns]
column_headers = [col[1] for col in columns]


def get_yesterday_str():
    """Returns yesterday's date in 'yyyy-mm-dd' format based on Pacific Time."""
    pacific = pytz.timezone("America/Los_Angeles")

    # Get current UTC time and convert to Pacific Time
    now_utc = datetime.now(tz=pytz.utc)
    now_pacific = now_utc.astimezone(pacific)

    # Calculate yesterday's date
    start_of_yesterday = now_pacific - timedelta(days=1)

    # Format the date as yyyy-mm-dd
    return start_of_yesterday.strftime("%Y-%m-%d")


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
        timeout=30,
    )

    try:
        return res.json().get("access_token")
    except (ValueError, JSONDecodeError) as exc:
        current_app.logger.error(
            "Failed to decode bearer token response: %s", exc
        )
        return None
