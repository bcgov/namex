
import logging

import flask
import flask_restplus

from solr_feeder.models import solr_dataimport_conflicts, solr_dataimport_names
from solr_feeder import solr


__all__ = ['api']


api = flask_restplus.Namespace('Feeds', description='Feed updates from legacy databases')


# Feed the cores with the data corresponding to the posted corporation number.
@api.route('/corporations')
class _Corporations(flask_restplus.Resource):
    @staticmethod
    def post():
        return {'message': 'Okie dokie'}, 200


# Feed the cores with the data corresponding to the posted name request number.
@api.route('/names')
class _Names(flask_restplus.Resource):
    name_request_number_model = api.model(
        'Name Request Number', {
            'nameRequestNumber': flask_restplus.fields.String(),
            'solr_core': flask_restplus.fields.String(),
            'action': flask_restplus.fields.String()
        }
    )

    @api.expect(name_request_number_model)
    def post(self):
        logging.debug('request raw data: {}'.format(flask.request.data))
        json = flask.request.get_json()

        # Validate the request.
        if not json or 'nameRequestNumber' not in json:
            return {'message': 'Required parameter "nameRequestNumber" not defined'}, 400

        name_request_number = json['nameRequestNumber']

        if 'solr_core' not in json:
            return {'message': 'Required parameter "solr_core" not defined'}, 400

        solr_core = json['solr_core']
        if solr_core not in ('names', 'possible.conflicts'):
            return {'message': 'Parameter "solr_core" has valid values "names" or "possible.conflicts"'}, 400

        if 'action' not in json:
            return {'message': 'Required parameter "action" not defined'}, 400

        action = json['action']
        if action not in ('delete', 'update'):
            return {'message': 'Parameter "action" has valid values "delete" or "update"'}, 400

        # Do the changes to the cores.
        if solr_core == 'names':
            response = self._dataimport_names(name_request_number, action)
            if response[1] != 200:
                return response
        else:
            response = self._dataimport_conflicts(name_request_number, action)
            if response[1] != 200:
                return response

        return {'message': 'Solr cores updated'}, 200

    @staticmethod
    def _dataimport_conflicts(name_request_number: str, action: str):
        result = solr_dataimport_conflicts.SolrDataimportConflicts.find(name_request_number)
        if not result:
            logging.info('Conflicts lookup of "{}" failed'.format(name_request_number))

            return {'message': 'Unknown "id" of "{}" in SOLR_DATAIMPORT_CONFLICTS_VW'.format(name_request_number)}, 404

        json = solr_dataimport_conflicts.SolrDataimportConflictsSchema().dump(result).data
        _convert_json_none_to_empty_string(json)
        logging.info('Conflicts lookup of "{}" succeeded'.format(json['id']))

        # Update the core. If any update fails we quit and leave the state inconsistent. A retry by the caller will sync
        # everything.
        error_response = solr.update_core('possible.conflicts', action, json)
        if error_response:
            return {'message': error_response['message']}, error_response['status_code']

        return {'message': 'Solr core updated'}, 200

    @staticmethod
    def _dataimport_names(name_request_number: str, action: str):
        results = solr_dataimport_names.SolrDataimportNames.find(name_request_number)
        if not results:
            logging.info('Names lookup of "{}" failed'.format(name_request_number))

            return {'message': 'Unknown "nr_num" of "{}" in SOLR_DATAIMPORT_NAMES_VW'.format(name_request_number)}, 404

        for result in results:
            json = solr_dataimport_names.SolrDataimportNamesSchema().dump(result).data
            _convert_json_none_to_empty_string(json)
            logging.info('Names lookup of "{}" succeeded'.format(json['id']))

            # Update the core. If any update fails we quit and leave the state inconsistent. A retry by the caller will
            # sync everything.
            error_response = solr.update_core('names', action, json)
            if error_response:
                return {'message': error_response['message']}, error_response['status_code']

        return {'message': 'Solr core updated'}, 200


# If we get null values from the database, convert them from None to ''.
def _convert_json_none_to_empty_string(json: dict) -> dict:
    for key in json.keys():
        if not json[key]:
            json[key] = ''

    return json
