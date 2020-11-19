import os
from flask import jsonify, request
from flask_restx import Resource, Namespace, cors
from namex.utils.auth import cors_preflight
import json
from namex import jwt
import urllib
from flask import current_app

api = Namespace('exactMatchMeta', description='Exact Match System - Metadata')
SOLR_URL = os.getenv('SOLR_BASE_URL')


@cors_preflight("GET")
@api.route("", methods=['GET', 'OPTIONS'])
class ExactMatch(Resource):

    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.requires_auth
    def get():
        query = request.args.get('query')
        query = query.lower().replace('*', '')
        url = SOLR_URL + '/solr/possible.conflicts' + \
            '/select?' + \
            'sow=false' + \
            '&df=name_exact_match' + \
            '&wt=json' + \
            '&q=' + urllib.parse.quote(query)
        current_app.logger.debug('Exact-match query: ' + url)
        connection = urllib.request.urlopen(url)
        answer = json.loads(connection.read())
        docs = answer['response']['docs']
        names = [{'name': doc['name'], 'id':doc['id'], 'source':doc['source'], 'start_date':doc['start_date'], 'jurisdiction':doc['jurisdiction']} for doc in docs]

        return jsonify({'names': names})
