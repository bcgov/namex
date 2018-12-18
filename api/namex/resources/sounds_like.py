from flask import jsonify, request
from flask_restplus import Resource, Namespace, cors
from namex.utils.util import cors_preflight
import json
from namex import jwt
import urllib
from flask import current_app
from namex.resources.phonetic import first_vowels, first_arpabet, match_consonate, designations, first_consonants

api = Namespace('soundsLikeMeta', description='Sounds Like System - Metadata')
import os

SOLR_URL = os.getenv('SOLR_BASE_URL')


def post_treatment(docs, query):
    query = query.upper()
    names = []
    for candidate in docs:
        name = candidate['name'].upper()
        words = name.split()
        qwords = query.split()

        for qword in qwords:
            for word in words:
                if word not in designations():
                    keep_phonetic_match(candidate, word, names, qword, name)

    return names


def keep_phonetic_match(candidate, word, names, query, name):
    word_first_consonant = first_consonants(word)
    query_first_consonant = first_consonants(query)
    if match_consonate(query_first_consonant, word_first_consonant):
        query_first_vowels = first_vowels(query)
        word_first_vowels = first_vowels(word)
        if query_first_vowels == word_first_vowels:
            keep_candidate(candidate, name, names)
        else:
            query_first_arpabet = first_arpabet(query)
            word_first_arpabet = first_arpabet(word)
            if query_first_arpabet == word_first_arpabet:
                keep_candidate(candidate, name, names)


def keep_candidate(candidate, name, names):
    if len([doc['id'] for doc in names if doc['id'] == candidate['id']]) == 0:
        names.append({'name': name, 'id': candidate['id'], 'source': candidate['source']})


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

