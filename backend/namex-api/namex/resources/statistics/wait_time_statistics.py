from http import HTTPStatus

from flask import jsonify, make_response
from flask_restx import Namespace, Resource

from namex.services.cache import cache
from namex.services.exceptions import ApiServiceException
from namex.services.statistics.wait_time_statistics import WaitTimeStatsService
from namex.utils.api_resource import handle_exception
from namex.utils.auth import cors_preflight

# Register a local namespace for wait time statistics
api = Namespace('Wait Time Statistics', description='Fetch average wait time statistics for name request processing')


@cors_preflight('GET')
@api.route('/', strict_slashes=False, methods=['GET', 'OPTIONS'])
class WaitTimeStats(Resource):
    @staticmethod
    @api.doc(
        description='fetch the latest calculated average wait times for name request processing',
        responses={
            200: 'Wait time statistics fetched successfully',
            400: 'Invalid response from WaitTimeStatsService',
            500: 'Internal server error',
        },
    )
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
