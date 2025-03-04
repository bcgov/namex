import json
import jsonpickle

from ast import literal_eval

from flask import request, make_response, jsonify
from flask_restx import Namespace, Resource, cors, fields, marshal_with, reqparse
from flask_jwt_oidc import AuthError

from urllib.parse import unquote_plus

from synonyms.utils.logging import logging

from synonyms.services.synonyms.synonym import SynonymService
from synonyms.models import synonym

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


dictionary_list = api.model('DictionaryList', {
    'key': fields.String,
    'list': fields.List(fields.String)
})

# Define our response object
response_dict_list = api.model('SynonymDictionaryList', {
    'data': fields.List(fields.Nested(dictionary_list))
})

# Define our response object
response_list = api.model('SynonymList', {
    'data': fields.List(fields.String)
})

# Define our response object
response_string = api.model('String', {
    'data': fields.String
})


@api.route('/synonyms', strict_slashes=False, methods=['GET'])
class _WordSynonyms(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.response(200, 'SynonymsApi', response_list)
    @marshal_with(response_list)
    @api.doc(params={
        'word': ''
    })
    def get():
        word = unquote_plus(request.args.get('word')) if request.args.get('word') else None

        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_synonyms(word)

        return {
            'data': results
        }


@api.route('/substitutions', strict_slashes=False, methods=['GET'])
class _WordSubstitutions(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.response(200, 'SynonymsApi', response_list)
    @marshal_with(response_list)
    @api.doc(params={
        'word': ''
    })
    def get():
        word = unquote_plus(request.args.get('word')) if request.args.get('word') else None

        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_substitutions(word)

        return {
            'data': results
        }


@api.route('/all-substitutions-synonyms', strict_slashes=False, methods=['GET'])
class _AllSubstitutionsSynonyms(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.response(200, 'SynonymsApi', response_dict_list)
    @marshal_with(response_dict_list)
    @api.doc(params={
        'words': '',
        'words_are_distinctive': ''
    })
    def get():
        # TODO: Raise an error if no words?
        words = literal_eval(request.args.get('words')) \
            if request.args.get('words') else []

        words_are_distinctive = literal_eval(request.args.get('words_are_distinctive')) \
            if request.args.get('words_are_distinctive') else False

        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_all_substitutions_synonyms(words, words_are_distinctive)

        output = []
        for key in results:
            output.append({
                'key': key,
                'list': results[key]
            })

        return {
            'data': output
        }


@api.route('/all-categories-synonyms', strict_slashes=False, methods=['GET'])
class _AllCategoriesSynonyms(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.response(200, 'SynonymsApi', response_dict_list)
    @marshal_with(response_dict_list)
    @api.doc(params={
        'list_desc': ''
    })
    def get():
        list_desc = literal_eval(request.args.get('list_desc')) \
            if request.args.get('list_desc') else []

        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_all_categories_synonyms(list_desc)

        output = []
        for key in results:
            output.append({
                'key': key,
                'list': results[key]
            })

        return {
            'data': output
        }


@api.route('/stop-words', strict_slashes=False, methods=['GET'])
class _StopWords(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.response(200, 'SynonymsApi', response_list)
    @marshal_with(response_list)
    @api.doc(params={
        'word': ''
    })
    def get():
        word = unquote_plus(request.args.get('word')) if request.args.get('word') else None

        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_stop_words(word)

        return {
            'data': results
        }


@api.route('/prefixes', strict_slashes=False, methods=['GET'])
class _Prefixes(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.response(200, 'SynonymsApi', response_list)
    @marshal_with(response_list)
    @api.doc(params={
    })
    def get():
        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_prefixes()

        return {
            'data': results
        }


@api.route('/stand-alone', strict_slashes=False, methods=['GET'])
class _StandAlone(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.response(200, 'SynonymsApi', response_list)
    @marshal_with(response_list)
    @api.doc(params={
    })
    def get():
        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_standalone()

        return {
            'data': results
        }


@api.route('/number-words', strict_slashes=False, methods=['GET'])
class _NumberWords(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.response(200, 'SynonymsApi', response_list)
    @marshal_with(response_list)
    @api.doc(params={
    })
    def get():
        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_number_words()

        return {
            'data': results
        }


@api.route('/designations', strict_slashes=False, methods=['GET'])
class _Designations(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.response(200, 'SynonymsApi', response_list)
    @marshal_with(response_list)
    @api.doc(params={
        'entity_type_code': '',
        'position_code': '',
        'lang': ''
    })
    def get():
        entity_type_code = unquote_plus(request.args.get('entity_type_code', 'english'))
        position_code = unquote_plus(request.args.get('position_code'))
        lang = unquote_plus(request.args.get('lang'))

        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_designations(entity_type_code, position_code, lang)

        return {
            'data': results
        }


@api.route('/designated-end-all-words', strict_slashes=False, methods=['GET'])
class _DesignatedEndAllWords(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.response(200, 'SynonymsApi', response_list)
    @marshal_with(response_list)
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

        return {
            'data': results
        }


@api.route('/designated-any-all-words', strict_slashes=False, methods=['GET'])
class _DesignatedAnyAllWords(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.response(200, 'SynonymsApi', response_list)
    @marshal_with(response_list)
    @api.doc(params={
        'entity_type_code': '',
        'position_code': '',
        'lang': ''
    })
    def get():
        entity_type_code = None
        position_code = DesignationPositionCodes.ANY.value
        lang = unquote_plus(request.args.get('lang', 'english'))  # Default to english!

        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_designations(entity_type_code, position_code, lang)

        return {
            'data': results
        }


@api.route('/misplaced-end-designations', strict_slashes=False, methods=['GET'])
class _MisplacedEndDesignations(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.response(200, 'SynonymsApi', response_list)
    @marshal_with(response_list)
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

        return {
            'data': results
        }


@api.route('/misplaced-end-designations', strict_slashes=False, methods=['GET'])
class _MisplacedEndDesignations(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.response(200, 'SynonymsApi', response_list)
    @marshal_with(response_list)
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

        return {
            'data': results
        }


@api.route('/misplaced-any-designations', strict_slashes=False, methods=['GET'])
class _MisplacedAnyDesignations(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.response(200, 'SynonymsApi', response_list)
    @marshal_with(response_list)
    @api.doc(params={
        'name': '',
        'designation_any_entity_type': ''
    })
    def get():
        name = unquote_plus(request.args.get('name'))
        designation_any_entity_type = unquote_plus(request.args.get('designation_any_entity_type'))

        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_misplaced_any_designations(name, designation_any_entity_type)

        return {
            'data': results
        }


@api.route('/incorrect-designation-end-in-name', strict_slashes=False, methods=['GET'])
class _IncorrectDesignationEndInName(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.response(200, 'SynonymsApi', response_list)
    @marshal_with(response_list)
    @api.doc(params={
        'tokenized_name': '',
        'designation_end_list': ''
    })
    def get():
        tokenized_name = literal_eval(request.args.get('tokenized_name'))
        designation_end_list = literal_eval(request.args.get('designation_end_list'))

        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_incorrect_designation_end_in_name(tokenized_name, designation_end_list)

        return {
            'data': results
        }


@api.route('/entity-type-end-designation', strict_slashes=False, methods=['GET'])
class _EntityTypeEndDesignation(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.response(200, 'SynonymsApi', response_list)
    @marshal_with(response_list)
    @api.doc(params={
        'entity_end_designation_dict': '',
        'all_designation_any_end_list': ''
    })
    def get():
        entity_end_designation_dict = literal_eval(request.args.get('entity_end_designation_dict'))
        all_designation_any_end_list = literal_eval(request.args.get('all_designation_any_end_list'))

        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_entity_type_end_designation(entity_end_designation_dict, all_designation_any_end_list)

        return {
            'data': results
        }


@api.route('/entity-type-any-designation', strict_slashes=False, methods=['GET'])
class _EntityTypeAnyDesignation(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.response(200, 'SynonymsApi', response_list)
    @marshal_with(response_list)
    @api.doc(params={
        'entity_any_designation_dict': '',
        'all_designation_any_end_list': ''
    })
    def get():
        entity_any_designation_dict = literal_eval(request.args.get('entity_any_designation_dict'))
        all_designation_any_end_list = literal_eval(request.args.get('all_designation_any_end_list'))

        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_entity_type_any_designation(entity_any_designation_dict, all_designation_any_end_list)

        return {
            'data': results
        }


@api.route('/designation-end-in-name', strict_slashes=False, methods=['GET'])
class _DesignationEndInName(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.response(200, 'SynonymsApi', response_list)
    @marshal_with(response_list)
    @api.doc(params={
        'name': ''
    })
    def get():
        name = unquote_plus(request.args.get('name'))

        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_designation_end_in_name(name)

        return {
            'data': results
        }


@api.route('/designation-all-in-name', strict_slashes=False, methods=['GET'])
class _DesignationAllInName(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.response(200, 'SynonymsApi', response_list)
    @marshal_with(response_list)
    @api.doc(params={
        'name': ''
    })
    def get():
        name = unquote_plus(request.args.get('name'))

        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_designation_all_in_name(name)

        return {
            'data': results
        }


@api.route('/designation-any-in-name', strict_slashes=False, methods=['GET'])
class _DesignationAnyInName(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.response(200, 'SynonymsApi', response_list)
    @marshal_with(response_list)
    @api.doc(params={
        'name': ''
    })
    def get():
        name = unquote_plus(request.args.get('name'))

        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_designation_any_in_name(name)

        return {
            'data': results
        }


@api.route('/all-end-designations', strict_slashes=False, methods=['GET'])
class _AllEndDesignations(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.response(200, 'SynonymsApi', response_dict_list)
    @marshal_with(response_dict_list)
    @api.doc(params={
    })
    def get():
        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_all_end_designations()

        output = []
        for key in results:
            output.append({
                'key': key,
                'list': results[key]
            })

        return {
            'data': output
        }


@api.route('/all-any-designations', strict_slashes=False, methods=['GET'])
class _AllAnyDesignations(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.response(200, 'SynonymsApi', response_dict_list)
    @marshal_with(response_dict_list)
    @api.doc(params={
    })
    def get():
        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_all_any_designations()

        output = []
        for key in results:
            output.append({
                'key': key,
                'list': results[key]
            })

        return {
            'data': output
        }


@api.route('/entity-type-by-value', strict_slashes=False, methods=['GET'])
class _EntityTypeByValue(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.response(200, 'SynonymsApi', response_list)
    @marshal_with(response_list)
    @api.doc(params={
        'entity_type_dicts': '',
        'designation': ''
    })
    def get():
        entity_type_dicts = literal_eval(request.args.get('entity_type_dicts'))
        designation = unquote_plus(request.args.get('designation'))

        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.get_entity_type_by_value(entity_type_dicts, designation)

        return {
            'data': results
        }


@api.route('/exception-regex', strict_slashes=False, methods=['GET'])
class _ExceptionRegex(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.response(200, 'SynonymsApi', response_list)
    @marshal_with(response_list)
    @api.doc(params={
        'text': ''
    })
    def get():
        text = unquote_plus(request.args.get('text'))

        if not validate_request(request.args):
            return

        service = SynonymService()
        results = service.exception_regex(text)

        return {
            'data': results
        }


@api.route('/transform-text', strict_slashes=False, methods=['GET'])
class _TransformText(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.response(200, 'SynonymsApi', response_string)
    @marshal_with(response_string)
    @api.doc(params={
        'text': '',
        'designation_all': '',
        'prefix_list': '',
        'number_list': '',
        'exceptions_ws': '',
    })
    def get():
        text = unquote_plus(request.args.get('text'))
        designation_all = literal_eval(request.args.get('designation_all'))
        prefix_list = literal_eval(request.args.get('prefix_list'))
        number_list = literal_eval(request.args.get('number_list'))
        exceptions_ws = literal_eval(request.args.get('exceptions_ws')) if request.args.get('exceptions_ws') else []

        if not validate_request(request.args):
            return

        service = SynonymService()
        result = service.regex_transform(text, designation_all, prefix_list, number_list, exceptions_ws)

        return {
            'data': result
        }


@api.route('/regex-prefixes', strict_slashes=False, methods=['GET'])
class _RegexPrefixes(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    @api.response(200, 'SynonymsApi', response_string)
    @marshal_with(response_string)
    @api.doc(params={
        'text': '',
        'prefixes_str': '',
        'exception_designation': '',
    })
    def get():
        text = unquote_plus(request.args.get('text'))
        prefixes_str = unquote_plus(request.args.get('prefixes_str'))
        exception_designation = literal_eval(request.args.get('exception_designation')) \
            if request.args.get('exception_designation') else []

        if not validate_request(request.args):
            return

        service = SynonymService()
        result = service.regex_prefixes(text, prefixes_str, exception_designation)

        return {
            'data': result
        }

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
