from http import HTTPStatus

from flask import current_app, jsonify, make_response
from flask_restx import Namespace, Resource

from namex.models.request import Request
from namex.utils.api_resource import handle_exception
from namex.utils.auth import cors_preflight

from .utils import EntityUtils

MSG_BAD_REQUEST_NO_JSON_BODY = 'No JSON data provided'
MSG_SERVER_ERROR = 'Server Error!'
MSG_NOT_FOUND = 'Resource not found'
MSG_COULD_NOT_FIND_CORP = 'Error: Could not find corporation details'


# Register a local namespace for the NR reserve
colin_api = Namespace('Colin Info', description='Fetch business, office, and party details from Corporate Online (Colin)')


@cors_preflight('GET')
@colin_api.route('/<string:corp_num>', strict_slashes=False, methods=['GET', 'OPTIONS'])
@colin_api.doc(
    description='Fetch Colin business data including legal name, status, offices, and directors/attorneys',
    params={'corp_num': 'Incorporation number of the business'},
    responses={
        200: 'Business data fetched successfully',
        404: 'Business not found or Colin returned an error',
        500: 'Internal server error',
    },
)
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
                error_message = f'Error retrieving {corp_num}: '

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

            # Fetch nature business info
            nature_business_info = self._get_nature_of_business(corp_num)

            # Construct the response dictionary
            response_dict = {
                'identifier': business_info.get('identifier', corp_num),
                'incorporated': business_info.get('foundingDate'),
                'legalName': business_info.get('legalName'),
                'legalType': legal_type,
                'corpState': business_info.get('corpStateClass'),
                'status': business_info.get('status'),
                'jurisdiction': business_info.get('jurisdiction'),
                'homeIdentifier': business_info.get('homeJurisdictionNumber'),
                'registered office delivery address': office_info.get('registeredOffice', []),
                'records office delivery address': office_info.get('recordsOffice', []),
                'head office': office_info.get('headOffice', []),
                'directors': parties_info.get('directorNames'),
                'attorney names': parties_info.get('attorneyNames'),
                'nature of business': nature_business_info,
            }

            # Return the response as JSON
            return make_response(jsonify(response_dict), 200)

        except ValueError as ve:
            current_app.logger.error(f'ValueError: {ve}')
            return handle_exception(ve, 'Invalid Request', 400)

        except Exception as err:
            current_app.logger.error(f'Unexpected error: {err}')
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
                address = office_data.get(office_type, {}).get('deliveryAddress', {})
                return (
                    [
                        (address.get('streetAddress') or '').strip(),
                        (address.get('streetAddressAdditional') or '').strip(),
                        (address.get('addressCity') or '').strip(),
                        (address.get('addressRegion') or '').strip(),
                        (address.get('postalCode') or '').strip(),
                        (address.get('addressCountry') or '').strip(),
                    ]
                    if address
                    else []
                )

            # Return formatted addresses
            return {
                'registeredOffice': extract_address('registeredOffice'),
                'recordsOffice': extract_address('recordsOffice'),
                'headOffice': extract_address('headOffice'),  # head office for xpro companies
            }

        except Exception as e:
            current_app.logger.error(f'Error while processing office data for {corp_num}: {e}')
            raise ValueError(f'Failed to retrieve or process office data for {corp_num}: {e}')

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
            parties_endpoint = f'{colin_service_url}/businesses/{legal_type}/{corp_num}/parties/all'

            # Make the authenticated request
            response = EntityUtils.make_authenticated_request(parties_endpoint)
            parties_data = {}
            if response.status_code == HTTPStatus.OK:
                parties_data = response.json()

            # Log the received data for debugging
            current_app.logger.debug(f'Processing parties data for corporation number {corp_num}: {parties_data}')

            # Helper function to extract names for a specific role
            def extract_names(party_list, role_type):
                # Return an empty list immediately if the party_list is empty
                if not party_list:
                    return []

                names = []
                for party in party_list:
                    roles = party.get('roles', [])
                    if any(role.get('roleType') == role_type for role in roles):
                        officer = party.get('officer') or {}
                        first_name = (officer.get('firstName') or '').strip()
                        middle_initial = (officer.get('middleInitial') or '').strip()
                        last_name = (officer.get('lastName') or '').strip()
                        full_name = f'{first_name} {middle_initial} {last_name}'.strip()
                        names.append(full_name)
                return names

            # Extract names for the directoires, if it is a BC company
            role = 'Director'
            party_list = parties_data.get('parties', [])
            director_names = extract_names(party_list, role)

            # extract names for Attorneys, if it is a xpro corp
            role = 'Attorney'
            attorney_names = extract_names(party_list, role)

            return {'directorNames': director_names, 'attorneyNames': attorney_names}
        except Exception as e:
            current_app.logger.error(f'Error while processing parties data for {corp_num}: {e}')
            raise ValueError(f'Failed to retrieve or process parties data for {corp_num}: {e}')

    def _get_nature_of_business(self, corp_num):
        return Request.get_nature_business_info(corp_num)
