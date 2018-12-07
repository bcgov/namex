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


def distinct_vowels_indexes(word):
    indexes = [word.find('A'), word.find('E'), word.find('I'), word.find('O'), word.find('U'), word.find('Y')]
    indexes = [x for x in indexes if x >= 0]
    indexes.sort()
    return indexes


def first_distinct_vowel_index(word):
    return distinct_vowels_indexes(word)[0]


def second_distinct_vowel_index(word):
    index = first_distinct_vowel_index(word)
    suffix = word[index + 1:]
    return first_distinct_vowel_index(suffix) + index + 1


def second_separated_vowel_index(word):
    index = distinct_vowels_indexes(word)[0]
    suffix = word[index + 2:]
    indexes = distinct_vowels_indexes(suffix)
    if len(indexes) == 0:
        return -1
    return indexes[0] + index + 2


def build_first_syllable_sound(param):
    if len(param)>=3 and param[0]=='I' and param[1]==param[2]:
        return 'E' + param[2:]
    if len(param)>=3 and param[0]=='E' and param[1]=='E':
        return 'E' + param[2:]

    return param


def build_first_syllable_double_vowels_sound(param):
    if param == 'EY':
        return 'A'
    if param == 'EI':
        return 'A'
    if param == 'AY':
        return 'A'

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
        vowel_index = first_distinct_vowel_index(query)
        vowel = query[vowel_index]
        names = [{'name': doc['name'], 'id': doc['id'], 'source': doc['source']}
                 for doc in docs if doc['name'].upper()[vowel_index] == vowel]

        for candidate in docs:
            if candidate and len([doc['name'] for doc in names if doc['name']==candidate['name']])==0:
                name = candidate['name']
                name_second_vowel = second_separated_vowel_index(name)
                query_second_vowel = second_separated_vowel_index(query)
                if name_second_vowel > -1 and query_second_vowel > -1:
                    name_first_syllable_sound = build_first_syllable_sound(name[first_distinct_vowel_index(name):name_second_vowel])
                    query_first_syllable_sound = build_first_syllable_sound(query[first_distinct_vowel_index(query):query_second_vowel])
                    if name_first_syllable_sound == query_first_syllable_sound:
                        names.append({'name': name, 'id': candidate['id'], 'source': candidate['source']})

            if candidate and len([doc['name'] for doc in names if doc['name'] == candidate['name']]) == 0:
                name_two_vowels_sound = build_first_syllable_double_vowels_sound(name[first_distinct_vowel_index(name):second_distinct_vowel_index(name) + 1])
                query_two_vowels_sound = build_first_syllable_double_vowels_sound(query[first_distinct_vowel_index(query):second_distinct_vowel_index(query) + 1])
                if name_two_vowels_sound == query_two_vowels_sound:
                    names.append({'name': name, 'id': candidate['id'], 'source': candidate['source']})

        return jsonify({'names': names})
