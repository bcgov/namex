import os
from flask import jsonify, request
from flask_restx import Resource, Namespace, cors
from namex.utils.auth import cors_preflight
import json
from namex import jwt
import urllib
from flask import current_app

api = Namespace('historiesMeta', description='Histories Match - Metadata')
SOLR_URL = os.getenv('SOLR_BASE_URL')
MAX_RESULTS = '50'


@cors_preflight("GET")
@api.route("", methods=['GET', 'OPTIONS'])
class Histories(Resource):

    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.requires_auth
    def get():
        query = request.args.get('query')
        query = query.lower().replace('*', '')
        url = SOLR_URL + '/solr/names' + \
            '/select?' + \
            'sow=false' + \
            '&df=name_exact_match' + \
            '&wt=json' + \
            '&rows=' + MAX_RESULTS + \
            '&q=' + urllib.parse.quote(query)
        current_app.logger.debug('Histories match query: ' + url)
        connection = urllib.request.urlopen(url)
        answer = json.loads(connection.read())

        docs = answer['response']['docs']

        names = [
            {'name': doc['name'],
             'id':doc['id'],
             'name_state_type_cd':doc['name_state_type_cd'],
             'submit_count':doc['submit_count'],
             'nr_num':doc['nr_num'],
             'start_date':doc['start_date'],
             'jurisdiction':doc['jurisdiction']
             } for doc in docs]

        results = {'names': names}
        return jsonify(results)
