import os
from lxml import etree  # Don't worry about this it exists... the module is dynamically loaded

import requests

from flask import jsonify
from flask_restplus import Namespace, Resource, cors

from namex.utils.auth import cors_preflight
from namex.utils.api_resource import handle_exception
from namex.utils.logging import setup_logging

setup_logging()  # Important to do this first

MSG_BAD_REQUEST_NO_JSON_BODY = 'No JSON data provided'
MSG_SERVER_ERROR = 'Server Error!'
MSG_NOT_FOUND = 'Resource not found'

MRAS_SVC_PROFILE_URL = os.getenv('MRAS_SVC_URL', '') + '/api/v1/xpr/GetProfile/{profile_id}/{source_jurisdiction_id}'
MRAS_SVC_PROFILE_JUR_URL = os.getenv('MRAS_SVC_URL', '') + '/api/v1/xpr/jurisdictions/{profile_id}'
MRAS_SVC_API_KEY = os.getenv('MRAS_SVC_API_KEY', '')


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
    xml_content = etree.fromstring(response.content)

    if xpath_query:
        return xml_content.xpath(xpath_query, namespaces={'mras': 'http://mras.ca/schema/v1'})

    return xml_content


@cors_preflight('GET')
@mras_profile_api.route('/<string:province>/<string:corp_num>', strict_slashes=False, methods=['GET', 'OPTIONS'])
@mras_profile_api.doc(params={
    'province': 'Province - This field is required',
    'corp_num': 'Incorporation Number - This field is required'
})
class MrasProfile(Resource):
    @cors.crossdomain(origin='*')
    def get(self, province, corp_num):
        try:
            # Get the jurisdiction
            print('Calling MRAS Jurisdictions API using [corp_num: {corp_num}]'.format(corp_num=corp_num))
            mras_url = MRAS_SVC_PROFILE_JUR_URL.format(profile_id=corp_num)
            headers = {
                'x-api-key': MRAS_SVC_API_KEY,
                'Accept': 'application/xml'
            }

            print(mras_url)
            print(repr(headers))
            response = requests.get(
                mras_url,
                headers=headers
            )

            if not response.status_code == 200:
                mras_errors = load_xml_response_content(response, './/mras_error')
                mras_error = {
                    'error_code': mras_errors[0].find('error_code').text,
                    'internal_error_code': mras_errors[0].find('internal_error_code').text,
                    'internal_error_message': mras_errors[0].find('internal_error_message').text
                }

                raise MrasServiceException(mras_error=mras_error, message='Error retrieving MRAS profile jurisdictions')

            jurisdiction_id_els = load_xml_response_content(response, './/mras:JurisdictionID')
            jurisdiction_ids = [j.text for j in jurisdiction_id_els]  # All we care about are the codes / IDs

            if province not in jurisdiction_ids:
                return jsonify(message='Invalid request, province jurisdiction is incorrect'), 400
            else:
                print('Valid jurisdiction IDs')
                print(repr(jurisdiction_ids))

            # Get the profile
            print('\nCalling MRAS Profile API using [corp_num: {corp_num}], [province: {province}]'.format(corp_num=corp_num, province=province))
            mras_url = MRAS_SVC_PROFILE_URL.format(profile_id=corp_num, source_jurisdiction_id=province)
            headers = {
                'x-api-key': MRAS_SVC_API_KEY,
                'Accept': 'application/xml'
            }

            print(mras_url)
            print(repr(headers))
            response = requests.get(
                mras_url,
                headers=headers
            )

            # Return the auth response if an error occurs
            if not response.status_code == 200:
                mras_errors = load_xml_response_content(response, './/mras_error')
                mras_error = {
                    'error_code': mras_errors[0].find('error_code').text,
                    'internal_error_code': mras_errors[0].find('internal_error_code').text,
                    'internal_error_message': mras_errors[0].find('internal_error_message').text
                }

                raise MrasServiceException(mras_error=mras_error)

            # Just return true or false, the profile either exists or it doesn't
            return jsonify(response), 200
        except MrasServiceException as err:
            return handle_exception(err, err.message, err.error_code)
        except Exception as err:
            return handle_exception(err, 'Internal Server Error', 500)
