import enum

from flask import current_app, jsonify, make_response, request
from flask_restx import Namespace, Resource
from flask_restx import fields as rp_fields
from marshmallow import Schema, ValidationError, validates
from marshmallow import fields as ma_fields

from namex import jwt
from namex.analytics import VALID_ANALYSIS, RestrictedWords, SolrQueries
from namex.utils.auth import cors_preflight

api = Namespace('Name Checks', description='Checks names for conflicts, word restrictions, and other issues')


class DocumentType(enum.Enum):
    type_unspecified = 'TYPE_UNSPECIFIED'
    plain_text = 'PLAIN_TEXT'


class DocumentSchema(Schema):
    type = ma_fields.String(required=True, error_messages={'required': {'message': 'type is a required field'}})
    content = ma_fields.String(required=True, error_messages={'required': {'message': 'content is a required field'}})

    @validates('type')
    def validate_type(self, value):
        values = [item.value for item in DocumentType]
        if value.upper() not in values:
            raise ValidationError('Document Type must be one of: {}.'.format(DocumentType._member_names_))

    @validates('content')
    def validate_content(self, value):
        if len(value) <= 1:
            raise ValidationError('Document Content must have more than 1 character.')


@cors_preflight('POST, GET')
@api.route(':<string:analysis>', methods=['POST', 'GET', 'OPTIONS'])
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
            'type': rp_fields.String(description='The object type', enum=DocumentType._member_names_),
            'content': rp_fields.String(description='string content of the document', required=True),
        },
    )

    @staticmethod
    @jwt.requires_auth
    @api.expect(a_document)
    @api.doc(
        description='Check submitted name content for issues like restricted words',
        params={
            'analysis': 'The type of check to perform (e.g., conflicts, restricted_words, trademarks, histories)',
            'start': 'Pagination start index (default: 0)',
            'rows': 'Number of results to return (default: 50)',
        },
        responses={
            200: 'Analysis completed successfully',
            400: 'Invalid input or missing content',
            401: 'Unauthorized',
            404: 'Unsupported analysis type',
            500: 'Internal server error',
        },
    )
    def post(analysis=None, *args, **kwargs):
        start = request.args.get('start', DocumentAnalysis.START)
        rows = request.args.get('rows', DocumentAnalysis.ROWS)

        if analysis.lower() not in VALID_ANALYSIS:
            current_app.logger.info('requested analysis:{} is not valid'.format(analysis.lower()))
            return make_response(jsonify(message='{analysis} is not a valid analysis'.format(analysis=analysis)), 404)

        json_input = request.get_json()
        if not json_input:
            return make_response(jsonify(message='No JSON data provided'), 400)

        err = DocumentSchema().validate(json_input)
        if err:
            return make_response(jsonify(err), 400)

        content = json_input['content']

        if analysis in RestrictedWords.RESTRICTED_WORDS:
            results, msg, code = RestrictedWords.get_restricted_words_conditions(content)

        else:
            current_app.logger.debug('Solr Search: {}'.format(content))
            results, msg, code = SolrQueries.get_results(analysis.lower(), content, start=start, rows=rows)

        if code:
            return make_response(jsonify(message=msg), code)
        return make_response(jsonify(results), code)

    @staticmethod
    @jwt.requires_auth
    @api.doc(
        description='Check name content using query parameters instead of a request body',
        params={
            'analysis': 'The type of check to perform (e.g., conflicts, restricted_words, trademarks, histories)',
            'start': 'Pagination start index (default: 0)',
            'rows': 'Number of results to return (default: 50)',
            'content': 'The name content to analyze',
            'type': 'Content type (default: plain_text)',
        },
        responses={
            200: 'Analysis completed successfully',
            400: 'Invalid input or missing content',
            401: 'Unauthorized',
            404: 'Unsupported analysis type',
            500: 'Internal server error',
        },
    )
    def get(analysis=None, *args, **kwargs):
        # added because namerequest has no token and auto generated can't be allowed to POST
        # (would have updated above post to get but corresponding UI change in namex-fe-caddy couldn't be built at the time)
        start = request.args.get('start', DocumentAnalysis.START)
        rows = request.args.get('rows', DocumentAnalysis.ROWS)

        if not analysis or analysis.lower() not in VALID_ANALYSIS:
            current_app.logger.info('requested analysis:{} is not valid'.format(analysis.lower()))
            return make_response(jsonify(message='{analysis} is not a valid analysis'.format(analysis=analysis)), 404)

        json_input = {'content': request.args.get('content'), 'type': request.args.get('type', 'plain_text')}
        if not json_input:
            return make_response(jsonify(message='No JSON data provided'), 400)

        err = DocumentSchema().validate(json_input)
        if err:
            return make_response(jsonify(err), 400)

        content = json_input['content']

        if analysis in RestrictedWords.RESTRICTED_WORDS:
            results, msg, code = RestrictedWords.get_restricted_words_conditions(content)

        else:
            current_app.logger.debug('Solr Search: {}'.format(content))
            results, msg, code = SolrQueries.get_results(analysis.lower(), content, start=start, rows=rows)

        if code:
            return make_response(jsonify(message=msg), code)
        return make_response(jsonify(results), code)
