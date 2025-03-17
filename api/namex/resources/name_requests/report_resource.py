import base64
from http import HTTPStatus
import json
from datetime import datetime
from pathlib import Path
import pycountry
from pytz import timezone

import requests
from flask import current_app, jsonify, request, make_response
from flask_restx import Resource
from gcp_queue.logging import structured_log

from namex.constants import RequestAction
from namex.models import Request, State
from namex.utils.api_resource import handle_exception
from namex.utils.auth import cors_preflight, full_access_to_name_request
from namex.utils.logging import setup_logging
from namex.services.name_request import NameRequestService
from namex.services.name_request.utils import get_mapped_entity_and_action_code
from namex.utils.auth import get_client_credentials
from .api_namespace import api
from ..utils import EntityUtils

setup_logging()  # Important to do this first

DATE_FORMAT = '%B %-d, %Y at %-I:%M %p Pacific time'

@cors_preflight('GET')
@api.route('/<int:nr_id>/result', strict_slashes=False, methods=['GET', 'OPTIONS'])
@api.doc(params={
    'nr_id': 'NR ID - This field is required'
})
class ReportResource(Resource):

    EX_COOP_ASSOC = 'Extraprovincial Cooperative Association'
    GENERIC_STEPS = 'Submit appropriate form to BC Registries. Call if assistance required'
    BCA = 'Business Corporations Act'
    PA = 'Partnership Act'


    def get(self, nr_id):
        try:
            if not full_access_to_name_request(request):
                return {"message": "You do not have access to this NameRequest."}, 403
            nr_model = Request.query.get(nr_id)
            if not nr_model:
                return make_response(jsonify(message='{nr_id} not found'.format(nr_id=nr_model.id)), HTTPStatus.NOT_FOUND)
            nr_json = nr_model.json()
            resp = ReportResource._get_report(nr_json)
            response = make_response(resp)
            response.mimetype = "application/octet-stream"
            return response
        except Exception as err:
            return handle_exception(err, 'Error retrieving the report.', 500)

    @staticmethod
    def _get_report(nr_model):
        if nr_model['stateCd'] not in [State.APPROVED, State.CONDITIONAL,
                                    State.CONSUMED, State.EXPIRED, State.REJECTED]:
            return make_response(jsonify(message='Invalid NR state'.format(nr_id=nr_model['id'])), HTTPStatus.BAD_REQUEST)

        authenticated, token = ReportResource._get_service_client_token()
        if not authenticated:
            return make_response(jsonify(message='Error in authentication'.format(nr_id=nr_model['id'])),\
                    HTTPStatus.INTERNAL_SERVER_ERROR)

        headers = {
            'Authorization': 'Bearer {}'.format(token),
            'Content-Type': 'application/json'
        }
        data = {
            'reportName': ReportResource._get_report_filename(nr_model),
            'template': "'" + base64.b64encode(bytes(ReportResource._get_template(), 'utf-8')).decode() + "'",
            'templateVars': ReportResource._get_template_data(nr_model)
        }
        response = requests.post(url=current_app.config.get('REPORT_SVC_URL'), headers=headers,
                                    data=json.dumps(data))

        if response.status_code != HTTPStatus.OK:
            return make_response(jsonify(message=str(response.content)), response.status_code)
        return response.content, response.status_code

    @staticmethod
    def _get_report_filename(nr_model):
        return 'NR {}.pdf'.format(nr_model['nrNum']).replace(' ', '_')

    @staticmethod
    def _get_template():
        try:
            template_path = current_app.config.get('REPORT_TEMPLATE_PATH')
            template_code = Path(f'{template_path}/{ReportResource._get_template_filename()}').read_text()
            template_code = ReportResource._substitute_template_parts(template_code)
        except Exception as err:
            current_app.logger.error(err)
            raise err
        return template_code

    @staticmethod
    def _get_template_filename():
        return 'nameRequest.html'


    @staticmethod
    def _add_expiry_date(nr_model):
        nr_service = NameRequestService()
        expiry_days = nr_service.get_expiry_days(nr_model['request_action_cd'], nr_model['requestTypeCd'])
        expiry_date = nr_service.create_expiry_date(
            start= datetime.fromisoformat(nr_model['lastUpdate']).replace(tzinfo=timezone('UTC')),
            expires_in_days=expiry_days
        )
        nr_model['expirationDate'] = expiry_date


    @staticmethod
    def _substitute_template_parts(template_code):
        template_path = current_app.config.get('REPORT_TEMPLATE_PATH')
        template_parts = [
            'name-request/style',
            'name-request/logo',
            'name-request/nrDetails',
            'name-request/nameChoices',
            'name-request/applicantContactInfo',
            'name-request/resultDetails'
        ]
        # substitute template parts - marked up by [[filename]]
        for template_part in template_parts:
            template_part_code = Path(f'{template_path}/template-parts/{template_part}.html').read_text()
            template_code = template_code.replace('[[{}.html]]'.format(template_part), template_part_code)

        return template_code
    
    @staticmethod
    def _update_entity_and_action_code(nr_model):
        if nr_model['requestTypeCd'] and (not nr_model['entity_type_cd'] or not nr_model['request_action_cd']):
            # For the NRO ones.
            entity_type, request_action = get_mapped_entity_and_action_code(nr_model['requestTypeCd'])
            nr_model['entity_type_cd'] = entity_type
            nr_model['request_action_cd'] = request_action

    @staticmethod
    def _get_template_data(nr_model):
        ReportResource._update_entity_and_action_code(nr_model)
        nr_report_json = nr_model
        nr_report_json['service_url'] = current_app.config.get('NAME_REQUEST_URL')
        nr_report_json['entityTypeDescription'] = ReportResource._get_entity_type_description(nr_model['entity_type_cd'])
        nr_report_json['legalAct'] = ReportResource._get_legal_act(nr_model['entity_type_cd'])
        isXPRO = nr_model['entity_type_cd'] in ['XCR', 'XUL', 'RLC', 'XLP', 'XLL', 'XCP', 'XSO']
        nr_report_json['isXPRO'] = isXPRO
        instruction_group = ReportResource._get_instruction_group(nr_model['entity_type_cd'], nr_model['request_action_cd'], nr_model['corpNum'])
        nr_report_json['isModernized'] = True if instruction_group == 'modernized' else False
        nr_report_json['isColin'] = True if instruction_group == 'colin' else False
        nr_report_json['isSociety'] = True if instruction_group == 'so' else False
        nr_report_json['isNew'] = True if instruction_group == 'new' else False
        nr_report_json['isPaper'] = not (ReportResource._is_colin(nr_model['entity_type_cd']) or ReportResource._is_modernized(nr_model['entity_type_cd']) or ReportResource._is_society(nr_model['entity_type_cd']) or ReportResource._is_potential_colin(nr_model['entity_type_cd']))
        nr_report_json['requestCodeDescription'] = \
            ReportResource._get_request_action_cd_description(nr_report_json['request_action_cd'])
        nr_report_json['nrStateDescription'] = \
            ReportResource._get_state_cd_description(nr_report_json['stateCd'])
        if isXPRO and nr_report_json['nrStateDescription'] == 'Rejected':
            nr_report_json['nrStateDescription'] = 'Not Approved'
        if nr_report_json['expirationDate']:
            tz_aware_date = datetime.fromisoformat(nr_model['expirationDate']).replace(tzinfo=timezone('UTC'))
            localized_date = tz_aware_date.astimezone(timezone('US/Pacific'))
            nr_report_json['expirationDate'] = localized_date.strftime(DATE_FORMAT)
        else:
            ReportResource._add_expiry_date(nr_model)
            nr_report_json['expirationDate'] = nr_model['expirationDate'].strftime(DATE_FORMAT)
        if nr_report_json['submittedDate']:
            tz_aware_date = datetime.fromisoformat(nr_model['submittedDate']).replace(tzinfo=timezone('UTC'))
            localized_date = tz_aware_date.astimezone(timezone('US/Pacific'))
            nr_report_json['submittedDate'] = localized_date.strftime(DATE_FORMAT)
        if nr_report_json['applicants']['countryTypeCd']:
            nr_report_json['applicants']['countryName'] = \
                pycountry.countries.search_fuzzy(nr_report_json['applicants']['countryTypeCd'])[0].name
        action_url = ReportResource._get_action_url(nr_model['entity_type_cd'], instruction_group)
        actions_obj = ReportResource._get_next_action_text(nr_model['entity_type_cd'], action_url, instruction_group)
        if actions_obj:
            action_text = actions_obj.get(nr_report_json['request_action_cd'])
            if not action_text:
                action_text = actions_obj.get('DEFAULT')
            if action_text:
                nr_report_json['nextAction'] = action_text
        nr_report_json['retrievalDateTime'] = datetime.now().astimezone(timezone('US/Pacific')).strftime(DATE_FORMAT)

        nr_report_json['hasUnreviewedNames'] = ReportResource._hasUnReviewedNames(nr_report_json['names'])
        return nr_report_json


    @staticmethod
    def _hasUnReviewedNames(names):
        for choice in names:
            if choice['state'] not in ['REJECTED', 'APPROVED', 'CONDITION']:
                return True
        return False


    @staticmethod
    def _get_service_client_token():
        auth_url = current_app.config.get('PAYMENT_SVC_AUTH_URL')
        client_id = current_app.config.get('PAYMENT_SVC_AUTH_CLIENT_ID')
        secret = current_app.config.get('PAYMENT_SVC_CLIENT_SECRET')
        return get_client_credentials(auth_url, client_id, secret)


    @staticmethod
    def _get_request_action_cd_description(request_cd: str):
        request_cd_description = {
            'NEW': 'New Business Name',
            'MVE': 'Continuation in',
            'REH': 'Restoration or Reinstatement',
            'AML': 'Amalgamation',
            'NRO-NEWAML': 'Amalgamation',
            'CHG': 'Name Change',
            'CNV': 'Alteration',
            'NRO-REST': 'Restoration or Reinstatement'
        }

        return request_cd_description.get(request_cd, None)

    @staticmethod
    def _get_state_cd_description(state_cd: str):
        nr_state_description = {
            'APPROVED': 'Approved',
            'CONDITIONAL': 'Conditionally Approved',
            'REJECTED': 'Rejected',
            'CONSUMED': 'Consumed',
            'EXPIRED': 'Expired'
        }

        return nr_state_description.get(state_cd, None)

    @staticmethod
    def _get_entity_type_description(entity_type_cd: str):
        entity_type_descriptions = {
            # BC Types
            'CR': 'BC Limited Company',
            'UL': 'BC Unlimited Liability Company',
            'FR': 'BC Sole Proprietorship',
            'GP': 'BC General Partnership',
            'DBA': 'BC Doing Business As',
            'LP': 'BC Limited Partnership',
            'LL': 'BC Limited Liability Partnership',
            'CP': 'BC Cooperative Association',
            'BC': 'BC Benefit Company',
            'CC': 'BC Community Contribution Company',
            'SO': 'BC Society',
            'PA': 'BC Private Act',
            'FI': 'BC Credit Union',
            'PAR': 'BC Parish',
            # XPRO and Foreign Types
            'XCR': 'Extraprovincial Limited Company',
            'XUL': 'Extraprovincial Unlimited Liability Company',
            'RLC': 'Extraprovincial Limited Liability Company',
            'XLP': 'Extraprovincial Limited Partnership',
            'XLL': 'Extraprovincial Limited Liability Partnership',
            'XCP':  ReportResource.EX_COOP_ASSOC,
            'XSO': 'Extraprovincial Non-share Corporation',
            # Used for mapping back to legacy oracle codes, description not required
            'FIRM': 'FIRM (Legacy Oracle)'
        }
        return entity_type_descriptions.get(entity_type_cd, None)

    @staticmethod
    def _is_lear_entity(corpNum):
        if not corpNum:
            return False
        entity_url = f'{current_app.config.get("ENTITY_SVC_URL")}/businesses/{corpNum}'
        response = EntityUtils.make_authenticated_request(entity_url)
        if response.status_code == HTTPStatus.OK and response.json():
            return True
        return False
    
    @staticmethod
    def _is_modernized(legal_type):
        modernized_list = ['GP', 'DBA', 'FR', 'CP', 'BC']
        return legal_type in modernized_list

    @staticmethod
    def _is_colin(legal_type):
        colin_list = ['XCR', 'XUL', 'RLC', 'CR', 'UL', 'CC']
        return legal_type in colin_list
    
    @staticmethod
    def _is_society(legal_type):
        society_list = ['SO', 'XSO']
        return legal_type in society_list

    @staticmethod
    def _is_magic_link(legal_type, request_action):
        magic_link_list = {
            'NEW': ['CR', 'UL', 'CC'],
            'MVE': ['CR', 'UL', 'CC']
        }
        return legal_type in magic_link_list.get(request_action)

    @staticmethod
    def _get_instruction_group(legal_type, request_action, corpNum):
        email_feature_flags = ReportResource._get_email_feature_flags()
        structured_log(request, 'DEBUG', f'NR-Email: NameX API - Email Feature Flags: {email_feature_flags}')
        if request_action in {RequestAction.REH.value, RequestAction.REST.value}:
            return 'reh'
        if request_action in {RequestAction.CHG.value, RequestAction.CNV.value}:
            # For the 'Name Change' or 'Alteration', return 'modernized' if the company is in LEAR, and 'colin' if not
            return 'modernized' if ReportResource._is_lear_entity(corpNum) else 'colin'
        # Check for magic link conditions
        if ReportResource._is_magic_link(legal_type, request_action) and (
            (request_action == RequestAction.NEW.value and email_feature_flags.get('enable_won_emails')) or
            (request_action == RequestAction.MVE.value and email_feature_flags.get('enable_cont_in_emails'))
        ):
            return 'magic-link'
        if ReportResource._is_modernized(legal_type):
            return 'modernized'
        if ReportResource._is_colin(legal_type):
            return 'colin'
        if ReportResource._is_society(legal_type):
            return 'so'
        return ''

    @staticmethod
    def _get_action_url(entity_type_cd: str, instruction_group: str):

        DECIDE_BUSINESS_URL =  current_app.config.get('DECIDE_BUSINESS_URL')
        CORP_FORMS_URL =  current_app.config.get('CORP_FORMS_URL')
        BUSINESS_URL = current_app.config.get('BUSINESS_URL')
        CORP_ONLINE_URL = current_app.config.get('COLIN_URL')
        SOCIETIES_URL = current_app.config.get('SOCIETIES_URL')

        url = {
            # BC Types
            'CR':  BUSINESS_URL if instruction_group == 'modernized' else CORP_ONLINE_URL,
            'UL':  BUSINESS_URL if instruction_group == 'modernized' else CORP_ONLINE_URL,
            'FR':  DECIDE_BUSINESS_URL,
            'GP':  DECIDE_BUSINESS_URL,
            'DBA': DECIDE_BUSINESS_URL,
            'LP':  CORP_FORMS_URL,
            'LL':  CORP_FORMS_URL,
            'CP':  BUSINESS_URL,
            'BC':  BUSINESS_URL,
            'CC':  BUSINESS_URL if instruction_group == 'modernized' else CORP_ONLINE_URL,
            'SO':  SOCIETIES_URL,
            'PA': ReportResource.GENERIC_STEPS,
            'FI': ReportResource.GENERIC_STEPS,
            'PAR': ReportResource.GENERIC_STEPS,
            # XPRO and Foreign Types
            'XCR': CORP_ONLINE_URL,
            'XUL': CORP_ONLINE_URL,
            'RLC': CORP_ONLINE_URL,
            'XLP': CORP_FORMS_URL,
            'XLL': CORP_FORMS_URL,
            'XCP': ReportResource.EX_COOP_ASSOC,
            'XSO': SOCIETIES_URL,
        }
        return url.get(entity_type_cd, None)

    @staticmethod
    def _get_legal_act(entity_type_cd: str):

        next_action_text = {
            # BC Types
            'CR':  ReportResource.BCA,
            'UL':  ReportResource.BCA,
            'FR':  ReportResource.PA,
            'GP':  ReportResource.PA,
            'DBA': ReportResource.PA,
            'LP':  ReportResource.PA,
            'LL':  ReportResource.PA,
            'CP':  'Cooperative Association Act',
            'BC':  ReportResource.BCA,
            'CC':  ReportResource.BCA,
            'SO':  'Society Act',
            'PA':  'Individual Acts',
            'FI':  'Credit Union Incorporation Act',
            'PAR': 'Trustee (Church Property) Act',
            # XPRO and Foreign Types
            'XCR': ReportResource.BCA,
            'XUL': ReportResource.BCA,
            'RLC': ReportResource.BCA,
            'XLP': ReportResource.PA,
            'XLL': ReportResource.PA,
            'XCP': 'Cooperative Association Act',
            'XSO': 'Society Act',
        }
        return next_action_text.get(entity_type_cd, None)

    @staticmethod
    def _get_next_action_text(entity_type_cd: str, url: str, instruction_group: str):

        BUSINESS_CHANGES_URL =  current_app.config.get('BUSINESS_CHANGES_URL')
        STEPS_TO_RESTORE_URL =  current_app.config.get('STEPS_TO_RESTORE_URL')

        next_action_text = {
            # BC Types
            'CR':  {
               'DEFAULT': f'Use this name request to complete your application by visiting <a href="{url}">'
                          f'{url}</a>'
            },
            'UL': {
               'DEFAULT': f'Use this name request to complete your application by visiting <a href="{url}">'
                          f'{url}</a>'
            },
            'FR': {
               'NEW': f'Use this name request to complete your application by visiting <a href="{url}">'
                        'Registering Proprietorships and Partnerships</a>',
               'DEFAULT': f'Use this name request to complete your application by visiting <a href="{url}">'
                          'Registering Proprietorships and Partnerships</a> for more information. To learn more, visit '
                          f'<a href="{BUSINESS_CHANGES_URL}">Making Changes to your Proprietorship or'
                          ' Partnership</a>'
            },
            'GP': {
               'NEW': f'Use this name request to complete your application by visiting <a href="{url}">'
                        'BC Registries and Online Services</a>',
               'DEFAULT': f'Use this name request to complete your application by visiting <a href="{url}">'
                          'BC Registries and Online Services</a> for more information. To learn more, visit '
                          f'<a href="{BUSINESS_CHANGES_URL}">Making Changes to your Proprietorship or'
                          ' Partnership</a>'
            },
            'DBA': {
               'NEW': f'Use this name request to complete your application by visiting <a href="{url}">'
                        'Registering Proprietorships and Partnerships</a>',
               'DEFAULT': f'Use this name request to complete your application by visiting <a href="{url}">'
                          'Registering Proprietorships and Partnerships</a> for more information. To learn more, visit '
                          f'<a href="{BUSINESS_CHANGES_URL}">Making Changes to your Proprietorship or'
                          ' Partnership</a>'
            },
            'LP': {
               'DEFAULT': f'Visit <a href= "{url}">Forms, fees and information packages page</a> and'
                          ' download the appropriate form'
            },
            'LL': {
               'DEFAULT': f'Visit <a href= "{url}">Forms, fees and information packages page</a> and'
                          ' download the appropriate form'
            },
            'CP': {
               'DEFAULT': f'Use this name request to complete your application by visiting <a href="{url}">{url}</a>'
            },
            'BC': {
               'DEFAULT': f'Use this name request to complete your application by visiting <a href="{url}">{url}</a>'
            },
            'CC': {
               'DEFAULT': f'Use this name request to complete your application by visiting <a href="{url}">'
                          f'{url}</a>'
            },
            'SO': {
               'DEFAULT': f'To complete your filing, visit <a href="{url}">'
                          f'{url}</a> and login with your BCeID.'
            },
            'PA': {
               'DEFAULT': ReportResource.GENERIC_STEPS
            },
            'FI': {
               'DEFAULT': ReportResource.GENERIC_STEPS
            },
            'PAR': {
               'DEFAULT': ReportResource.GENERIC_STEPS
            },
            # XPRO and Foreign Types
            'XCR': {
               'NEW': f'Use this name request to complete your application by visiting <a href="{url}">'
                      f'{url}</a>',
               'CHG': f'Use this name request to complete your application by visiting <a href="{url}">'
                      f'{url}</a>',
               'DEFAULT': f'To complete your filing, <a href= "{url}">visit our Forms page</a> to'
                          ' download and submit a form'
            },
            'XUL': {
               'DEFAULT': f'Use this name request to complete your application by visiting <a href="{url}">'
                          f'{url}</a>'
            },
            'RLC': {
                'DEFAULT': f'Use this name request to complete your application by visiting <a href="{url}">'
                          f'{url}</a>'
            },
            'XLP': {
               'DEFAULT': f'Visit <a href= "{url}">Forms, fees and information packages page</a> and'
                          ' download the appropriate form'
            },
            'XLL': {
               'DEFAULT': f'Visit <a href= "{url}">Forms, fees and information packages page</a> and'
                          ' download the appropriate form'
            },
            'XCP': {
                'DEFAULT': 'Extraprovincial Cooperative Association'
            },
            'XSO': {
                'DEFAULT': f'To complete your filing, visit <a href="{url}">'
                           f'{url}</a> and login with your BCeID.'
            },
            # Used for mapping back to legacy oracle codes, description not required
            'FIRM': {
                'DEFAULT': 'FIRM (Legacy Oracle)'
            }
        }

        # next action text by instruction group
        next_action_text_by_group = {
            'reh': {  # Restoration or Reinstatement
                'DEFAULT': f'To complete your application using this business name, choose the appropriate <a href="{STEPS_TO_RESTORE_URL}">'
                           f'information package</a> and submit the required forms to BC Registries.'
            },
            'magic-link': {
                'DEFAULT': 'Check your email for instructions on how to complete your application using this name request.'
            }
        }

        text = next_action_text_by_group.get(instruction_group, None)
        if text:
            return text

        return next_action_text.get(entity_type_cd, None)

    @staticmethod
    def _get_email_feature_flags():
        """Fetch email-related feature flags from the configuration service.

        Returns:
            dict[str, bool]: Dictionary of email feature flags.
        """
        from namex.services import flags  # pylint: disable=import-outside-toplevel
        return {
            'enable_won_emails': flags.value('enable-won-emails'),
            'enable_cont_in_emails': flags.value('enable-cont-in-emails'),
        }
