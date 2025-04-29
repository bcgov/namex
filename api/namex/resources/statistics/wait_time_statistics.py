from http import HTTPStatus

from flask import jsonify, make_response
from flask_jwt_oidc import AuthError
from flask_restx import Namespace, Resource

from namex.services.cache import cache
from namex.services.exceptions import ApiServiceException
from namex.services.statistics.wait_time_statistics import WaitTimeStatsService
from namex.utils.api_resource import handle_exception
from namex.utils.auth import cors_preflight

# Register a local namespace for the requests
api = Namespace('waitTimeStats', description='API for Wait Time Statistics')


@api.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@cors_preflight('GET')
@api.route('/', strict_slashes=False, methods=['GET', 'OPTIONS'])
class WaitTimeStats(Resource):
    @staticmethod
    @cache.cached(timeout=14400)  # cached for 4 hours
    def get():
        try:
            service = WaitTimeStatsService()
            response = service.get_statistics()

            if not response:
                raise ApiServiceException(message='WaitTimeStatsService did not return a result')

            return make_response(jsonify(response), HTTPStatus.OK)

        except ValueError as err:
            return make_response(jsonify('Wait time stats not found: ' + repr(err)), 200)
        except ApiServiceException as err:
            return handle_exception(err, err.message, 400)
        except Exception as err:
            return make_response(jsonify('Internal Server Error\n' + repr(err)), 500)
