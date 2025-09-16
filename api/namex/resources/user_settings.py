from flask import current_app, g, jsonify, make_response, request
from flask_jwt_oidc.exceptions import AuthError
from flask_restx import Namespace, Resource, fields

from namex import jwt
from namex.models import User
from namex.services.name_request.utils import get_or_create_user_by_jwt
from namex.utils.auth import cors_preflight

api = Namespace('User Settings', description='Fetch or update saved user preferences')


@api.errorhandler(AuthError)
def handle_auth_error(ex):
    return {'message': 'Unauthorized', 'details': ex.error.get('description') or 'Invalid or missing token'}, 401


user_settings_model = api.model(
    'UserSettings',
    {'searchColumns': fields.List(fields.String, required=True, description='List of search column names')},
)


@cors_preflight('GET, PUT')
@api.route('', methods=['GET', 'PUT', 'OPTIONS'])
class UserSettings(Resource):
    @staticmethod
    @jwt.requires_auth
    @api.doc(
        description='Fetch saved search column preferences for the current user',
        responses={
            200: 'User settings fetched successfully',
            401: 'Unauthorized',
            500: 'Internal server error',
        },
    )
    def get(*args, **kwargs):
        try:
            # GET existing or CREATE new user based on the JWT info
            user = get_or_create_user_by_jwt(g.jwt_oidc_token_info)
            search_columns = user.searchColumns.split(',')
            return make_response(jsonify({'searchColumns': search_columns}), 200)

        except Exception as err:
            current_app.logger.error(f'unable to get user settings: {err.with_traceback(None)}')
            return make_response(jsonify({'message': 'Error getting user settings.'}), 500)

    @staticmethod
    @jwt.requires_auth
    @api.expect(user_settings_model)
    @api.doc(
        description='Update the saved search column preferences for the current user',
        responses={
            204: 'User settings updated successfully',
            400: 'Invalid or missing payload',
            401: 'Unauthorized',
            500: 'Internal server error',
        },
    )
    def put():
        try:
            # GET existing or CREATE new user based on the JWT info
            user = User.find_by_jwtToken(g.jwt_oidc_token_info)
            if not user:
                return make_response(jsonify({'message': 'Could not find existing user to update settings for.'}), 400)
            json_input = request.get_json()
            if not json_input or not json_input.get('searchColumns'):
                return make_response(jsonify({'message': 'Invalid user settings provided in payload.'}), 400)
            search_columns = ''
            for column in json_input.get('searchColumns'):
                if search_columns != '':
                    search_columns += ',' + column
                else:
                    search_columns += column
            user.searchColumns = search_columns
            user.save_to_db()
            return {}, 204

        except Exception as err:
            current_app.logger.error(f'unable to update user settings: {err.with_traceback(None)}')
            return make_response(jsonify({'message': 'Error updating user settings.'}), 500)
