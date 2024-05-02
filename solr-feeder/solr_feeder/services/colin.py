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


def _get_colin_api_resp(path: str, token: str, accepted_codes: list[HTTPStatus]) -> tuple[dict, dict]:
    """Return colin-api response json for the given path."""
    try:
        headers = {'Authorization': 'Bearer ' + token}

        resp = requests.get(f'{current_app.config["COLIN_API_URL"]}/{path}',
                            headers=headers,
                            timeout=current_app.config['COLIN_API_TIMEOUT'])

        if resp.status_code not in accepted_codes:
            logging.debug('COLIN service unexpected response code %s %s %s', resp.status_code, path, resp.json())
            return None, {'message': resp.json(), 'status_code': resp.status_code}

        return resp.json(), None

    except (exceptions.ConnectionError, exceptions.Timeout) as err:
        logging.debug('COLIN connection failure %s', err)
        return None, {'message': 'COLIN connection failure.', 'status_code': HTTPStatus.GATEWAY_TIMEOUT}
    except Exception as err:
        logging.debug('COLIN service error %s', err.with_traceback(None))
        return None, {'message': 'COLIN service error.', 'status_code': HTTPStatus.INTERNAL_SERVER_ERROR}


def get_business_info(legal_type: str, identifier: str, token: str) -> tuple[dict, dict]:
    """Return the business info for the identifier and legal type."""
    try:
        business_json, error = _get_colin_api_resp(f'businesses/{legal_type}/{identifier}', token, [HTTPStatus.OK])
        if error:
            return None, error

        bus_addresses = None
        legal_types_with_ro = ['LP', 'BC', 'C', 'CC', 'CCC', 'CUL',
                               'QA', 'QB', 'QC', 'QD', 'QE', 'ULC',
                               'UQA', 'UQB', 'UQC', 'UQD', 'UQE']
        if legal_type in legal_types_with_ro:
            bus_addresses, error = _get_colin_api_resp(f'businesses/{legal_type}/{identifier}/office',
                                                       token,
                                                       [HTTPStatus.OK])
            if error:
                # log error for ops and continue (address info should not block the update)
                logging.error('Error getting address data while updating %s.', identifier)

        business = {
            'email': business_json['business']['email'],
            'goodStanding': business_json['business'].get('goodStanding', None),
            # add BC prefix to payload if its a BC limited company
            'identifier': f'BC{identifier}' if legal_type == 'BC' else identifier,
            'legalName': business_json['business']['legalName'],
            'legalType': legal_type,
            'state': 'HISTORICAL' if business_json['business']['corpStateClass'] == 'HIS' else 'ACTIVE',
            'taxId': business_json['business']['businessNumber']
        }
        if bus_addresses and (address := bus_addresses.get('registeredOffice', {}).get('deliveryAddress')):
            business['addresses'] = [{**address, 'addressType': 'DELIVERY'}]

        return {'business': business}, None

    except (exceptions.ConnectionError, exceptions.Timeout) as err:
        logging.error('COLIN connection failure %s', err)
        return None, {'message': 'COLIN connection failure.', 'status_code': HTTPStatus.GATEWAY_TIMEOUT}
    except Exception as err:
        logging.error('COLIN service error %s', err.with_traceback(None))
        return None, {'message': 'COLIN service error.', 'status_code': HTTPStatus.INTERNAL_SERVER_ERROR}


def get_owners(legal_type: str, identifier: str, token: str) -> tuple[list[dict], dict]:
    """Return the firm owners of the business."""
    owners = []
    if legal_type not in FIRM_LEGAL_TYPES:
        return [], None

    parties_path = f'businesses/{legal_type}/{identifier}/parties'
    # get owners
    fio_json, fio_error = _get_colin_api_resp(f'{parties_path}?partyType=Firm Individual Owner',
                                              token,
                                              [HTTPStatus.OK, HTTPStatus.NOT_FOUND])
    fbo_json, fbo_error = _get_colin_api_resp(f'{parties_path}?partyType=Firm Business Owner',
                                              token,
                                              [HTTPStatus.OK, HTTPStatus.NOT_FOUND])
    if fio_error or fbo_error:
        return None, fio_error if fio_error else fbo_error

    colin_owners = fio_json.get('directors', []) + fbo_json.get('directors', [])

    for owner in colin_owners:
        parsed_owner = _parse_party(owner, legal_type)
        # only need to include officer and roles for this flow
        owners.append({'officer': parsed_owner['officer'], 'roles': parsed_owner['roles']})

    return owners, None


def get_parties(legal_type: str, identifier: str, token: str) -> tuple[list[dict], dict]:
    """Return the parties of the business."""
    parties_path = f'businesses/{legal_type}/{identifier}/parties/all'
    all_parties_json, error = _get_colin_api_resp(parties_path, token, [HTTPStatus.OK, HTTPStatus.NOT_FOUND])
    if error:
        return None, error

    parties = []
    for party in all_parties_json.get('parties', []):
        # David R said to ignore these (they are also ignored in the importer job):
        #   - Data for these is garbage and won't be brought over when they are modernized.
        #   - party_typ_cds: ('PAS','PDI','PSA','RAD','RAF','RAO','RAS','TAP','TAA','TSP')
        ignored_types = ['Partner ATT SK', 'Partner DIRECTOR', 'Partner Sign Auth',
                         'Partner Reinstatement Applicant - Director of foreign entity',
                         'Partner Reinstatement Applicant - Foreign Entity Reinstated',
                         'Partner Reinstatement Applicant - Office of foreign entity',
                         'Partner Reinstatement Applicant - Shareholder of foreign entity',
                         'TILMA Alternate Attorney', 'TILMA Primary Attorney', 'TILMA Submitting Party']
        roles = []
        for role in party['roles']:
            # only add valid roles
            if role['roleType'] not in ignored_types:
                roles.append(role)
        if roles:
            # has valid roles so add party to update
            party['roles'] = roles
            if parsed_party := _parse_party(party, legal_type):
                # check to make sure it contains a person name (otherwise we will ignore this record)
                # - NOTE: some records contain no organization name AND no party name
                has_person_name = parsed_party['officer'].get('firstName') \
                    or parsed_party['officer'].get('middleInitial') \
                    or parsed_party['officer'].get('lastName')
                if has_person_name:
                    parties.append(parsed_party)

    return parties, None
