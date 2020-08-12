from flask import jsonify

from namex.services.name_request.utils import handle_exception
from namex.services.statistics.wait_time_statistics import WaitTimeStatsService
from namex.services.exceptions import ApiServiceException
from namex.utils.logging import setup_logging
from flask_restplus import Namespace, Resource, cors, fields
from flask_jwt_oidc import AuthError

from http import HTTPStatus

from namex.utils.util import cors_preflight

setup_logging()  # important to do this first

# Register a local namespace for the requests
api = Namespace('waitTimeStats', description='API for Wait Time Statistics')


@api.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@cors_preflight('GET')
@api.route('/', strict_slashes=False, methods=['GET','OPTIONS'])
class WaitTimeStats(Resource):
    @staticmethod
    @cors.crossdomain(origin='*')
    def get():
        try:
            service = WaitTimeStatsService()
            response = service.get_statistics()

            if not response:
                raise ApiServiceException(message='WaitTimeStatsService did not return a result')

            return jsonify(response), HTTPStatus.OK

        except ValueError as err:
            return jsonify('Wait time stats not found: ' + repr(err)), 200
        except ApiServiceException as err:
            return handle_exception(err, err.message, 400)
        except Exception as err:
            return jsonify('Internal Server Error\n' + repr(err)), 500
