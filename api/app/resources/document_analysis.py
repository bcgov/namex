from flask import request, jsonify, current_app, escape
from flask_restplus import Namespace, Resource, cors, fields as rp_fields
from marshmallow import Schema, validates, ValidationError, fields as ma_fields
from app import oidc

import enum
import sys

from app.utils.util import cors_preflight
from .solr import SolrQueries


api = Namespace('documents', description='Name Request System - OPS checks')


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


@cors_preflight("POST")
@api.route(':<string:analysis>', methods=['POST' ,'OPTIONS'])
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
    @cors.crossdomain(origin='*')
    @oidc.accept_token(require_token=True)
    @api.expect(a_document)
    def post(analysis=None, *args, **kwargs):
        start = request.args.get('start', DocumentAnalysis.START)
        rows = request.args.get('rows' ,DocumentAnalysis.ROWS)

        if analysis.lower() not in SolrQueries.VALID_QUERIES:
            current_app.logger.info('requested analysis:{} is not valid'.format(analysis.lower()))
            return jsonify \
                ({"message": "{analysis} is not a valid analysis".format(analysis=analysis)}), 404

        json_input = request.get_json()

        err = DocumentSchema().validate(json_input)
        if err:
            return jsonify(err)

        name = escape(json_input['content'])
        print('name: {}'.format(name))
        try:
            solr = SolrQueries.get_results(analysis.lower(), name, start=start, rows=rows)
        except Exception as err:
            current_app.logger.error('SOLR - name:{}, analysis:{}, err:{}'.format(nrd_name.name, analysis, err))
            return jsonify({"message": "Internal server error"}) , 500

        analyzed = {"response": {"numFound": solr['response']['numFound'],
                                  "start": solr['response']['start'],
                                  "rows": solr['responseHeader']['params']['rows'],
                                  "maxScore": solr['response']['maxScore'],
                                  "name": solr['responseHeader']['params']['q'][5:]
                                  },
                     'names' :solr['response']['docs'],
                     'highlighting' :solr['highlighting']}

        return jsonify(analyzed), 200

