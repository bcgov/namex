from flask_restx import Namespace, Resource
from sqlalchemy import exc, text

from namex.models import db

api = Namespace('API Health', description='Endpoints to check if the NameX API is healthy and ready to serve traffic')

sql = text('select 1')


@api.route('/healthz')
class Healthz(Resource):
    @api.doc(
        description='Checks if the API is healthy and able to connect to the database',
        responses={
            200: 'API is healthy',
            500: 'Internal server error',
        },
    )
    @staticmethod
    def get():
        try:
            with db.engine.connect() as connection:
                connection.execute(sql)
        except exc.SQLAlchemyError:
            return {'message': 'api is down'}, 500

        # made it here, so all checks passed
        return {'message': 'api is healthy'}, 200


@api.route('/readyz')
class Readyz(Resource):
    @staticmethod
    @api.doc(
        description='Checks if the API is ready to receive requests',
        responses={200: 'API is ready'},
    )
    def get():
        # TODO: add a poll to the DB when called
        return {'message': 'api is ready'}, 200
