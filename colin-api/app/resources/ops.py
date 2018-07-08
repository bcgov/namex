from flask_restplus import Resource
from sqlalchemy import text, exc
from app import api, db, app


sql = text('select 1')

@api.route("/corporations/healthz")
class Healthz(Resource):

    @staticmethod
    def get():
        try:
            db.engine.execute(sql)
        except exc.SQLAlchemyError:
            return {"message": "api is down -- error connecting to colin"}, 500

        try:
            db.get_engine(app, 'db2').execute(sql)
        except exc.SQLAlchemyError:
            return {"message": "api is down -- error connecting to namesU"}, 500

        return {"message": "api is healthy"}, 200

@api.route("/corporations/readyz")
class Readyz(Resource):

    @staticmethod
    def get():
        # TODO: add pole to db when called
        return {"message": "api is ready"}, 200
