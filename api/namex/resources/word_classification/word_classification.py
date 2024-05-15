from flask import jsonify, make_response, request
from flask_restx import Namespace, Resource, cors, fields
from flask_jwt_oidc import AuthError

from http import HTTPStatus

from namex.utils.auth import cors_preflight
from namex.utils.logging import setup_logging

from namex.services.word_classification.word_classification import WordClassificationService
from namex.models import User
from namex import jwt

setup_logging()  # important to do this first

# Register a local namespace for the requests
api = Namespace('wordClassification', description='API for Word Classifications')

word_request = api.model('word_classification_request', {
    'classification': fields.String,
    'examiner': fields.String,
    'name': fields.String,
    'word': fields.String
})

word_classification = api.model('word_classification', {
    'id': fields.Integer,
    'word': fields.String,
    'classification': fields.String,
    'lastNameUsed': fields.String,
    'lastPrepName': fields.String,
    'frequency': fields.Integer,
    'approvedBy': fields.Integer,
    'approvedDate': fields.DateTime,
    'startDate': fields.DateTime,
    'lastUpdatedBy': fields.Integer,
    'lastUpdatedDate': fields.DateTime
})


@api.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@cors_preflight('GET, POST, PUT, DELETE')
@api.route('/<string:word>', strict_slashes=False, methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
class WordClassification(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    @api.expect(word_request)
    def get(word):
        try:
            service = WordClassificationService()
            entity = service.find_one(word)

            if not entity:
                raise ValueError('WordClassificationService did not return a result')

            return make_response(jsonify({'word': word}), HTTPStatus.OK)
        except ValueError as err:
            return make_response(jsonify('Word [' + word + '] not found: ' + repr(err)), HTTPStatus.NOT_FOUND)
        except Exception as err:
            return make_response(jsonify('Internal server error: ' + repr(err)), HTTPStatus.INTERNAL_SERVER_ERROR)

    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    @api.expect(word_request)
    def post(word):
        json_input = request.get_json()
        if not json_input:
            return make_response(jsonify('No input data provided'), HTTPStatus.BAD_REQUEST)

        try:
            service = WordClassificationService()
            entity = service.create(json_input)
            if not entity:
                raise ValueError('WordClassificationService did not return a result')

            # TODO: Why are we not using the model schema...
            # model_schema = WordClassificationSchema().dump(entity)
            data = entity.json()
            return make_response(jsonify(data), HTTPStatus.OK)
        except ValueError as err:
            return make_response(jsonify('Word [' + word + '] not found: ' + repr(err)), HTTPStatus.NOT_FOUND)
        except Exception as err:
            return make_response(jsonify('Internal server error: ' + repr(err)), HTTPStatus.INTERNAL_SERVER_ERROR)

    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_roles([User.APPROVER])
    # @api.marshal_with(word_classification)
    @api.expect(word_request)
    def put(word):
        json_input = request.get_json()
        if not json_input:
            return make_response(jsonify('No input data provided'), HTTPStatus.BAD_REQUEST)

        try:
            service = WordClassificationService()
            entity = service.create_or_update(json_input)

            if not entity:
                raise ValueError('WordClassificationService did not return a result')
            data = entity.json()
            return make_response(jsonify(data), HTTPStatus.OK)
        except ValueError as err:
            return make_response(jsonify('Word [' + word + '] not found: ' + repr(err)), HTTPStatus.NOT_FOUND)
        except Exception as err:
            return make_response(jsonify('Internal server error: ' + repr(err)), HTTPStatus.INTERNAL_SERVER_ERROR)

    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    def delete(word):
        try:
            service = WordClassificationService()
            service.delete(word)

            return make_response({}, HTTPStatus.OK)
        # except ValueError as err:
        #    return make_response(jsonify('Word [' + word + '] not found: ' + repr(err)), HTTPStatus.NOT_FOUND
        except Exception as err:
            return make_response(jsonify('Internal server error: ' + repr(err)), HTTPStatus.INTERNAL_SERVER_ERROR)
