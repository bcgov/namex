import requests
import traceback
from flask import current_app
from cachetools import TTLCache, cached
from config import Config

@staticmethod
@cached(cache=TTLCache(maxsize=1, ttl=180))
def get_bearer_token():
    """Get a valid Bearer token for the service to use."""
    token_url = Config.ACCOUNT_SVC_AUTH_URL
    client_id = Config.ACCOUNT_SVC_CLIENT_ID
    client_secret = Config.ACCOUNT_SVC_CLIENT_SECRET

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
        current_app.logger.error("Error getting Bearer Token. Traceback:\n%s", traceback.format_exc())
        return None
