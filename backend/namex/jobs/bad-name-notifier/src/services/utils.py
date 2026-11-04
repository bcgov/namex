"""
Utility functions for date calculations and authentication
used by the Bad Name Notifier service.
"""

from datetime import datetime, timedelta

import pytz
import requests
from cachetools import TTLCache, cached
from flask import current_app


def _now_in_vancouver():
    zone = pytz.timezone("America/Vancouver")
    return datetime.now(tz=pytz.utc).astimezone(zone)


def get_yesterday_str():
    """Return yesterday in America/Vancouver as yyyy-mm-dd."""
    yesterday = _now_in_vancouver() - timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")


def get_yesterday_utc_range():
    """Return the start of yesterday and today in Vancouver, as UTC strings."""
    local = _now_in_vancouver()
    zone = pytz.timezone("America/Vancouver")
    midnight = local.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
    start_of_today = zone.localize(midnight)
    start_of_yesterday = zone.normalize(start_of_today - timedelta(days=1))
    start_of_today_utc = start_of_today.astimezone(pytz.utc).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    start_of_yesterday_utc = start_of_yesterday.astimezone(pytz.utc).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    return start_of_yesterday_utc, start_of_today_utc


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
        timeout=10,  # ✅ prevents hanging
    )

    try:
        return res.json().get("access_token")
    except Exception:  # pylint: disable=broad-exception-caught
        current_app.logger.error("Error getting Bearer Token.")
        return None
