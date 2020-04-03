import json
import jsonpickle

from flask import request, make_response, jsonify
from flask_restplus import Namespace, Resource, cors
from flask_jwt_oidc import AuthError

from urllib.parse import unquote_plus

from synonyms.utils.logging import logging

from synonyms.services.synonyms.synonym import SynonymService
import synonyms.models.synonym as synonym


__all__ = ['api']


api = Namespace('Synonyms', description='Synonyms Service - Used by Namex API and Name Processing Service')


@api.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


# TODO: Determine whether to throw an Error or Validation
def validate_request(request):
    return True


@api.route('/synonyms/<word>', strict_slashes=False, methods=['GET'])
class _WordSynonyms(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.doc(params={
    })
    def get(word=None):
        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_synonyms(word)

        payload = {
            # Always wrap arrays of JSON data, it prevents an exploit
            'data': results
        }

        response = make_response(jsonpickle.encode(payload), 200)
        return response


@api.route('/substitutions/<word>', strict_slashes=False, methods=['GET'])
class _WordSubstitutions(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.doc(params={
    })
    def get(word=None):
        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_substitutions(word)

        payload = {
            # Always wrap arrays of JSON data, it prevents an exploit
            'data': results
        }

        response = make_response(jsonpickle.encode(payload), 200)
        return response


@api.route('/stop-words/<word>', strict_slashes=False, methods=['GET'])
class _WordStops(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.doc(params={
    })
    def get(word=None):
        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_stop_words(word)

        payload = {
            # Always wrap arrays of JSON data, it prevents an exploit
            'data': results
        }

        response = make_response(jsonpickle.encode(payload), 200)
        return response


@api.route('/prefixes', strict_slashes=False, methods=['GET'])
class _Prefixes(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.doc(params={
    })
    def get():
        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_prefixes()

        payload = {
            # Always wrap arrays of JSON data, it prevents an exploit
            'data': results
        }

        response = make_response(jsonpickle.encode(payload), 200)
        return response


@api.route('/number-words', strict_slashes=False, methods=['GET'])
class _NumberWords(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.doc(params={
    })
    def get():
        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_number_words()

        payload = {
            # Always wrap arrays of JSON data, it prevents an exploit
            'data': results
        }

        response = make_response(jsonpickle.encode(payload), 200)
        return response


@api.route('/designations', strict_slashes=False, methods=['GET'])
class _Designations(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.doc(params={
        'entity_type_code': '',
        'position_code': '',
        'lang': ''
    })
    def get():
        entity_type_code = unquote_plus(request.args.get('entity_type_code'))
        position_code = unquote_plus(request.args.get('position_code'))
        lang = unquote_plus(request.args.get('lang'))

        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_designations(entity_type_code, position_code, lang)

        payload = {
            # Always wrap arrays of JSON data, it prevents an exploit
            'data': results
        }

        response = make_response(jsonpickle.encode(payload), 200)
        return response


@api.route('/transform-text', strict_slashes=False, methods=['GET'])
class _TransformText(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.doc(params={
        'text': '',
        'designation_all': '',
        'prefix_list': '',
        'number_list': '',
    })
    def get():
        text = unquote_plus(request.args.get('text'))
        designation_all = unquote_plus(request.args.get('designation_all'))
        prefix_list = unquote_plus(request.args.get('prefix_list'))
        number_list = unquote_plus(request.args.get('number_list'))
        # exceptions_ws

        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.regex_transform(text, designation_all, prefix_list, number_list)

        payload = {
            # Always wrap arrays of JSON data, it prevents an exploit
            'data': results
        }

        response = make_response(jsonpickle.encode(payload), 200)
        return response


@api.route('/<col>/<term>', strict_slashes=False, methods=['GET'])
class _Synonyms(Resource):
    @staticmethod
    def get(col, term):
        term = term.strip().lower()
        logging.debug('Doing {} search for "{}"'.format(col, term))

        results = synonym.Synonym.find(term, col)

        if not results:
            return {'message': 'Term \'{}\' not found in any synonyms list'.format(term)}, 404

        response_list = []
        for result in results:
            if col == 'synonyms_text':
                response_list.append(result.synonyms_text)
            # col == stems_text
            else:
                response_list.append(result.stems_text)
        print(response_list)
        return ('results', response_list), 200
