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
from typing import List, Tuple

import requests
from requests import exceptions
from flask import current_app


FIRM_LEGAL_TYPES = ['SP', 'GP', 'LP', 'XP', 'LL', 'XL', 'MF']


def get_business_info(legal_type: str, identifier: str) -> Tuple[dict, dict]:
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
            'state': 'HISTRICAL' if res_json['business']['corpState'] == 'HIS' else 'ACTIVE',
            'taxId': res_json['business']['businessNumber']
        }

        return {'business': business}, None

    except (exceptions.ConnectionError, exceptions.Timeout) as err:
        logging.error('COLIN connection failure %s', err)
        return None, {'message': 'COLIN connection failure.', 'status_code': HTTPStatus.GATEWAY_TIMEOUT}
    except Exception as err:  # noqa: B902
        logging.error('COLIN service error %s', err.with_traceback(None))
        return None, {'message': 'COLIN service error.', 'status_code': HTTPStatus.INTERNAL_SERVER_ERROR}


def get_owners(legal_type: str, identifier: str) -> Tuple[List[dict], dict]:
    """Return the owners of the business."""
    try:
        if legal_type not in FIRM_LEGAL_TYPES:
            return {'parties': []}, None
        parties_url = f'{current_app.config["COLIN_API_URL"]}/businesses/{legal_type}/{identifier}/parties'
        fio_res = requests.get(f'{parties_url}?partyType=Firm Individual Owner', timeout=current_app.config['COLIN_API_TIMEOUT'])
        fbo_res = requests.get(f'{parties_url}?partyType=Firm Business Owner', timeout=current_app.config['COLIN_API_TIMEOUT'])
        if fio_res.status_code not in [HTTPStatus.OK, HTTPStatus.NOT_FOUND] or fbo_res.status_code not in [HTTPStatus.OK, HTTPStatus.NOT_FOUND]:
            return None, {'message': res.json(), 'status_code': res.status_code}
        
        fio_json = fio_res.json()
        fbo_json = fbo_res.json()
        colin_owners = fio_json.get('directors', []) + fbo_json.get('directors', [])
        
        owners = []
        for owner in colin_owners:
            officer = {}
            if owner['officer'].get('orgName'):
                officer['organizationName'] = owner['officer']['orgName']
                officer['partyType'] = 'organization'
            else:
                officer['firstName'] = owner['officer']['firstName']
                officer['middleInitial'] = owner['officer'].get('middleInitial')
                officer['lastName'] = owner['officer']['lastName']
                officer['partyType'] = 'person'
            roles = [{'roleType': 'proprietor' if legal_type == 'SP' else 'partner'}]
            
            owners.append({'officer': officer, 'roles': roles})

        return {'parties': owners}, None

    except (exceptions.ConnectionError, exceptions.Timeout) as err:
        logging.error('COLIN connection failure %s', err)
        return None, {'message': 'COLIN connection failure.', 'status_code': HTTPStatus.GATEWAY_TIMEOUT}
    except Exception as err:  # noqa: B902
        logging.error('COLIN service error %s', err.with_traceback(None))
        return None, {'message': 'COLIN service error.', 'status_code': HTTPStatus.INTERNAL_SERVER_ERROR}
