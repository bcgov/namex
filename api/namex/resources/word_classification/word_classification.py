from http import HTTPStatus

from flask import jsonify, make_response, request
from flask_jwt_oidc import AuthError
from flask_restx import Namespace, Resource, cors, fields

from namex.services.word_classification.word_classification import WordClassificationService
from namex.utils.auth import cors_preflight

# Register a local namespace for the requests
api = Namespace('Word Classification', description='Fetch and manage word classifications')

word_request = api.model(
    'WordClassificationInput',
    {
        'word': fields.String(required=True, description='The word to classify'),
        'name': fields.String(description='Full name associated with the word'),
        'classification': fields.String(description='Classification code'),
        'examiner': fields.String(description='Examiner who submitted the word'),
    }
)

word_classification = api.model(
    'word_classification',
    {
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
        'lastUpdatedDate': fields.DateTime,
    },
)


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
    @api.doc(
        description='Fetch classification info for a given word',
        params={'word': 'The word to look up classification info for'},
        responses={
            200: 'Word classification fetched successfully',
            404: 'Word not found',
            500: 'Internal server error',
        },
    )
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
    @api.doc(
        description='Create a new classification for the given word',
        responses={
            200: 'Word classification created successfully',
            400: 'Missing input',
            500: 'Internal server error',
        },
    )
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
    @api.doc(
        description='Update or create classification for a given word.',
        responses={
            200: 'Word classification updated successfully',
            400: 'Missing input',
            500: 'Internal server error',
        },
    )
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
    @api.doc(
        description='Delete the classification for a given word.',
        responses={
            200: 'Word classification deleted successfully',
            500: 'Internal server error',
        },
    )
    def delete(word):
        try:
            service = WordClassificationService()
            service.delete(word)

            return make_response({}, HTTPStatus.OK)
        # except ValueError as err:
        #    return make_response(jsonify('Word [' + word + '] not found: ' + repr(err)), HTTPStatus.NOT_FOUND
        except Exception as err:
            return make_response(jsonify('Internal server error: ' + repr(err)), HTTPStatus.INTERNAL_SERVER_ERROR)
