import json
import jsonpickle

from flask import request, make_response, jsonify
from flask_restplus import Namespace, Resource, cors
from flask_jwt_oidc import AuthError

from urllib.parse import unquote_plus

from synonyms.utils.logging import logging

from synonyms.services.synonyms.synonym import SynonymService
import synonyms.models.synonym as synonym

from synonyms.services.synonyms import DesignationPositionCodes


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


@api.route('/synonyms', strict_slashes=False, methods=['GET'])
class _WordSynonyms(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.doc(params={
        'word': ''
    })
    def get():
        word = unquote_plus(request.args.get('word')) if request.args.get('word') else None

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


@api.route('/substitutions', strict_slashes=False, methods=['GET'])
class _WordSubstitutions(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.doc(params={
        'word': ''
    })
    def get():
        word = unquote_plus(request.args.get('word')) if request.args.get('word') else None

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


@api.route('/stop-words', strict_slashes=False, methods=['GET'])
class _StopWords(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.doc(params={
        'word': ''
    })
    def get():
        word = unquote_plus(request.args.get('word')) if request.args.get('word') else None

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


@api.route('/designated-end-all-words', strict_slashes=False, methods=['GET'])
class _DesignatedEndAllWords(Resource):
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
        entity_type_code = None
        position_code = DesignationPositionCodes.END.value
        lang = unquote_plus(request.args.get('lang', 'english'))  # Default to english!

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


@api.route('/designated-any-all-words', strict_slashes=False, methods=['GET'])
class _DesignatedAnyAllWords(Resource):
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
        entity_type_code = None
        position_code = DesignationPositionCodes.END.value
        lang = unquote_plus(request.args.get('lang', 'english'))  # Default to english!

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


@api.route('/misplaced-end-designations', strict_slashes=False, methods=['GET'])
class _MisplacedEndDesignations(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.doc(params={
        'name': '',
        'designation_end_entity_type': ''
    })
    def get():
        name = unquote_plus(request.args.get('name'))
        designation_end_entity_type = unquote_plus(request.args.get('designation_end_entity_type'))

        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_misplaced_end_designations(name, designation_end_entity_type)

        payload = {
            # Always wrap arrays of JSON data, it prevents an exploit
            'data': results
        }

        response = make_response(jsonpickle.encode(payload), 200)
        return response


@api.route('/misplaced-end-designations', strict_slashes=False, methods=['GET'])
class _MisplacedEndDesignations(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.doc(params={
        'name': '',
        'designation_end_entity_type': ''
    })
    def get():
        name = unquote_plus(request.args.get('name'))
        designation_end_entity_type = unquote_plus(request.args.get('designation_end_entity_type'))

        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_misplaced_end_designations(name, designation_end_entity_type)

        payload = {
            # Always wrap arrays of JSON data, it prevents an exploit
            'data': results
        }

        response = make_response(jsonpickle.encode(payload), 200)
        return response


@api.route('/misplaced-any-designations', strict_slashes=False, methods=['GET'])
class _MisplacedAnyDesignations(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.doc(params={
        'name': '',
        'designation_any_entity_type': ''
    })
    def get():
        name = unquote_plus(request.args.get('name'))
        designation_end_entity_type = unquote_plus(request.args.get('designation_any_entity_type'))

        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_misplaced_any_designations(name, designation_end_entity_type)

        payload = {
            # Always wrap arrays of JSON data, it prevents an exploit
            'data': results
        }

        response = make_response(jsonpickle.encode(payload), 200)
        return response


@api.route('/entity-type-end-designation', strict_slashes=False, methods=['GET'])
class _EntityTypeEndDesignation(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.doc(params={
        'entity_end_designation_dict': '',
        'all_designation_any_end_list': ''
    })
    def get():
        name = unquote_plus(request.args.get('entity_end_designation_dict'))
        designation_end_entity_type = unquote_plus(request.args.get('all_designation_any_end_list'))

        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_entity_type_end_designation(name, designation_end_entity_type)

        payload = {
            # Always wrap arrays of JSON data, it prevents an exploit
            'data': results
        }

        response = make_response(jsonpickle.encode(payload), 200)
        return response


@api.route('/entity-type-any-designation', strict_slashes=False, methods=['GET'])
class _EntityTypeAnyDesignation(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.doc(params={
        'entity_any_designation_dict': '',
        'all_designation_any_end_list': ''
    })
    def get():
        name = unquote_plus(request.args.get('entity_any_designation_dict'))
        designation_end_entity_type = unquote_plus(request.args.get('all_designation_any_end_list'))

        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_entity_type_any_designation(name, designation_end_entity_type)

        payload = {
            # Always wrap arrays of JSON data, it prevents an exploit
            'data': results
        }

        response = make_response(jsonpickle.encode(payload), 200)
        return response


@api.route('/designation-end-in-name', strict_slashes=False, methods=['GET'])
class _DesignationEndInName(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.doc(params={
        'name': ''
    })
    def get():
        name = unquote_plus(request.args.get('name'))

        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_designation_end_in_name(name)

        payload = {
            # Always wrap arrays of JSON data, it prevents an exploit
            'data': results
        }

        response = make_response(jsonpickle.encode(payload), 200)
        return response


@api.route('/designation-all-in-name', strict_slashes=False, methods=['GET'])
class _DesignationAllInName(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.doc(params={
        'name': ''
    })
    def get():
        name = unquote_plus(request.args.get('name'))

        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_designation_all_in_name(name)

        payload = {
            # Always wrap arrays of JSON data, it prevents an exploit
            'data': results
        }

        response = make_response(jsonpickle.encode(payload), 200)
        return response


@api.route('/designation-any-in-name', strict_slashes=False, methods=['GET'])
class _DesignationAllInName(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.doc(params={
        'name': ''
    })
    def get():
        name = unquote_plus(request.args.get('name'))

        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_designation_any_in_name(name)

        payload = {
            # Always wrap arrays of JSON data, it prevents an exploit
            'data': results
        }

        response = make_response(jsonpickle.encode(payload), 200)
        return response


@api.route('/all-end-designations', strict_slashes=False, methods=['GET'])
class _AllEndDesignations(Resource):
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
        results = service.get_all_end_designations()

        payload = {
            # Always wrap arrays of JSON data, it prevents an exploit
            'data': results
        }

        response = make_response(jsonpickle.encode(payload), 200)
        return response


@api.route('/all-any-designations', strict_slashes=False, methods=['GET'])
class _AllAnyDesignations(Resource):
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
        results = service.get_all_any_designations()

        payload = {
            # Always wrap arrays of JSON data, it prevents an exploit
            'data': results
        }

        response = make_response(jsonpickle.encode(payload), 200)
        return response


@api.route('/entity-type-by-value', strict_slashes=False, methods=['GET'])
class _EntityTypeByValue(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.doc(params={
        'entity_type_dicts': '',
        'designation': ''
    })
    def get():
        entity_type_dicts = unquote_plus(request.args.get('entity_type_dicts'))
        designation = unquote_plus(request.args.get('designation'))

        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_entity_type_by_value(entity_type_dicts, designation)

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
