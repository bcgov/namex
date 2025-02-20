from flask import request, make_response, jsonify
from flask_restx import Namespace, Resource, cors
from flask_jwt_oidc import AuthError

__all__ = ['api']


api = Namespace('NameProcessing', description='Name Processing Service - Used by Namex API')


@api.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


# TODO: Determine whether to throw an Error or Validation
def validate_request(request):
    return True


@api.route('/', strict_slashes=False, methods=['GET'])
class _NameProcessing(Resource):
    @staticmethod
    def get():
        return ('results', [], 200)


@api.route('/', strict_slashes=False, methods=['GET'])
class _WordClassification(Resource):
    @staticmethod
    def get():
        return ('results', [], 200)
