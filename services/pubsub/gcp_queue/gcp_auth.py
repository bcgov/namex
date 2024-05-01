import functools
from http import HTTPStatus

import google.oauth2.id_token as id_token
from cachecontrol import CacheControl
from flask import abort, current_app, request
from google.auth.transport.requests import Request
from requests.sessions import Session

from .logging import structured_log


def verify_jwt(session):
    """Verify token is valid."""
    msg = ''
    try:
        if current_app.config.get("DEBUG_REQUEST"):
            structured_log(request, "INFO", f"Headers: {request.headers}")
        # Get the Cloud Pub/Sub-generated JWT in the "Authorization" header.
        claim = id_token.verify_oauth2_token(
            request.headers.get("Authorization").split()[1],
            Request(session=session),
            audience=current_app.config.get("SUB_AUDIENCE")
        )
        if current_app.config.get("DEBUG_REQUEST"):
            structured_log(request, "INFO", f"claim: {claim}")
        sa_email = current_app.config.get("SUB_SERVICE_ACCOUNT")
        if not claim['email_verified'] or claim['email'] != sa_email:
            msg = f"Invalid service account or email not verified for email: {claim['email']}\n"

    except Exception as e:  # TODO fix
        msg = f"Invalid token: {e}\n"
    finally:
        return msg


def ensure_authorized_queue_user(f):
    """Ensures the user is authorized to use the queue."""
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        # Use CacheControl to avoid re-fetching certificates for every request.
        if message := verify_jwt(CacheControl(Session())):
            print(message)
            abort(HTTPStatus.UNAUTHORIZED)
        return f(*args, **kwargs)
    return decorated_function