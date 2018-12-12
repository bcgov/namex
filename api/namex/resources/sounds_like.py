from flask import jsonify, request
from flask_restplus import Resource, Namespace, cors
from namex.utils.util import cors_preflight
import json
from namex import jwt
import urllib
from flask import current_app
from namex.resources.phonetic import first_vowels, first_arpabet

api = Namespace('soundsLikeMeta', description='Sounds Like System - Metadata')
import os

SOLR_URL = os.getenv('SOLR_BASE_URL')


def distinct_vowels_indexes(word):
    indexes = [word.find('A'), word.find('E'), word.find('I'), word.find('O'), word.find('U'), word.find('Y')]
    indexes = [x for x in indexes if x >= 0]
    indexes.sort()
    return indexes


def first_distinct_vowel_index(word):
    indexes = distinct_vowels_indexes(word)
    if len(indexes) == 0:
        return -1
    return indexes[0]


def second_distinct_vowel_index(word):
    index = first_distinct_vowel_index(word)
    if index == len(word)-1:
        return -1
    suffix = word[index + 1:]
    second_index = first_distinct_vowel_index(suffix)
    if second_index == -1:
        return -1
    return second_index + index + 1


def second_separated_vowel_index(word):
    index = distinct_vowels_indexes(word)[0]
    suffix = word[index + 2:]
    indexes = distinct_vowels_indexes(suffix)
    if len(indexes) == 0:
        return -1
    return indexes[0] + index + 2


def syllable_sound(syllable):
    if len(syllable)>=3 and syllable[0]== 'I' and syllable[1]==syllable[2]:
        return 'E' + syllable[2:]
    if len(syllable)>=3 and syllable[0]== 'E' and syllable[1]== 'E':
        return 'E' + syllable[2:]
    if syllable[0] == 'Y':
        return 'I' + syllable[1:]

    return syllable


def double_vowels_sound(double):
    if double == 'EY':
        return 'A'
    if double == 'EI':
        return 'A'
    if double == 'AY':
        return 'A'

    return double


def match_consons(c1, c2):
    if set(['C', 'G']) == set([c1, c2]):
        return True
    if set(['C', 'K']) == set([c1, c2]):
        return True

    return c1 == c2


def extract_first_vowel_and_following_consons(name):
    name_second_vowel = second_separated_vowel_index(name)
    return name[first_distinct_vowel_index(name):name_second_vowel if name_second_vowel != -1 else len(name)]


def extract_first_two_vowels(name):
    name_second_vowel = second_distinct_vowel_index(name)
    return name[first_distinct_vowel_index(name):name_second_vowel + 1 if name_second_vowel != -1 else len(name)]


def consider_first_syllable_sound(query, candidate, names):
    name = candidate['name']
    name_sound = syllable_sound(extract_first_vowel_and_following_consons(name))
    query_sound = syllable_sound(extract_first_vowel_and_following_consons(query))

    if name_sound == query_sound:
        names.append({'name': name, 'id': candidate['id'], 'source': candidate['source']})


def consider_double_vowels_sound(query, candidate, names):
    name = candidate['name']
    name_sound = double_vowels_sound(extract_first_two_vowels(name))
    query_sound = double_vowels_sound(extract_first_two_vowels(query))

    if name_sound == query_sound:
        names.append({'name': name, 'id': candidate['id'], 'source': candidate['source']})


def add_documents_matching_multi_letters_sound(query, docs, names):
    for candidate in docs:
        if len([doc['name'] for doc in names if doc['name'] == candidate['name']]) == 0:
            consider_first_syllable_sound(query, candidate, names)

        if len([doc['name'] for doc in names if doc['name'] == candidate['name']]) == 0:
            consider_double_vowels_sound(query, candidate, names)


def remove_documents_not_matching_first_vowel(query, docs):
    vowel_index = first_distinct_vowel_index(query)
    vowel = query[vowel_index]
    names = [{'name': doc['name'], 'id': doc['id'], 'source': doc['source']}
             for doc in docs if doc['name'].upper()[vowel_index] == vowel]
    return names


def remove_documents_not_matching_first_letter(query, names):
    query_first_consonants = query[0]
    return [doc for doc in names if match_consons(doc['name'][0], query_first_consonants)]


def add_documents_matching_single_letter_sound(query, docs, names):
    for candidate in docs:
        if len([doc['name'] for doc in names if doc['name'] == candidate['name']]) == 0:
            consider_first_syllable_sound(query, candidate, names)


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

