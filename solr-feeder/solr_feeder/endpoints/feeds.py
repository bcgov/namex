
import logging

import flask
import flask_restplus

from solr_feeder import solr


__all__ = ['api']


api = flask_restplus.Namespace('Feeds', description='Feed updates from legacy databases')


# Feed the specified core with the given data.
@api.route('')
class _Names(flask_restplus.Resource):
    solr_request_model = api.model(
        'Solr Request', {
            'solr_core': flask_restplus.fields.String(),
            'request': flask_restplus.fields.String()
        }
    )

    @api.expect(solr_request_model)
    def post(self):
        logging.debug('request raw data: {}'.format(flask.request.data))
        json_data = flask.request.get_json()

        if 'solr_core' not in json_data:
            return {'message': 'Required parameter "solr_core" not defined'}, 400

        solr_core = json_data['solr_core']
        if solr_core not in ('names', 'possible.conflicts'):
            return {'message': 'Parameter "solr_core" only has valid values of "names" or "possible.conflicts"'}, 400

        if 'request' not in json_data:
            return {'message': 'Required parameter "request" not defined'}, 400

        error_response = solr.update_core(solr_core, json_data['request'])
        if error_response:
            return {'message': error_response['message']}, error_response['status_code']

        return {'message': 'Solr core updated'}, 200
