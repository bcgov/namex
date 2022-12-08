from flask import current_app, jsonify, g, request
from flask_restx import cors, Resource, Namespace
from sqlalchemy import text, exc

from namex import jwt
from namex.models import User, State, Comment, NameCommentSchema, Event
from namex.services.name_request.utils import get_or_create_user_by_jwt
from namex.utils.auth import cors_preflight

api = Namespace('namexUserSettings', description='Namex - get/update user settings')


@cors_preflight('GET, PUT')
@api.route('', methods=['GET', 'PUT', 'OPTIONS'])
class UserSettings(Resource):

    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.requires_auth
    def get(*args, **kwargs):
        try:
            # GET existing or CREATE new user based on the JWT info
            user = get_or_create_user_by_jwt(g.jwt_oidc_token_info)
            search_columns = user.searchColumns.split(',')
            return jsonify({ 'searchColumns': search_columns }), 200
            
        except Exception as err:
            current_app.logger.error(f'unable to get user settings: {err.with_traceback(None)}')
            return jsonify({'message': 'Error getting user settings.'}), 500
    
    @staticmethod
    @cors.crossdomain(origin='*')
    @jwt.requires_auth
    def put():
        try:
            # GET existing or CREATE new user based on the JWT info
            user = User.find_by_jwtToken(g.jwt_oidc_token_info)
            if not user:
                return jsonify({'message': 'Could not find existing user to update settings for.'}), 400
            json_input = request.get_json()
            if not json_input or not json_input.get('searchColumns'):
                return jsonify({'message': 'Invalid user settings provided in payload.'}), 400
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
            return jsonify({'message': f'Error updating user settings.'}), 500
