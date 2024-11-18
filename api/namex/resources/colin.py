from http import HTTPStatus
import json

import requests
from flask import current_app, jsonify, make_response
from flask_restx import Namespace, Resource, cors
from namex.exceptions import EntityServiceException

from namex.utils.api_resource import handle_exception
from namex.utils.auth import MSG_CLIENT_CREDENTIALS_REQ_FAILED, cors_preflight
from namex.utils.logging import setup_logging
from .utils import EntityUtils


setup_logging()  # Important to do this first

MSG_BAD_REQUEST_NO_JSON_BODY = 'No JSON data provided'
MSG_SERVER_ERROR = 'Server Error!'
MSG_NOT_FOUND = 'Resource not found'
MSG_COULD_NOT_FIND_CORP = 'Error: Could not find corporation details'


# Register a local namespace for the NR reserve
colin_api = Namespace('colin', description='COLIN API')

@cors_preflight('GET')
@colin_api.route('/<string:corp_num>', strict_slashes=False, methods=['GET', 'OPTIONS'])
@colin_api.doc(params={
    'corp_num': 'Incorporation Number - This field is required'
})
class ColinApi(Resource):
    def get(self, corp_num):
        """
        Handles GET requests to retrieve business, office, and parties data for a given corporation number.

        Args:
            corp_num (str): The corporation number.

        Returns:
            Response: A Flask response object with the business data in JSON format.
        """
        try:
            # Build the Colin public endpoint URL
            colin_url = f'{current_app.config.get("COLIN_SVC_URL")}/businesses/{corp_num}/public'
            # Fetch the business information
            response = EntityUtils.make_authenticated_request(colin_url)

            if response.status_code != HTTPStatus.OK:
                error_message = f"Error retrieving {corp_num}: "

                # If response is JSON, modify the JSON object
                response_body = response.json()
                if isinstance(response_body, dict):
                    response_body['error'] = error_message + response_body.get('message', 'Unknown error')
                else:
                    # Handle cases where the JSON response is not a dictionary
                    response_body = {'error': error_message + str(response_body)}
                return make_response(jsonify(response_body), response.status_code)
            
            business_info = response.json().get('business', {})
            legal_type = business_info.get('legalType')

            # Fetch office and parties information
            office_info = self._get_office_data(corp_num, legal_type)
            parties_info = self._get_parties_data(corp_num, legal_type)

            # Construct the response dictionary
            response_dict = {
                'identifier': business_info.get('identifier', corp_num),
                'legalName': business_info.get('legalName'),
                'legalType': legal_type,
                'corpState': business_info.get('corpStateClass'),
                'status': business_info.get('status'),
                'jurisdiction': business_info.get('jurisdiction'),
                'homeIdentifier': business_info.get('homeJurisdictionNumber'),
                'registeredOfficeDeliveryAddress': office_info.get('registered', []),
                'recordsOfficeDeliveryAddress': office_info.get('records', []),
                'directors': parties_info
            }

            # Return the response as JSON
            return make_response(jsonify(response_dict), 200)

        except ValueError as ve:
            current_app.logger.error(f"ValueError: {ve}")
            return handle_exception(ve, 'Invalid Request', 400)

        except Exception as err:
            current_app.logger.error(f"Unexpected error: {err}")
            return handle_exception(err, 'Internal Server Error', 500)


    def _get_office_data(self, corp_num, legal_type):
        """
        Process the office data for a given corporation number.

        Args:
            corp_num (str): The corporation number.
            legal_type (str): the legal type

        Returns:
            dict: A dictionary containing address components for registered and records offices.
                If an office type is missing, its value will be an empty list.
        """
        try:
            # Build the Colin service endpoint
            colin_service_url = f'{current_app.config.get("COLIN_SVC_URL")}'
            office_endpoint = f'{colin_service_url}/businesses/{legal_type}/{corp_num}/office'

            # Make the authenticated request
            response = EntityUtils.make_authenticated_request(office_endpoint)
            if response.status_code != HTTPStatus.OK:
                office_data = {}
            else:
                office_data = response.json()

            # Helper function to extract and format address
            def extract_address(office_type):
                address = office_data.get(office_type, {}).get("deliveryAddress", {})
                return [
                    address.get("streetAddress", "").strip(),
                    address.get("streetAddressAdditional", "").strip(),
                    address.get("addressCity", "").strip(),
                    address.get("addressRegion", "").strip(),
                    address.get("postalCode", "").strip(),
                    address.get("addressCountry", "").strip()
                ] if address else []

            # Return formatted addresses
            return {
                'registered': extract_address("registeredOffice"),
                'records': extract_address("recordsOffice")
            }

        except Exception as e:
            current_app.logger.error(f"Error while processing office data for {corp_num}: {e}")
            raise ValueError(f"Failed to retrieve or process office data for {corp_num}: {e}")

    def _get_parties_data(self, corp_num, legal_type):
        """
        Process the parties data for a given corporation number.

        Args:
            corp_num (str): The corporation number.
            legal_type (str): The legal type.

        Returns:
            list: A list of director names in the format "FirstName MiddleInitial LastName".
        """
        try:
            # Build the Colin service endpoint
            colin_service_url = f'{current_app.config.get("COLIN_SVC_URL")}'
            parties_endpoint = f"{colin_service_url}/businesses/{legal_type}/{corp_num}/parties"

            # Make the authenticated request
            response = EntityUtils.make_authenticated_request(parties_endpoint)
            parties_data = {}
            if response.status_code == HTTPStatus.OK:
                parties_data = response.json()

            # Log the received data for debugging
            current_app.logger.debug(f"Processing parties data for corporation number {corp_num}: {parties_data}")

            # Extract director names
            def extract_director_name(director):
                officer = director.get("officer", {})
                first_name = officer.get("firstName", "").strip()
                middle_initial = officer.get("middleInitial", "").strip()
                last_name = officer.get("lastName", "").strip()
                return f"{first_name} {middle_initial} {last_name}".strip()

            directors = []
            for director in parties_data.get("directors", []):
                directors.append(extract_director_name(director))
            return directors

        except Exception as e:
            current_app.logger.error(f"Error while processing parties data for {corp_num}: {e}")
            raise ValueError(f"Failed to retrieve or process parties data for {corp_num}: {e}")

