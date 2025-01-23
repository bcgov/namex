from datetime import datetime, timedelta
import pytz
import requests
from cachetools import TTLCache, cached
from flask import current_app

def get_yesterday_str():
        # Calculate yesterday's date
    yesterday = datetime.now() - timedelta(days=1)
    
    # Format the date as yyyy-mm-dd
    return yesterday.strftime('%Y-%m-%d')

def get_yesterday_utc_range():
    pacific = pytz.timezone('America/Los_Angeles')

    # Calculate the start of today and yesterday in Pacific Time
    start_of_today_pacific = pacific.localize(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))
    start_of_yesterday_pacific = start_of_today_pacific - timedelta(days=1)

    # Convert to UTC
    start_of_today_utc = start_of_today_pacific.astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S')
    start_of_yesterday_utc = start_of_yesterday_pacific.astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S')

    return start_of_yesterday_utc, start_of_today_utc

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
