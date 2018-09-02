
import logging

import flask
import flask_restplus
import requests

from solr_feeder.models import completed_nr
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
        'Name Request Number', {'nameRequestNumber': flask_restplus.fields.String('Name Request Number')})

    @api.expect(name_request_number_model)
    def post(self):
        request_json = flask.request.get_json()
        if not request_json or 'nameRequestNumber' not in request_json:
            return {'message': 'Required parameter "nameRequestNumber" not defined'}, 400

        name_request_number = request_json['nameRequestNumber']
        name_request = completed_nr.CompletedNr.find(name_request_number)
        if not name_request:
            logging.info('Names lookup of "{}" failed'.format(name_request_number))

            return {'message': 'Unknown "nameRequestNumber" of "{}"'.format(name_request_number)}, 404

        logging.info('Names lookup of "{}" succeeded'.format(name_request_number))

        json = completed_nr.CompletedNrSchema().dump(name_request).data

        # Alter the data to conform to what the Solr core is expecting.
        #
        # names: SELECT nr_num || '-' || choice_number AS id, name_instance_id, choice_number, corp_num, name, nr_num,
        # request_id, submit_count, request_type_cd, name_id, start_event_id, name_state_type_cd
        names_json = _convert_json_none_to_empty_string({
            'id': json['nr_num'] + '-' + str(json['choice_number']),
            'name_instance_id': json['name_instance_id'],
            'choice_number': json['choice_number'],
            'corp_num': json['corp_num'],
            'name': json['name'],
            'nr_num': json['nr_num'],
            'request_id': json['request_id'],
            'request_type_cd': json['request_type_cd'],
            'name_id': json['name_id'],
            'start_event_id': json['start_event_id'],
            'name_state_type_cd': json['name_state_type_cd']
        })

        # Alter the data to conform to what the Solr core is expecting. We should create new views that only return the
        # data that is needed.
        #
        # possible.conflicts: SELECT nr_num AS id, name, name_state_type_cd AS state_type_cd, 'NR' AS source
        possible_conflicts_json = _convert_json_none_to_empty_string({
            'id': json['nr_num'],
            'name': json['name'],
            'state_type_cd': json['name_state_type_cd'],
            'source': 'NR'
        })

        # Update the cores. In the case that the first update succeeds and the second fails, the two Solr cores will
        # be inconsistent. However, the caller will receive a non-200 response, and will retry both updates at a later
        # time. The core data will eventually be consistent.
        response = solr.update_core('names', names_json)
        if response:
            return {'message': response['message']}, response['status_code']

        response = solr.update_core('possible.conflicts', possible_conflicts_json)
        if response:
            return {'message': response['message']}, response['status_code']

        return {'message': 'Solr cores updated'}, 200


# If we get null values from the database, convert them from None to ''.
def _convert_json_none_to_empty_string(json: dict) -> dict:
    for key in json.keys():
        if not json[key]:
            json[key] = ''

    return json
