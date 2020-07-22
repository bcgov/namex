import re
from sqlalchemy import func

from flask import request, jsonify, current_app
from flask_restplus import Namespace, Resource, fields, cors

from namex.utils.logging import setup_logging
from namex.utils.util import cors_preflight

from namex.models import Request, Event, State, Applicant
from namex.criteria.request import RequestQueryCriteria

from namex.services import EventRecorder

from namex.services.name_request.utils import handle_exception, get_query_param_str, normalize_nr_num
from namex.services.name_request.exceptions import *
from namex.services.name_request import NameRequestService

setup_logging()  # Important to do this first

SOLR_CORE = 'possible.conflicts'

# Register a local namespace for the NR reserve
api = Namespace('nameRequests', description='Public facing Name Requests')

applicant_model = api.model('applicant_model', {
    'partyId': fields.Integer('partyId'),
    'lastName': fields.String(attribute='lastName'),
    'firstName': fields.String(attribute='firstName'),
    'middleName': fields.String('Applicant middle name or initial'),
    'contact': fields.String('Applicant contact person last and first name'),
    'clientFirstName': fields.String('Client first name'),
    'clientLastName': fields.String('Client last name'),
    'phoneNumber': fields.String('Contact phone number'),
    'faxNumber': fields.String('Contact fax number'),
    'emailAddress': fields.String('Contact email'),
    'addrLine1': fields.String('First address line'),
    'addrLine2': fields.String('Second address line'),
    'city': fields.String('City'),
    'stateProvinceCd': fields.String('Province or state code'),
    'postalCd': fields.String('Postal code or zip code'),
    'countryTypeCd': fields.String('Country code')
})

consent_model = api.model('consent_model', {
    'consent_word': fields.String('A word that requires consent')
})

name_model = api.model('name_model', {
    'id': fields.Integer('id'),
    'choice': fields.Integer('Name choice'),
    'name': fields.String('Name'),
    'name_type_cd': fields.String('For company or assumed name', enum=['CO', 'AS']),
    'state': fields.String('The state of the Name'),
    'designation': fields.String('Name designation based on entity type'),
    'conflict1_num': fields.String('The corp_num of the matching name'),
    'conflict1': fields.String('The matching corp name'),
    'consent_words': fields.Nested(consent_model)
})

nr_request = api.model('name_request', {
    'id': fields.Integer('id'),
    'nrNum': fields.Integer('nrNum'),
    'entity_type': fields.String('The entity type'),
    'request_action': fields.String('The action requested by the user'),
    'stateCd': fields.String('The state of the NR'),
    'english': fields.Boolean('Set when the name is English only'),
    'nameFlag': fields.Boolean('Set when the name is a person'),
    'additionalInfo': fields.String('Additional NR Info'),
    'natureBusinessInfo': fields.String('The nature of business'),
    'tradeMark': fields.String('Registered Trademark'),
    'previousRequestId': fields.Integer('Internal Id for Re-Applys'),
    'priorityCd': fields.String('Set to Yes if it is  priority going to examination'),
    'submit_count': fields.Integer('Used to enforce the 3 times only rule for Re-Applys'),
    'xproJurisdiction': fields.String('The province or country code for XPRO requests'),
    'homeJurisNum': fields.String('For MRAS participants, their home jurisdiction corp_num'),
    'corpNum': fields.String('For companies already registered in BC, their BC corp_num'),
    'applicants': fields.Nested(applicant_model),
    'names': fields.Nested(name_model)
})


def parse_nr_num(nr_num_str):
    nr_num = normalize_nr_num(nr_num_str) if nr_num_str else None
    if nr_num_str and not nr_num:
        raise InvalidInputError(message='Invalid NR number format provided')

    return nr_num


class AbstractNameRequestResource(Resource):
    _nr_service = None

    @property
    def nr_service(self):
        return self._service

    @nr_service.setter
    def nr_service(self, service):
        self._nr_service = service

    def _initialize(self):
        self.nr_service = NameRequestService()

        self._validate_config(current_app)

        self.request_data = request.get_json()
        if not self.request_data:
            self.log_error('Error getting json input.', None)
            raise InvalidInputError()

    @classmethod
    def _validate_config(cls, app):
        app_config = app.config.get('SOLR_SYNONYMS_API_URL', None)
        if not app_config:
            cls.log_error('ENV is not set', None)
            raise Exception('Internal server error')

        test_env = 'prod'
        if test_env in app_config:
            return NotImplementedError()

    @staticmethod
    def log_error(msg, err):
        return msg.format(err)


