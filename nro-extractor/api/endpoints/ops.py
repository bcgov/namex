from flask import jsonify
from flask_restplus import Resource, Namespace
from sqlalchemy import text, exc
from api import db

import logging

api = Namespace('nroRequesOPS', description='Name Request System - extractor OPS checks')


sql = text('select 1')

@api.route("/healthz")
class Healthz(Resource):

    @staticmethod
    def get():
        try:
            result = db.engine.execute(sql)
        except exc.SQLAlchemyError:
            return {"message": "api is down"}, 500

        # made it here, so all checks passed
        return {"message": "api is healthy"}, 200


@api.route("/readyz")
class Readyz(Resource):

    @staticmethod
    def get():
        # TODO: add a poll to the DB when called
        return {"message": "api is ready"}, 200
