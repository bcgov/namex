from datetime import datetime, timedelta
import pytz
import requests
from cachetools import TTLCache, cached
from flask import current_app

def get_yesterday_str():
    pacific = pytz.timezone('America/Los_Angeles')

    # Calculate the start of today and yesterday in Pacific Time
    start_of_today_pacific = pacific.localize(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))
    start_of_yesterday_pacific = start_of_today_pacific - timedelta(days=1)

    # Format the date as yyyy-mm-dd
    return start_of_yesterday_pacific.strftime('%Y-%m-%d')

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