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
"""Manages search-api interactions."""
import logging
from http import HTTPStatus

import requests
from requests import exceptions
from flask import current_app

from solr_feeder.services import get_bearer_token, get_business_info, get_owners, get_parties


def _update_solr(url: str, payload: dict[str, str], timeout: int, token: str):
    """Update solr core."""
    try:
        headers = {'Authorization': 'Bearer ' + token}

        res = requests.put(url=url, headers=headers, json=payload, timeout=timeout)
        if res.status_code != HTTPStatus.OK:
            return {'message': res.json(), 'status_code': res.status_code}

        return None

    except (exceptions.ConnectionError, exceptions.Timeout) as err:
        logging.error('%s connection failure %s', url, err)
        return {'message': f'{url} connection failure.', 'status_code': HTTPStatus.GATEWAY_TIMEOUT}
    except Exception as err:
        logging.error('%s service error %s', url, err.with_traceback(None))
        return {'message': f'{url} service error.', 'status_code': HTTPStatus.INTERNAL_SERVER_ERROR}


def update_search_cores(identifier: str, legal_type: str):
    """Update registries search AND bor search."""
    logging.debug('Updating registries search and bor core records for %s...', identifier)
    # get token
    token, error = get_bearer_token()
    if error:
        return error

    # get business data
    business, error = get_business_info(legal_type, identifier)
    if error:
        logging.error('Error getting COLIN business data: %s', error)
        return {'message': error['message']}, HTTPStatus.INTERNAL_SERVER_ERROR

    error_messages = []
    # send data to bor search core via bor-api
    if bor_url := current_app.config['BOR_API_URL']:
        parties, error = get_parties(legal_type, identifier)
        if error:
            logging.error('Error getting COLIN party data: %s', error)
            return {'message': error['message']}, HTTPStatus.INTERNAL_SERVER_ERROR

        logging.debug('Updating BOR core...')
        error = _update_solr(url=f'{bor_url}/internal/solr/update',
                             payload={**business, 'parties': parties},
                             timeout=current_app.config['BOR_API_TIMEOUT'],
                             token=token)
        if error:
            if error['status_code'] == HTTPStatus.GATEWAY_TIMEOUT:
                logging.debug('BOR update error probably due to many parties associated ' +
                              'with the entity. Please verify the update for %s and ' +
                              'manually retry if necessary.', identifier)
                # error log for sentry message -- do not return an error msg as COLIN will keep retrying
                logging.error('Timeout error updating %s', identifier)
            else:
                logging.error('Error updating bor core: %s', error)
                error_messages.append(error['message'])
        else:
            logging.debug('BOR core updated.')

    # for business search only include owners
    owners, error = get_owners(legal_type, identifier)
    if error:
        logging.error('Error getting COLIN owner data: %s', error)
        return {'message': error['message']}, HTTPStatus.INTERNAL_SERVER_ERROR

    # send data to business search core via search-api
    error = _update_solr(url=f'{current_app.config["SEARCH_API_URL"]}/internal/solr/update',
                         payload={**business, 'parties': owners},
                         timeout=current_app.config['SEARCH_API_TIMEOUT'],
                         token=token)
    if error:
        logging.error('Error updating business search core: %s', error)
        error_messages.append(error['message'])
    else:
        logging.debug('BUSINESS SEARCH core updated.')

    if error_messages:
        return {'message': error_messages}, HTTPStatus.INTERNAL_SERVER_ERROR

    return None
