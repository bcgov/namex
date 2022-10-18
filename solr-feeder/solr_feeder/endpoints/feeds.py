import logging
from http import HTTPStatus

import flask
from flask import Blueprint

from solr_feeder import solr
from solr_feeder.services import get_business_info, get_owners, update_search


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
        identifier = json_data.get('identifier')
        legal_type = json_data.get('legalType')
        if not identifier:
            return {'message': 'Required parameter "identifier" not defined'}, HTTPStatus.BAD_REQUEST
        if not legal_type:
            return {'message': 'Required parameter "legalType" not defined'}, HTTPStatus.BAD_REQUEST
        logging.debug('Updating search core record for %s...', identifier)
        # get business data
        business, error_response = get_business_info(legal_type, identifier)
        if error_response:
            logging.error('Error getting COLIN business data: %s', error_response)
            return {'message': error_response['message']}, HTTPStatus.INTERNAL_SERVER_ERROR
        
        owners, error_response = get_owners(legal_type, identifier)
        if error_response:
            logging.error('Error getting COLIN owners data: %s', error_response)
            return {'message': error_response['message']}, HTTPStatus.INTERNAL_SERVER_ERROR
        # send data to search core via search-api
        error_response = update_search({**business, **owners})
        if error_response:
            logging.error('Error updating search core: %s', error_response)
            return {'message': error_response['message']}, HTTPStatus.INTERNAL_SERVER_ERROR

        logging.debug('Search core updated.')

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
