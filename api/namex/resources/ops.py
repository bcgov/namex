from flask_restx import Namespace, Resource
from sqlalchemy import exc, text

from namex.models import db

api = Namespace('namexRequestOPS', description='Namex - OPS checks')

sql = text('select 1')


@api.route('/healthz')
class Healthz(Resource):
    @staticmethod
    def get():
        try:
            db.engine.execute(sql)
        except exc.SQLAlchemyError:
            return {'message': 'api is down'}, 500

        # made it here, so all checks passed
        return {'message': 'api is healthy'}, 200


@api.route('/readyz')
class Readyz(Resource):
    @staticmethod
    def get():
        # TODO: add a poll to the DB when called
        return {'message': 'api is ready'}, 200
