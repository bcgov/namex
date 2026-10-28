from flask import jsonify, make_response, request
from flask_restx import Namespace, Resource
from flask_restx import fields as rp_fields

from namex import jwt
from namex.models.restricted_words import RestrictedWords
from namex.utils.auth import cors_preflight

api = Namespace('Name Checks', description='Checks names for conflicts, word restrictions, and other issues')


@cors_preflight('POST, GET')
@api.route('/restricted-words', methods=['POST', 'GET', 'OPTIONS'])
class DocumentAnalysis(Resource):
    """
    :param analysis (str): the type of analysis to perform
    :param args: start: number of hits to start from, default is 0
    :param args: names_per_page: number of names to return per page, default is 50
    :param kwargs: __futures__
    :return: 200 - success; 40X for errors
    """

    START = 0
    ROWS = 50

    a_document = api.model(
        'document',
        {
            'content': rp_fields.String(description='string content of the document', required=True),
        },
    )

    @staticmethod
    @jwt.requires_auth
    @api.expect(a_document)
    @api.doc(
        description='Check submitted name content for restricted words',
        responses={
            200: 'Analysis completed successfully',
            400: 'Invalid input or missing content',
            401: 'Unauthorized',
            404: 'Unsupported analysis type',
            500: 'Internal server error',
        },
    )
    def post():
        json_input = request.get_json()
        if not json_input:
            return make_response(jsonify(message='No JSON data provided'), 400)

        content = json_input['content']
        if not content:
            return make_response(jsonify(message='No name content provided'), 400)

        results, msg, code = RestrictedWords.get_restricted_words_conditions(content)

        if code:
            return make_response(jsonify(message=msg), code)
        return make_response(jsonify(results), code)

    @staticmethod
    @jwt.requires_auth
    @api.doc(
        description='Check name content using query parameters instead of a request body',
        params={
            'content': 'The name content to analyze',
        },
        responses={
            200: 'Analysis completed successfully',
            400: 'Invalid input or missing content',
            401: 'Unauthorized',
            404: 'Unsupported analysis type',
            500: 'Internal server error',
        },
    )
    def get():
        content = request.args.get('content')
        if not content:
            return make_response(jsonify(message='No name content provided'), 400)

        results, msg, code = RestrictedWords.get_restricted_words_conditions(content)

        if code:
            return make_response(jsonify(message=msg), code)
        return make_response(jsonify(results), code)
