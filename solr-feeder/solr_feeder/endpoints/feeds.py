import logging
from http import HTTPStatus

import flask
from flask import Blueprint, current_app

from solr_feeder import solr
from solr_feeder.services import get_bearer_token, get_business_info, get_owners, get_parties, update_search


bp = Blueprint('FEEDER', __name__, url_prefix='/feeds')  # pylint: disable=invalid-name


# Feed the specified core with the given data.
@bp.post('')
def feed_solr():
    """Updates the solr cores for namex and search.

    Expected payload for updating namex core:
        {
            solr_core: str,
            request: <raw str representation of solr update/delete object for request>
        }

    Expected payload for updating registries search core:
        {
            solr_core: str,
            identifier: str,
            legalType: str
        }
    """
    logging.debug('request raw data: {}'.format(flask.request.data))
    json_data = flask.request.get_json()

    solr_core = json_data.get('solr_core')
    if not solr_core:
        return {'message': 'Required parameter "solr_core" not defined'}, HTTPStatus.BAD_REQUEST

    if solr_core not in ('names', 'possible.conflicts', 'search'):
        return {'message': 'Parameter "solr_core" only has valid values of "names", "possible.conflicts" or "search"'}, 400

    if solr_core == 'search':
        # update registries search AND bor search
        identifier = json_data.get('identifier')
        legal_type = json_data.get('legalType')
        if not identifier:
            return {'message': 'Required parameter "identifier" not defined'}, HTTPStatus.BAD_REQUEST
        if not legal_type:
            return {'message': 'Required parameter "legalType" not defined'}, HTTPStatus.BAD_REQUEST

        logging.debug('Updating search and bor core records for %s...', identifier)
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
            error = update_search(url=f'{bor_url}/internal/solr/update',
                                  payload={**business, 'parties': parties},
                                  timeout=current_app.config['BOR_API_TIMEOUT'],
                                  token=token)
            if error:
                if error['status_code'] == HTTPStatus.GATEWAY_TIMEOUT:
                    logging.warn('BOR update error probably due to many parties associated ' + \
                                 'with the entity. Please verify the update for %s and ' + \
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
        error = update_search(url=f'{current_app.config["SEARCH_API_URL"]}/internal/solr/update',
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

    else:
        if 'request' not in json_data:
            return {'message': 'Required parameter "request" not defined'}, HTTPStatus.BAD_REQUEST

        logging.debug('Updating namex core record...')
        error_response = solr.update_core(solr_core, json_data['request'])
        if error_response:
            logging.error('Error updating namex core: %s', error_response)
            return {'message': error_response['message']}, error_response['status_code']

        logging.debug('Namex core updated.')

    return {'message': 'Solr core updated'}, HTTPStatus.OK
