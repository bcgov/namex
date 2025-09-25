import requests
from flask import Request, current_app
from flask_jwt_oidc.jwt_manager import JwtManager
from jose import jwt

from namex.constants import PHONE_CLEANUP_PATTERN
from namex.models import Request as RequestDAO


def cors_preflight(methods):
    def wrapper(f):
        def options(self, *args, **kwargs):
            return (
                {'Allow': 'GET'},
                200,
                {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': methods,
                    'Access-Control-Allow-Headers': 'Authorization, Content-Type, BCREG-NR, BCREG-NRL, BCREG-User-Email, BCREG-User-Phone, App-Name, x-apikey',
                },
            )

        f.options = options
        return f

    return wrapper


def set_to_none(string, none_values):
    if string and str(string).lower() in none_values:
        return None
    return string


def full_access_to_name_request(request: Request) -> bool:
    """Returns that the request contains the headers required to fully access this NR."""
    nr = request.headers.get('BCREG-NR', '')
    nrl = request.headers.get('BCREG-NRL', '')
    email = request.headers.get('BCREG-User-Email', '')
    phone = request.headers.get('BCREG-User-Phone', '')

    current_app.logger.debug('NR: %s, NRL: %s, Email: %s, Phone: %s', nr, nrl, email, phone)

    nr = set_to_none(nr, ['none', 'null', 'nan'])
    nrl = set_to_none(nrl, ['none', 'null', 'nan'])
    email = set_to_none(email, ['none', 'null', 'nan'])
    phone = set_to_none(phone, ['none', 'null', 'nan'])

    if nr and not RequestDAO.validNRFormat(nr):
        nr = nr.replace(' ', '')
        nr = nr.replace('NR', '')
        nr = 'NR ' + nr

    if not (name_request := RequestDAO.find_by_nr(nr)):
        if not (name_request := RequestDAO.find_by_nr(nrl)):
            current_app.logger.debug('Failed to find NR - NR: %s, NRL: %s, Email: %s, Phone: %s', nr, nrl, email, phone)
            return False

    if not name_request.applicants:
        current_app.logger.debug(
            'Failed to find Applicant - NR: %s, NRL: %s, Email: %s, Phone: %s', nr, nrl, email, phone
        )
        return False
    applicant = name_request.applicants[0]

    if phone:
        phone = PHONE_CLEANUP_PATTERN.sub('', phone)
    if not (phone or email):
        current_app.logger.debug(
            'Failed no phone or email - NR: %s, NRL: %s, Email: %s, Phone: %s', nr, nrl, email, phone
        )
        return False
    if (
        phone
        and applicant.phoneNumber
        and phone != PHONE_CLEANUP_PATTERN.sub('', applicant.phoneNumber)
    ):
        current_app.logger.debug(
            'Failed wrong phone - NR: %s, NRL: %s, Email: %s, Phone: %s, Applicant phone %s',
            nr,
            nrl,
            email,
            phone,
            applicant.phoneNumber,
        )
        return False
    if email and applicant.emailAddress and applicant.emailAddress.lower() != email.lower():
        current_app.logger.debug(
            'Failed wrong email - NR: %s, NRL: %s, Email: %s, Phone: %s, Applicant email %s',
            nr,
            nrl,
            email,
            phone,
            applicant.emailAddress,
        )
        return False

    current_app.logger.debug('Success with NR: %s, NRL: %s, Email: %s, Phone: %s', nr, nrl, email, phone)
    return True


MSG_CLIENT_CREDENTIALS_REQ_FAILED = 'Client credentials request failed'


def get_client_credentials(auth_url, client_id, secret):
    auth = requests.post(
        auth_url,
        auth=(client_id, secret),
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data={'grant_type': 'client_credentials', 'client_id': client_id, 'client_secret': secret},
    )

    # Return the auth response if an error occurs
    if auth.status_code != 200:
        # TODO: This is mocked out
        # return True, 'asdf-asdf-asdf-adsf'
        return False, auth.json()

    token = dict(auth.json())['access_token']
    return True, token


def validate_roles(_jwt: JwtManager, authorization: str, required_roles):
    """Validate roles in authorization token."""
    parts = authorization.split()
    token = parts[1]
    _jwt._validate_token(token)
    unverified_claims = jwt.get_unverified_claims(token)
    roles_in_token = unverified_claims['realm_access']['roles']
    if all(elem in roles_in_token for elem in required_roles):
        return True
    return False
