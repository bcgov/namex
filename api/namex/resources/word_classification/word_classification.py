"""Requests used to support the namex API

TODO: Fill in a larger description once the API is defined for V1
"""
from flask import request, jsonify, g, current_app, get_flashed_messages
from flask_restplus import Namespace, Resource, fields, cors
from flask_jwt_oidc import AuthError

from namex.utils.logging import setup_logging
setup_logging() ## important to do this first

from sqlalchemy.dialects import postgresql
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func, text
from sqlalchemy.inspection import inspect

from namex import jwt, nro, services

@api.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response