@cors_preflight('GET, POST')
@api.route('/', strict_slashes=False, methods=['GET', 'POST', 'OPTIONS'])
class NameRequests(AbstractNameRequestResource):
    @cors.crossdomain(origin='*')
    @api.doc(params={
        'nrNum': 'NR Number - This field is required',
        'emailAddress': 'The applicant\'s email address - an emailAddress or a phoneNumber is required',
        'phoneNumber': 'The applicant\'s phone number - a phoneNumber or an emailAddress is required',
        # 'addrLine1': 'The applicant\'s address - optional'
    })
    def get(self):
        try:
            filters = []

            # Validate the request
            if len(request.args) == 0:
                raise InvalidInputError(message='No query parameters were specified in the request')

            nr_num_query_str = get_query_param_str('nrNum')
            email_address_query_str = get_query_param_str('emailAddress')
            phone_number_query_str = get_query_param_str('phoneNumber')

            if not nr_num_query_str:
                raise InvalidInputError(message='An nrNum must be provided')
            else:
                if not email_address_query_str and not phone_number_query_str:
                    raise InvalidInputError(message='Either an emailAddress or phoneNumber must be provided')

            # Continue
            nr_num = parse_nr_num(nr_num_query_str)
            email_address = email_address_query_str

            phone_number = get_query_param_str('phoneNumber')
            # Filter on addresses
            # address_line = get_query_param_str('addrLine1')

            if nr_num:
                filters.append(func.lower(Request.nrNum) == nr_num.lower())
            if phone_number:
                strip_phone_number_chars_regex = r"[^0-9]"
                filters.append(
                    Request.applicants.any(
                        func.regexp_replace(Applicant.phoneNumber, strip_phone_number_chars_regex, '', 'g').contains(re.sub(strip_phone_number_chars_regex, '', phone_number))
                    )
                )

            if email_address:
                filters.append(
                    Request.applicants.any(
                        func.lower(Applicant.emailAddress).startswith(email_address.lower())
                    )
                )

            '''
            Filter on addresses
            if address_line:
                filters.append(
                    Request.applicants.any(
                        func.lower(Applicant.addrLine1).startswith(address_line.lower())
                    )
                )
            '''

            criteria = RequestQueryCriteria(
                nr_num=nr_num,
                filters=filters
            )

            results = Request.find_by_criteria(criteria)

            if not results:
                results = []

        except InvalidInputError as err:
            return handle_exception(err, err.message, 400)
        except Exception as err:
            return handle_exception(err, 'Error retrieving the NR from the db.', 500)

        if nr_num and len(results) == 1:
            return jsonify(results[0].json()), 200
        elif len(results) > 0:
            return jsonify(list(map(lambda result: result.json(), results))), 200

        return jsonify(results), 200

    @api.expect(nr_request)
    @cors.crossdomain(origin='*')
    def post(self):
        try:
            self._initialize()
            nr_svc = self.nr_service

            # Create a new DRAFT name request
            nr_model = self.create_name_request()

            def handle_name_request_creation(nr, svc):
                """
                All logic for creating the name request goes inside this handler, which is invoked on successful state change.
                :param nr: The name request model
                :param svc A reference to the current Resource instance (this controller)
                """
                # Map the request data and save so we have a name request ID to use for collection ops
                nr = svc.map_request_data(nr, True)  # Set map_draft_attrs to True
                nr = svc.save_request(nr)
                # Map applicants from the request data to the name request
                nr = svc.map_request_applicants(nr)
                # Map any submitted names from the request data to the name request
                nr = svc.map_request_names(nr)
                # Save
                nr = svc.save_request(nr)
                # Return the updated name request
                return nr

            # Handle state changes
            # Use apply_state_change to change state, as it enforces the State change pattern

            # Transition the DRAFT to the state specified in the request:
            # eg. one of [State.DRAFT, State.COND_RESERVE, State.RESERVED]
            nr_model = nr_svc.apply_state_change(nr_model, nr_svc.request_state_code, handle_name_request_creation)

            # Record the event
            EventRecorder.record(nr_svc.user, Event.POST, nr_model, nr_svc.request_data)

            # Update Solr - note that we don't save DRAFT name requests to Solr
            if nr_model.stateCd in [State.COND_RESERVE, State.RESERVED]:
                nr_svc.create_solr_nr_doc(SOLR_CORE, nr_model)

            current_app.logger.debug(nr_model.json())
            return jsonify(nr_model.json()), 200
        except NameRequestException as err:
            return handle_exception(err, err.message, 500)


