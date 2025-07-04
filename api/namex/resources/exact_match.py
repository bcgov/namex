import json
import urllib

from flask import current_app, jsonify, request
from flask_restx import Namespace, Resource

from namex import jwt
from namex.utils.auth import cors_preflight

api = Namespace('Exact Match', description='Search for exact business name matches')


@cors_preflight('GET')
@api.route('', methods=['GET', 'OPTIONS'])
class ExactMatch(Resource):
    @staticmethod
    @jwt.requires_auth
    @api.doc(
        description='Fetch existing business names that exactly match the given query',
        params={'query': 'The full name to search for'},
        responses={
            200: 'Match results fetched successfully',
            400: 'Invalid or missing query parameter',
            401: 'Unauthorized',
            500: 'Internal server error',
        },
    )
    def get():
        query = request.args.get('query')
        query = query.lower().replace('*', '')
        url = (
            current_app.config.get('SOLR_BASE_URL')
            + '/solr/possible.conflicts'
            + '/select?'
            + 'sow=false'
            + '&df=name_exact_match'
            + '&wt=json'
            + '&q='
            + urllib.parse.quote(query)
        )
        current_app.logger.debug('Exact-match query: ' + url)
        connection = urllib.request.urlopen(url)
        answer = json.loads(connection.read())
        docs = answer['response']['docs']
        names = [
            {
                'name': doc['name'],
                'id': doc['id'],
                'source': doc['source'],
                'start_date': doc['start_date'],
                'jurisdiction': doc['jurisdiction'],
            }
            for doc in docs
        ]

        return jsonify({'names': names})
