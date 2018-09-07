
import logging
import os

import requests


__all__ = ['update_core']


_SOLR_INSTANCE = os.getenv('SOLR_FEEDER_SOLR_INSTANCE', 'http://localhost:8393/solr')
_SOLR_RELOAD_URL = _SOLR_INSTANCE + '/{}/update/json/docs'


# Update the core with the given data.
def update_core(core_name, action, json):
    # Temporary.
    del action

    logging.debug('json for {}: {}'.format(core_name, json))

    response = requests.post(
        _SOLR_RELOAD_URL.format(core_name), headers={'Content-Type': 'application/json'}, json=json)

    if response.status_code != 200:
        logging.error('{} core: {}'.format(core_name, response.json()))

        return {
            'message': '{} core: {}'.format(core_name, response.json()['error']['msg']),
            'status_code': response.status_code
        }

    return None
