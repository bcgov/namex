from flask import jsonify, request
from flask_restplus import Resource, Namespace, cors
from namex.utils.util import cors_preflight
import json
from namex import jwt
import urllib
from flask import current_app
from namex.resources.phonetic import first_vowels, first_arpabet, match_consons

api = Namespace('soundsLikeMeta', description='Sounds Like System - Metadata')
import os

SOLR_URL = os.getenv('SOLR_BASE_URL')


def post_treatment(docs, query):
    names = []
    for candidate in docs:
        name = candidate['name']
        query_first_consonant = query[0]
        name_first_consonant = name[0]
        if match_consons(query_first_consonant, name_first_consonant):
            query_first_vowels = first_vowels(query)
            name_first_vowels = first_vowels(name)
            if query_first_vowels == name_first_vowels:
                names.append({'name': name, 'id': candidate['id'], 'source': candidate['source']})
            else:
                query_first_arpabet = first_arpabet(query)
                name_first_arpabet = first_arpabet(name)
                if query_first_arpabet == name_first_arpabet:
                    names.append({'name': name, 'id': candidate['id'], 'source': candidate['source']})

    return names


@cors_preflight("GET")
@api.route("", methods=['GET', 'OPTIONS'])
class SoundsLike(Resource):

    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.requires_auth
    def get():
        query = request.args.get('query').upper()
        url = SOLR_URL + '/solr/possible.conflicts' + \
              '/select?' + \
              'df=dblmetaphone_name' + \
              '&wt=json' + \
              '&q=' + urllib.parse.quote(query)
        current_app.logger.debug('Sounds-like query: ' + url)
        connection = urllib.request.urlopen(url)
        answer = json.loads(connection.read())
        docs = answer['response']['docs']
        names = post_treatment(docs, query)

        return jsonify({'names': names})

