
import flask_restx


__all__ = ['api']


api = flask_restx.Namespace('Probes', description='Operations probes to determine liveness and readiness')


# If we are reachable, we consider ourselves to be live.
@api.route('/liveness')
class _Liveness(flask_restx.Resource):
    @staticmethod
    def get():
        return {'message': 'Liveness checks passed'}, 200


# If we are reachable, we consider ourselves to be ready.
@api.route('/readiness')
class _Readiness(flask_restx.Resource):
    @staticmethod
    def get():
        return {'message': 'Readiness checks passed'}, 200
