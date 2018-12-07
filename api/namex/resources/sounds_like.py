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


def vowels_indexes(word):
    indexes = [word.find('A'), word.find('E'), word.find('I'), word.find('O'), word.find('U'), word.find('Y')]
    indexes = [x for x in indexes if x >= 0]
    indexes.sort()
    return indexes


def first_vowels_index(word):
    return vowels_indexes(word)[0]


def second_vowels_index(word):
    return vowels_indexes(word)[1]


def build_vowel_sound(param):
    if len(param)>=3 and param[0]=='I' and param[1]==param[2]:
        return 'E' + param[2:]
    if len(param)>=3 and param[0]=='E' and param[1]=='E':
        return 'E' + param[2:]

    return param


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
              '&wt=json' + \
              '&q=' + urllib.parse.quote(query.lower())
        current_app.logger.debug('Sounds-like query: ' + url)
        connection = urllib.request.urlopen(url)
        answer = json.loads(connection.read())
        docs = answer['response']['docs']
        query = query.upper()
        vowel_index = first_vowels_index(query)
        vowel = query[vowel_index]
        names = [{'name': doc['name'], 'id': doc['id'], 'source': doc['source']}
                 for doc in docs if doc['name'].upper()[vowel_index] == vowel]

        for candidate in docs:
            if candidate and len([doc['name'] for doc in names if doc['name']==candidate['name']])==0:
                name = candidate['name']
                name_stem = build_vowel_sound(name[first_vowels_index(name):second_vowels_index(name)])
                query_stem = build_vowel_sound(query[first_vowels_index(query):second_vowels_index(name)])
                if name_stem == query_stem:
                    names.append({'name': name, 'id': candidate['id'], 'source': candidate['source']})

        return jsonify({'names': names})
