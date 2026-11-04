from http import HTTPStatus

from flask import current_app, make_response
from flask_restx import Namespace, Resource

from namex.utils.api_resource import handle_exception
from namex.utils.auth import cors_preflight

from .utils import EntityUtils

MSG_BAD_REQUEST_NO_JSON_BODY = 'No JSON data provided'
MSG_SERVER_ERROR = 'Server Error!'
MSG_NOT_FOUND = 'Resource not found'


# Register a local namespace for the NR reserve
entity_api = Namespace(
    'Entity Info', description='Fetch business details such as legal name, status, and filing options'
)


@cors_preflight('GET')
@entity_api.route('/<string:corp_num>', methods=['GET', 'OPTIONS'])
@entity_api.doc(
    description='Fetch business details using the given incorporation number',
    params={'corp_num': 'Incorporation number of the business'},
    responses={
        200: 'Entity information fetched successfully',
        404: 'Entity not found',
        500: 'Internal server error',
    },
)
class EntityApi(Resource):
    def get(self, corp_num):
        try:
            entity_url = f'{current_app.config.get("ENTITY_SVC_URL")}/businesses/{corp_num}'
            response = EntityUtils.make_authenticated_request(entity_url)
            return make_response(response.json(), response.status_code)
        except Exception as err:
            # For other exceptions, handle as an internal server error
            current_app.logger.error(f'Unexpected error: {err}')
            return handle_exception(err, 'Internal Server Error', HTTPStatus.INTERNAL_SERVER_ERROR)
