# Copyright © 2022 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Manages colin-api interactions."""
import logging
from http import HTTPStatus

import requests
from requests import exceptions
from flask import current_app


FIRM_LEGAL_TYPES = ['SP', 'GP', 'LP', 'XP', 'LL', 'XL', 'MF']


def _parse_party(party: dict, legal_type: str):
    """Return the party information with parsed data expected by the apis."""
    officer = {'id': party.get('id')}
    if party['officer'].get('orgName'):
        officer['organizationName'] = party['officer']['orgName']
        officer['partyType'] = 'organization'
    else:
        officer['firstName'] = party['officer']['firstName']
        officer['middleInitial'] = party['officer'].get('middleInitial')
        officer['lastName'] = party['officer']['lastName']
        officer['partyType'] = 'person'

    party['officer'] = officer
    party['source'] = 'COLIN'

    if legal_type in FIRM_LEGAL_TYPES:
        for role in party['roles']:
            if role['roleType'] in ['Firm Business Owner', 'Firm Individual Owner']:
                # convert role type to modernized description
                role['roleType'] = 'proprietor' if legal_type == 'SP' else 'partner'

    # if no address then set it to empty delivery
    if not party.get('deliveryAddress'):
        party['deliveryAddress'] = {'addressType': 'DELIVERY'}

    return party


def get_business_info(legal_type: str, identifier: str) -> tuple[dict, dict]:
    """Return the basic business info of the business."""
    try:
        res = requests.get(f'{current_app.config["COLIN_API_URL"]}/businesses/{legal_type}/{identifier}',
                           timeout=current_app.config['COLIN_API_TIMEOUT'])
        if res.status_code != HTTPStatus.OK:
            return None, {'message': res.json(), 'status_code': res.status_code}

        res_json = res.json()
        business = {
            # add BC prefix to payload if its a BC limited company
            'identifier': f'BC{identifier}' if legal_type == 'BC' else identifier,
            'legalName': res_json['business']['legalName'],
            'legalType': legal_type,
            'state': 'HISTORICAL' if res_json['business']['corpStateClass'] == 'HIS' else 'ACTIVE',
            'taxId': res_json['business']['businessNumber']
        }

        return {'business': business}, None

    except (exceptions.ConnectionError, exceptions.Timeout) as err:
        logging.error('COLIN connection failure %s', err)
        return None, {'message': 'COLIN connection failure.', 'status_code': HTTPStatus.GATEWAY_TIMEOUT}
    except Exception as err:
        logging.error('COLIN service error %s', err.with_traceback(None))
        return None, {'message': 'COLIN service error.', 'status_code': HTTPStatus.INTERNAL_SERVER_ERROR}


def get_owners(legal_type: str, identifier: str) -> tuple[list[dict], dict]:
    """Return the firm owners of the business."""
    try:
        owners = []
        if legal_type not in FIRM_LEGAL_TYPES:
            return [], None

        parties_url = f'{current_app.config["COLIN_API_URL"]}/businesses/{legal_type}/{identifier}/parties'
        # get owners
        fio_res = requests.get(f'{parties_url}?partyType=Firm Individual Owner',
                               timeout=current_app.config['COLIN_API_TIMEOUT'])
        fbo_res = requests.get(f'{parties_url}?partyType=Firm Business Owner',
                               timeout=current_app.config['COLIN_API_TIMEOUT'])
        if fio_res.status_code not in [HTTPStatus.OK, HTTPStatus.NOT_FOUND]:
            return None, {'message': fio_res.json(), 'status_code': fio_res.status_code}
        if fbo_res.status_code not in [HTTPStatus.OK, HTTPStatus.NOT_FOUND]:
            return None, {'message': fbo_res.json(), 'status_code': fbo_res.status_code}

        fio_json = fio_res.json()
        fbo_json = fbo_res.json()
        colin_owners = fio_json.get('directors', []) + fbo_json.get('directors', [])

        for owner in colin_owners:
            parsed_owner = _parse_party(owner, legal_type)
            # only need to include officer and roles for this flow
            owners.append({'officer': parsed_owner['officer'], 'roles': parsed_owner['roles']})

        return owners, None

    except (exceptions.ConnectionError, exceptions.Timeout) as err:
        logging.error('COLIN connection failure %s', err)
        return None, {'message': 'COLIN connection failure.', 'status_code': HTTPStatus.GATEWAY_TIMEOUT}
    except Exception as err:
        logging.error('COLIN service error %s', err.with_traceback(None))
        return None, {'message': 'COLIN service error.', 'status_code': HTTPStatus.INTERNAL_SERVER_ERROR}


def get_parties(legal_type: str, identifier: str) -> tuple[list[dict], dict]:
    """Return the parties of the business."""
    try:
        parties = []
        parties_url = f'{current_app.config["COLIN_API_URL"]}/businesses/{legal_type}/{identifier}/parties/all'

        # get all parties
        all_parties = requests.get(f'{parties_url}', timeout=current_app.config['COLIN_API_TIMEOUT'])
        if all_parties.status_code not in [HTTPStatus.OK, HTTPStatus.NOT_FOUND]:
            return None, {'message': all_parties.json(), 'status_code': all_parties.status_code}

        for party in (all_parties.json()).get('parties', []):
            parties.append(_parse_party(party, legal_type))

        return parties, None

    except (exceptions.ConnectionError, exceptions.Timeout) as err:
        logging.error('COLIN connection failure %s', err)
        return None, {'message': 'COLIN connection failure.', 'status_code': HTTPStatus.GATEWAY_TIMEOUT}
    except Exception as err:
        logging.error('COLIN service error %s', err.with_traceback(None))
        return None, {'message': 'COLIN service error.', 'status_code': HTTPStatus.INTERNAL_SERVER_ERROR}