@cors_preflight('GET, PUT')
@api.route('/<string:nr_num>', strict_slashes=False, methods=['GET', 'PUT', 'OPTIONS'])
class NameRequest(AbstractNameRequestResource):
    @cors.crossdomain(origin='*')
    def get(self, nr_num):
        try:
            nr_num = parse_nr_num(nr_num)
            name_request = Request.find_by_nr(nr_num)
        except Exception as err:
            return handle_exception(err, 'Error retrieving the NR from the db.', 500)

        return jsonify(name_request.json()), 200

    # REST Method Handlers
    @api.expect(nr_request)
    @cors.crossdomain(origin='*')
    def put(self, nr_num):
        try:
            self._initialize()
            nr_svc = self.nr_service

            # Find the existing name request
            nr_num = parse_nr_num(nr_num)
            nr_model = Request.find_by_nr(nr_num)
            nr_svc.nr_num = nr_model.nrNum
            nr_svc.nr_id = nr_model.id

            # Declare our update handlers functions

            def handle_name_request_update(nr, svc):
                """
                Logic for updating the name request DATA goes inside this handler, which is invoked on successful state change.
                :param nr: The name request model
                :param svc A reference to the current Resource instance (this controller)
                :return:
                """
                nr = svc.map_request_data(nr, False)
                # Map applicants from the request data to the name request
                nr = svc.map_request_applicants(nr)
                # Map any submitted names from the request data to the name request
                nr = svc.map_request_names(nr)
                # Save
                nr = svc.save_request(nr)
                # Return the updated name request
                return nr

            def handle_name_request_approval(nr, svc):
                """
                This method is for updating certain parts of the name request eg. its STATE when a payment token is present in the request.
                :param nr:
                :param svc:
                :return:
                """
                # Update the names, we can ignore everything else as this is only
                # invoked when we're completing a payment.
                nr = svc.map_request_names(nr)
                nr = svc.save_request(nr)
                # Return the updated name request
                return nr

            def on_nro_save_success(nr, svc):
                """
                :param nr:
                :param svc:
                :return:
                """

                nr = svc.save_request(nr)
                # Return the updated name request
                return nr

            # Handle state changes
            # Use apply_state_change to change state, as it enforces the State change pattern

            """
            This is the handler for a regular PUT from the frontend.
            """
            # If no payment token...
            if nr_model.payment_token is None and nr_model.stateCd in [State.DRAFT, State.COND_RESERVE, State.RESERVED]:
                # apply_state_change takes the model, updates it to the specified state, and executes the callback handler
                nr_model = nr_svc.apply_state_change(nr_model, nr_model.stateCd, handle_name_request_update)

            """
            This is the handler for a special PUT case where a payment has been received 
            and we need to APPROVE or CONDITIONALLY APPROVE a name request:
            1. When the payment ID is set, check to see if we need to update the entity state.
            2a. If the entity is in a COND_RESERVE state, update its state to CONDITIONAL.   
            2b. If the entity is in a RESERVED state, update its state to APPROVED.
            3. Execute the callback handler (do any custom update logic and save the name request here).
            """
            # If the state is COND_RESERVE update state to CONDITIONAL, and update the name request as required
            if nr_model.payment_token and nr_model.stateCd == State.COND_RESERVE:
                # apply_state_change takes the model, updates it to the specified state, and executes the callback handler
                nr_model = nr_svc.apply_state_change(nr_model, State.CONDITIONAL, handle_name_request_approval)
                # If the state is RESERVED update state to APPROVED, and update the name request as required
            elif nr_model.payment_token and nr_model.stateCd == State.RESERVED:
                # apply_state_change takes the model, updates it to the specified state, and executes the callback handler
                nr_model = nr_svc.apply_state_change(nr_model, State.APPROVED, handle_name_request_approval)

            temp_nr_num = None
            # Save the request to NRO and back to postgres ONLY if the state is DRAFT, CONDITIONAL, or APPROVED
            # this is after fees are accepted
            if nr_model.stateCd in [State.DRAFT, State.CONDITIONAL, State.APPROVED]:
                existing_nr_num = nr_model.nrNum
                # This updates NRO, it should return the nr_model with the updated nrNum, which we save back to postgres in the on_nro_save_success handler
                nr_model = nr_svc.save_request_to_nro(nr_model, on_nro_save_success)
                # Set the temp NR number if its different
                if nr_model.nrNum != existing_nr_num:
                    temp_nr_num = existing_nr_num

            # Record the event
            EventRecorder.record(nr_svc.user, Event.PUT, nr_model, nr_svc.request_data)

            # Update SOLR
            if nr_model.stateCd in [State.COND_RESERVE, State.RESERVED, State.CONDITIONAL, State.APPROVED]:
                nr_svc.create_solr_nr_doc(SOLR_CORE, nr_model)
                if temp_nr_num:
                    # This performs a safe delete, we check to see if the temp ID exists before deleting
                    nr_svc.delete_solr_doc(SOLR_CORE, temp_nr_num)

            current_app.logger.debug(nr_model.json())
            return jsonify(nr_model.json()), 200
        except NameRequestException as err:
            return handle_exception(err, err.message, 500)
