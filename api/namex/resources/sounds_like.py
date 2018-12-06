from flask import jsonify, request
from flask_restplus import Resource, Namespace, cors
from namex.utils.util import cors_preflight
import json
from namex import jwt
import urllib
from flask import current_app

api = Namespace('soundsLikeMeta', description='Sounds Like System - Metadata')
import os

SOLR_URL = os.getenv('SOLR_BASE_URL')


@cors_preflight("GET")
@api.route("", methods=['GET', 'OPTIONS'])
class ExactMatch(Resource):

    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.requires_auth
    def get():
        query = request.args.get('query')
        url = SOLR_URL + '/solr/possible.conflicts' + \
              '/select?' + \
              'df=dblmetaphone_name' + \
              '&rows=15' + \
              '&wt=json' + \
              '&q=' + urllib.parse.quote(query.lower())
        current_app.logger.debug('Sounds-like query: ' + url)
        connection = urllib.request.urlopen(url)
        answer = json.loads(connection.read())
        docs = answer['response']['docs']
        query = query.upper()
        indexes = [query.find('A'), query.find('E'), query.find('I'), query.find('O'), query.find('U'), query.find('Y')]
        indexes = [x for x in indexes if x > 0]
        vowel_index = min(indexes)
        vowel = query[vowel_index]
        names = [{'name': doc['name'], 'id': doc['id'], 'source': doc['source']}
                 for doc in docs if doc['name'].upper()[vowel_index] == vowel]

        return jsonify({'names': names})
