
import logging
import os

import requests


__all__ = ['update_core']


_SOLR_INSTANCE = os.getenv('SOLR_FEEDER_SOLR_INSTANCE', 'http://localhost:8393/solr')
_SOLR_URL = _SOLR_INSTANCE + '/{}/update/json'


# Update the core with the given data.
def update_core(core_name, action, json):
    logging.debug('json to {} in {}: {}'.format(action, core_name, json))

    # Set up the Solr commands, then add a commit command so that the document change is visible.
    if action == 'delete':
        json = {'delete': json['id']}
    else:
        json = {'add': {'doc': json}}

    json['commit'] = {}

    logging.debug('json Solr command: {}'.format(json))

    response = requests.post(_SOLR_URL.format(core_name), json=json)

    if response.status_code != 200:
        logging.error('{} core: {}'.format(core_name, response.json()))

        return {
            'message': '{} core: {}'.format(core_name, response.json()['error']['msg']),
            'status_code': response.status_code
        }

    return None
