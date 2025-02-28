from flask_restx import Namespace, Resource

health_api = Namespace("health", description="Liveness and readiness checks")


@health_api.route("/liveness")
class HealthCheck(Resource):
    def get(self):
        return {"status": "ok"}, 200
