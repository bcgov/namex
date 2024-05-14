from flask import request, jsonify, current_app
from flask_restx import Namespace, Resource, cors, fields as rp_fields
from marshmallow import Schema, validates, ValidationError, fields as ma_fields
from namex import jwt

import enum

from namex.utils.auth import cors_preflight
from namex.analytics import SolrQueries, RestrictedWords, VALID_ANALYSIS

api = Namespace('namexDocuments', description='Namex - OPS checks')


class DocumentType(enum.Enum):
    type_unspecified = 'TYPE_UNSPECIFIED'
    plain_text = 'PLAIN_TEXT'


class DocumentSchema(Schema):
    type = ma_fields.String(
        required=True,
        error_messages={'required': {'message': 'type is a required field'}}
    )
    content = ma_fields.String(
        required=True,
        error_messages={'required': {'message': 'content is a required field'}}
    )

    @validates('type')
    def validate_type(self, value):
        values = [item.value for item in DocumentType]
        if value.upper() not in values:
            raise ValidationError('Document Type must be one of: {}.'.format(DocumentType._member_names_))

    @validates('content')
    def validate_content(self, value):
        if len(value) <= 1:
            raise ValidationError('Document Content must have more than 1 character.')


@cors_preflight("POST, GET")
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

    a_document = api.model('document', {
        'type': rp_fields.String(description='The object type', enum=DocumentType._member_names_),
        'content': rp_fields.String(description='string content of the document', required=True),
    })

    @staticmethod
    @jwt.requires_auth
    @api.expect(a_document)
    def post(analysis=None, *args, **kwargs):
        start = request.args.get('start', DocumentAnalysis.START)
        rows = request.args.get('rows', DocumentAnalysis.ROWS)

        if analysis.lower() not in VALID_ANALYSIS:
            current_app.logger.info('requested analysis:{} is not valid'.format(analysis.lower()))
            return jsonify(message='{analysis} is not a valid analysis'.format(analysis=analysis)), 404

        json_input = request.get_json()
        if not json_input:
            return jsonify(message='No JSON data provided'), 400

        err = DocumentSchema().validate(json_input)
        if err:
            return jsonify(err), 400

        content = json_input['content']

        if analysis in RestrictedWords.RESTRICTED_WORDS:
            results, msg, code = RestrictedWords.get_restricted_words_conditions(content)

        else:
            current_app.logger.debug('Solr Search: {}'.format(content))
            results, msg, code = SolrQueries.get_results(analysis.lower(), content, start=start, rows=rows)

        if code:
            return jsonify(message=msg), code
        return jsonify(results), code

    @staticmethod
    @jwt.requires_auth
    def get(analysis=None, *args, **kwargs):
        # added because namerequest has no token and auto generated can't be allowed to POST
        # (would have updated above post to get but corresponding UI change in namex-fe-caddy couldn't be built at the time)
        start = request.args.get('start', DocumentAnalysis.START)
        rows = request.args.get('rows', DocumentAnalysis.ROWS)

        if not analysis or analysis.lower() not in VALID_ANALYSIS:
            current_app.logger.info('requested analysis:{} is not valid'.format(analysis.lower()))
            return jsonify(message='{analysis} is not a valid analysis'.format(analysis=analysis)), 404

        json_input = {
            'content': request.args.get('content'),
            'type': request.args.get('type', 'plain_text')
        }
        if not json_input:
            return jsonify(message='No JSON data provided'), 400

        err = DocumentSchema().validate(json_input)
        if err:
            return jsonify(err), 400

        content = json_input['content']

        if analysis in RestrictedWords.RESTRICTED_WORDS:
            results, msg, code = RestrictedWords.get_restricted_words_conditions(content)

        else:
            current_app.logger.debug('Solr Search: {}'.format(content))
            results, msg, code = SolrQueries.get_results(analysis.lower(), content, start=start, rows=rows)

        if code:
            return jsonify(message=msg), code
        return jsonify(results), code
