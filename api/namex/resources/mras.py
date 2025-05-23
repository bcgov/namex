from http import HTTPStatus

import requests
import xmltodict
from flask import current_app, jsonify, make_response
from flask_restx import Namespace, Resource
from lxml import etree  # Don't worry about this it exists... the module is dynamically loaded

from namex.utils.api_resource import handle_exception
from namex.utils.auth import cors_preflight

MSG_BAD_REQUEST_NO_JSON_BODY = 'No JSON data provided'
MSG_SERVER_ERROR = 'Server Error!'
MSG_NOT_FOUND = 'Resource not found'


class MrasServiceException(Exception):
    def __init__(self, mras_error=None, message=None):
        # eg.
        # '{"mras_response":{"mras_error":{"error_code":"401","internal_error_code":"1001","error_message":"Unauthorized access; a valid API token is required","internal_error_message":"Unauthorized access; a valid API token is required","error_instance_id":null}}}'
        self.error_code = int(mras_error['error_code'])
        self.mras_error_code = int(mras_error['internal_error_code'])
        self.message = message if message else str(self.mras_error_code) + ': ' + mras_error['internal_error_message']
        super().__init__(self.message)


# Register a local namespace for the NR reserve
mras_profile_api = Namespace('mras', description='MRAS API')


def load_xml_response_content(response, xpath_query=None):
    """
    Loads the response
    :param response:
    :param xpath_query:
    :return:
    """
    # Parse the XML
    parser = etree.XMLParser(resolve_entities=False)
    xml_content = etree.fromstring(response.content, parser)

    if xpath_query:
        return xml_content.xpath(xpath_query, namespaces={'mras': 'http://mras.ca/schema/v1'})

    return xml_content


@cors_preflight('GET')
@mras_profile_api.route('/<string:province>/<string:corp_num>', strict_slashes=False, methods=['GET', 'OPTIONS'])
@mras_profile_api.doc(
    params={
        'province': 'Province - This field is required',
        'corp_num': 'Incorporation Number - This field is required',
    }
)
class MrasProfile(Resource):
    def get(self, province, corp_num):
        try:
            # Get the jurisdiction
            current_app.logger.debug(
                'Calling MRAS Jurisdictions API using [corp_num: {corp_num}]'.format(corp_num=corp_num)
            )
            mras_url = f'{current_app.config.get("MRAS_SVC_URL")}/api/v1/xpr/jurisdictions/{corp_num}'
            headers = {'x-api-key': current_app.config.get('MRAS_SVC_API_KEY'), 'Accept': 'application/xml'}

            current_app.logger.debug(mras_url)
            current_app.logger.debug(repr(headers))
            response = requests.get(mras_url, headers=headers)

            if not response.status_code == 200:
                mras_errors = load_xml_response_content(response, './/mras_error')
                mras_error = {
                    'error_code': mras_errors[0].find('error_code').text,
                    'internal_error_code': mras_errors[0].find('internal_error_code').text,
                    'internal_error_message': mras_errors[0].find('internal_error_message').text,
                }

                raise MrasServiceException(mras_error=mras_error, message='Error retrieving MRAS profile jurisdictions')

            jurisdiction_id_els = load_xml_response_content(response, './/mras:JurisdictionID')
            jurisdiction_ids = [j.text for j in jurisdiction_id_els]  # All we care about are the codes / IDs

            if province not in jurisdiction_ids:
                return make_response(
                    jsonify(message='Invalid request, province jurisdiction is incorrect'), HTTPStatus.BAD_REQUEST
                )
            else:
                current_app.logger.debug('Valid jurisdiction IDs')
                current_app.logger.debug(repr(jurisdiction_ids))

            # Get the profile
            current_app.logger.debug(
                '\nCalling MRAS Profile API using [corp_num: {corp_num}], [province: {province}]'.format(
                    corp_num=corp_num, province=province
                )
            )
            mras_url = f'{current_app.config.get("MRAS_SVC_URL")}/api/v1/xpr/GetProfile/{corp_num}/{province}'

            headers = {'x-api-key': current_app.config.get('MRAS_SVC_API_KEY'), 'Accept': 'application/xml'}

            current_app.logger.debug(mras_url)
            current_app.logger.debug(repr(headers))
            response = requests.get(mras_url, headers=headers)

            # Return the auth response if an error occurs
            if not response.status_code == HTTPStatus.OK:
                return make_response(
                    jsonify({'error': 'No profile found for the jurisdiction, registration number pair.'}),
                    HTTPStatus.NOT_FOUND,
                )

            # Just return true or false, the profile either exists or it doesn't
            # Note: the response content is in xml format so we need to parse it to json format.
            dict_data = xmltodict.parse(response.content)
            jsonify_data = jsonify(dict_data)
            return make_response(jsonify_data, HTTPStatus.OK)
        except MrasServiceException as err:
            return handle_exception(err, err.message, err.error_code)
        except Exception as err:
            return handle_exception(err, 'Internal Server Error', HTTPStatus.INTERNAL_SERVER_ERROR)
