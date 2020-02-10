import jsonpickle

from flask import request, jsonify, g, current_app, get_flashed_messages, make_response
from flask_restplus import Namespace, Resource, fields, cors
from flask_jwt_oidc import AuthError

from http import HTTPStatus

from namex.utils.util import cors_preflight
from namex.utils.logging import setup_logging

# from sqlalchemy.dialects import postgresql
# from sqlalchemy.orm.exc import NoResultFound
# from sqlalchemy import func, text
# from sqlalchemy.inspection import inspect

from namex import jwt

from namex.services.word_classification.word_classification import WordClassificationService

setup_logging() ## important to do this first

# Register a local namespace for the requests
api = Namespace('wordClassification', description='Word Classification - Core API for Word Classifications')


@api.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@cors_preflight('GET, POST, DELETE')
@api.route('/<string:word>', strict_slashes=False, methods=['GET', 'POST', 'DELETE', 'OPTIONS'])
class WordClassification(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    def get(word):
        response = None

        if request.is_json:
            try:
                service = WordClassificationService()
                # Execute analysis using the supplied builder
                entity = service.find_one(word)

                if not entity:
                    raise ValueError('WordClassificationService did not return a result')

                payload = jsonpickle.encode(entity)

                response = make_response(payload, HTTPStatus.OK)
            except Exception as error:
                print('Error: ' + repr(error))
        else:
            response = make_response(HTTPStatus.BAD_REQUEST)

        return response

    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    def post():
        response = None

        if request.is_json:
            try:
                service = WordClassificationService()
                # Execute analysis using the supplied builder
                entity = service.create(request.json)

                if not entity:
                    raise ValueError('WordClassificationService did not return a result')

                payload = jsonpickle.encode(entity)

                response = make_response(payload, HTTPStatus.CREATED)
            except Exception as error:
                print('Error: ' + repr(error))
        else:
            response = make_response(HTTPStatus.BAD_REQUEST)

        return response

    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    def put():
        response = None

        if request.is_json:
            try:
                service = WordClassificationService()
                # Execute analysis using the supplied builder
                entity = service.create_or_update(request.json)

                if not entity:
                    raise ValueError('WordClassificationService did not return a result')

                payload = jsonpickle.encode(entity)

                response = make_response(payload, HTTPStatus.OK)
            except Exception as error:
                print('Error: ' + repr(error))
        else:
            response = make_response(HTTPStatus.BAD_REQUEST)

        return response

    @staticmethod
    @cors.crossdomain(origin='*')
    # @jwt.requires_auth
    # @api.expect()
    def delete(word):
        response = None

        if request.is_json:
            try:
                service = WordClassificationService()
                # Execute analysis using the supplied builder
                entity = service.delete(word)

                if not entity:
                    raise ValueError('WordClassificationService did not return a result')

                payload = jsonpickle.encode(entity)

                response = make_response(payload, HTTPStatus.NO_CONTENT)
            except Exception as error:
                print('Error: ' + repr(error))
        else:
            response = make_response(HTTPStatus.BAD_REQUEST)

        return response
