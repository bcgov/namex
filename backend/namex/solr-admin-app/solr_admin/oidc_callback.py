import requests
from flask import Blueprint, request, redirect, current_app, session
from urllib.parse import urlparse


bp = Blueprint("oidc_callback", __name__)


def is_safe_redirect_path(path: str) -> bool:
    """Validates that the redirect path is a relative URL preventing open redirect vulnerabilities"""
    parsed = urlparse(path)
    return not parsed.netloc and path.startswith("/")


@bp.route("/oidc_callback")
def callback():
    """Handles OIDC redirect from Keycloak by exchanging the auth code for an access token."""

    code = request.args["code"]  # auth code returned by Keycloak after the user logs in
    state = request.args.get("state", "/")  # original URL the user was trying to access before being redirected to login
    if not is_safe_redirect_path(state):
        state = "/"

    if session.get("access_token"):
        current_app.logger.debug("User already has access token, redirecting to default or validated state path.")
        return redirect(state)

    # Exchange the one-time auth code for an access token via Keycloak
    current_app.logger.debug("Exchanging auth code for access token...")
    try:
        response = requests.post(
            current_app.config["KEYCLOAK_AUTH_TOKEN_URL"],
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": current_app.config["OIDC_REDIRECT_URI"],
                "client_id": current_app.config["JWT_OIDC_AUDIENCE"],
                "client_secret": current_app.config["JWT_OIDC_CLIENT_SECRET"],
            },
            timeout=10
        )
    except requests.RequestException as e:
        current_app.logger.error("Token request failed: %s", str(e))
        return "Token request failed", 500

    # Check for unsuccessful response from token endpoint
    if response.status_code != 200:
        current_app.logger.error("Failed to get token: %s", response.text)
        return f"Failed to get token: {response.text}", 500

    # Parse the response and store the access token in the session
    token_response = response.json()
    session["access_token"] = token_response["access_token"]

    current_app.logger.debug("Access token successfully saved to session; redirecting to user-specified state URL.")
    return redirect(state)
