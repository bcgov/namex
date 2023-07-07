import base64
import json
import os
import pycountry
from http import HTTPStatus
from pathlib import Path

import requests
from flask import current_app, jsonify, request
from flask_restx import Resource, cors
from pytz import timezone

from namex.models import Request, State
from namex.utils.api_resource import handle_exception
from namex.utils.auth import cors_preflight, full_access_to_name_request
from namex.utils.logging import setup_logging
from .api_namespace import api
from namex.services.name_request.utils import get_mapped_entity_and_action_code
from namex.services.name_request import NameRequestService
from datetime import datetime

setup_logging()  # Important to do this first

RESULT_EMAIL_SUBJECT = 'Name Request Results from Corporate Registry'
CONSENT_EMAIL_SUBJECT = 'Consent Received by Corporate Registry'

@cors_preflight('GET')
@api.route('/<int:nr_id>/result', strict_slashes=False, methods=['GET', 'OPTIONS'])
@api.doc(params={
    'nr_id': 'NR ID - This field is required'
})
class ReportResource(Resource):
    def email_consent_letter(self, nr_id):
        try:
            nr_model = Request.query.get(nr_id)
            if not nr_model:
                return jsonify(message='{nr_id} not found'.format(nr_id=nr_model.id)), HTTPStatus.NOT_FOUND
            report_name = nr_model.nrNum + ' - ' + CONSENT_EMAIL_SUBJECT
            recepient_emails = []
            for applicant in nr_model.applicants:
                recepient_emails.append(applicant.emailAddress)
            if not nr_model.expirationDate:
                nr_service = NameRequestService()
                expiry_days = int(nr_service.get_expiry_days(nr_model))
                expiry_date = nr_service.create_expiry_date(
                    start=nr_model.lastUpdate,
                    expires_in_days=expiry_days
                )
                nr_model.expirationDate = expiry_date
            recepients = ','.join(recepient_emails)
            template_path = current_app.config.get('REPORT_TEMPLATE_PATH')
            email_body = Path(f'{template_path}/emails/consent.md').read_text()
            tz_aware_expiration_date = nr_model.expirationDate.replace(tzinfo=timezone('UTC'))
            localized_payment_completion_date = tz_aware_expiration_date.astimezone(timezone('US/Pacific'))
            email_body = email_body.replace('{{EXPIRATION_DATE}}', localized_payment_completion_date.strftime('%B %-d, %Y at %-I:%M %p Pacific time'))
            email_body = email_body.replace('{{NAMEREQUEST_NUMBER}}', nr_model.nrNum)
            email = {
                'recipients': recepients,
                'content': {
                    'subject': report_name,
                    'body': email_body,
                    'attachments': []
                }
            }
            return ReportResource._send_email(email)
        except Exception as err:
            return handle_exception(err, 'Error retrieving the report.', 500)

    def email_report(self, nr_id):
        try:
            nr_model = Request.query.get(nr_id)
            if not nr_model:
                return jsonify(message='{nr_id} not found'.format(nr_id=nr_model.id)), HTTPStatus.NOT_FOUND
            if not nr_model.expirationDate:
                nr_service = NameRequestService()
                expiry_days = int(nr_service.get_expiry_days(nr_model))
                expiry_date = nr_service.create_expiry_date(
                    start=nr_model.lastUpdate,
                    expires_in_days=expiry_days
                )
                nr_model.expirationDate = expiry_date
            report, status_code = ReportResource._get_report(nr_model)
            if status_code != HTTPStatus.OK:
                return jsonify(message=str(report)), status_code
            report_name = nr_model.nrNum + ' - ' + RESULT_EMAIL_SUBJECT
            recepient_emails = []
            for applicant in nr_model.applicants:
                recepient_emails.append(applicant.emailAddress)
            recepients = ','.join(recepient_emails)
            template_path = current_app.config.get('REPORT_TEMPLATE_PATH')
            nr_url = current_app.config.get('NAME_REQUEST_URL')
            email_body = Path(f'{template_path}/emails/rejected.md').read_text()
            if nr_model.stateCd in [State.APPROVED, State.CONDITIONAL]:
                email_body = Path(f'{template_path}/emails/approved.md').read_text()
                tz_aware_expiration_date = nr_model.expirationDate.replace(tzinfo=timezone('UTC'))
                localized_payment_completion_date = tz_aware_expiration_date.astimezone(timezone('US/Pacific'))
                email_body = email_body.replace('{{EXPIRATION_DATE}}', localized_payment_completion_date.strftime('%B %-d, %Y at %-I:%M %p Pacific time'))
                if nr_model.stateCd in [State.APPROVED]:
                    email_body = email_body.replace('{{APPROVAL_STATUS}}', 'approved')
                else:
                    email_body = email_body.replace('{{APPROVAL_STATUS}}', 'conditionally approved')

                action_url = ReportResource._get_action_url(nr_model.entity_type_cd)
                if 'https' in action_url:
                    email_body = email_body.replace('{{REGISTRATION_INSTRUCTIONS}}', f'[Register Now]({action_url})')
                else:
                    email_body = email_body.replace('{{REGISTRATION_INSTRUCTIONS}}', action_url)

                LIST_STEPS = ''
                if nr_model.consentFlag in ['Y', 'R']:
                    LIST_STEPS += '* Send in your consent letter to BCregistries@gov.bc.ca \n\n'
                    LIST_STEPS += '* Receive confirmation that the consent letter has been accepted \n\n'

                LIST_STEPS += '* Use this name request to register the business \n\n'
                email_body = email_body.replace('{{LIST_STEPS}}', LIST_STEPS)

            email_body = email_body.replace('{{NAME_REQUEST_URL}}', nr_url)
            email_body = email_body.replace('{{NAMEREQUEST_NUMBER}}', nr_model.nrNum)

            email = {
                'recipients': recepients,
                'content': {
                    'subject': report_name,
                    'body': email_body,
                    'attachments': []
                }
            }
            attachments = []
            attachments.append(
                {
                    'fileName': report_name.replace(' - ', ' ').replace(' ', '_') + '.pdf',
                    'fileBytes': base64.b64encode(report).decode(),
                    'fileUrl': '',
                    'attachOrder': 1
                }
            )
            email['content']['attachments'] = attachments
            return ReportResource._send_email(email)
        except Exception as err:
            return handle_exception(err, 'Error retrieving the report.', 500)

    @cors.crossdomain(origin='*')
    def get(self, nr_id):
        try:
            if not full_access_to_name_request(request):
                return {"message": "You do not have access to this NameRequest."}, 403
            nr_model = Request.query.get(nr_id)
            if not nr_model:
                return jsonify(message='{nr_id} not found'.format(nr_id=nr_model.id)), HTTPStatus.NOT_FOUND
            return ReportResource._get_report(nr_model)
        except Exception as err:
            return handle_exception(err, 'Error retrieving the report.', 500)

    @staticmethod
    def _send_email(email):
        """Send the email."""
        notify_url = current_app.config.get('NOTIFY_API_URL') + current_app.config.get('NOTIFY_API_VERSION')
        authenticated, token = ReportResource._get_service_client_token()
        if not authenticated:
            return jsonify(message='Error in authentication when sending email'), HTTPStatus.INTERNAL_SERVER_ERROR

        headers = {
            'Authorization': 'Bearer {}'.format(token),
            'Content-Type': 'application/json'
        }
        url = notify_url + "/notify"
        response = requests.request("POST", url, json=email, headers=headers)
        if response.status_code != 200:
            raise Exception(response.text)
        return response.content, response.status_code

    @staticmethod
    def _get_report(nr_model):
        if nr_model.stateCd not in [State.APPROVED, State.CONDITIONAL,
                                    State.CONSUMED, State.EXPIRED, State.REJECTED]:
            return jsonify(message='Invalid NR state'.format(nr_id=nr_model.id)), HTTPStatus.BAD_REQUEST

        authenticated, token = ReportResource._get_service_client_token()
        if not authenticated:
            return jsonify(message='Error in authentication'.format(nr_id=nr_model.id)),\
                    HTTPStatus.INTERNAL_SERVER_ERROR

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
            return jsonify(message=str(response.content)), response.status_code
        return response.content, response.status_code

    @staticmethod
    def _get_report_filename(nr_model):
        return 'NR {}.pdf'.format(nr_model.nrNum).replace(' ', '_')

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
    def _get_template_data(nr_model):
        if nr_model.requestTypeCd and (not nr_model.entity_type_cd or not nr_model.request_action_cd):
            # For the NRO ones.
            entity_type, request_action = get_mapped_entity_and_action_code(nr_model.requestTypeCd)
            nr_model.entity_type_cd = entity_type
            nr_model.request_action_cd = request_action
        nr_report_json = nr_model.json()
        nr_report_json['service_url'] = current_app.config.get('NAME_REQUEST_URL')
        nr_report_json['entityTypeDescription'] = ReportResource._get_entity_type_description(nr_model.entity_type_cd)
        nr_report_json['legalAct'] = ReportResource._get_legal_act(nr_model.entity_type_cd)
        isXPRO = nr_model.entity_type_cd in ['XCR', 'XUL', 'RLC', 'XLP', 'XLL', 'XCP', 'XSO']
        nr_report_json['isXPRO'] = isXPRO
        nr_report_json['requestCodeDescription'] = \
            ReportResource._get_request_action_cd_description(nr_report_json['request_action_cd'])
        nr_report_json['nrStateDescription'] = \
            ReportResource._get_state_cd_description(nr_report_json['stateCd'])
        if isXPRO and nr_report_json['nrStateDescription'] == 'Rejected':
            nr_report_json['nrStateDescription'] = 'Not Approved'
        if nr_report_json['expirationDate']:
            tz_aware_expiration_date = nr_model.expirationDate.replace(tzinfo=timezone('UTC'))
            localized_payment_completion_date = tz_aware_expiration_date.astimezone(timezone('US/Pacific'))
            nr_report_json['expirationDate'] = localized_payment_completion_date.strftime('%B %-d, %Y at %-I:%M %p Pacific time')
        if nr_report_json['submittedDate']:
            nr_report_json['submittedDate'] = nr_model.submittedDate.strftime('%B %-d, %Y')
        if nr_report_json['applicants']['countryTypeCd']:
            nr_report_json['applicants']['countryName'] = \
                pycountry.countries.search_fuzzy(nr_report_json['applicants']['countryTypeCd'])[0].name
        actions_obj = ReportResource._get_next_action_text(nr_model.entity_type_cd)
        if actions_obj:
            action_text = actions_obj.get(nr_report_json['request_action_cd'])
            if not action_text:
                action_text = actions_obj.get('DEFAULT')
            if action_text:
                nr_report_json['nextAction'] = action_text
        nr_report_json['approvalDate'] = datetime.today().strftime('%B %-d, %Y')
        return nr_report_json

    @staticmethod
    def _get_service_client_token():
        auth_url = current_app.config.get('PAYMENT_SVC_AUTH_URL')
        client_id = current_app.config.get('PAYMENT_SVC_AUTH_CLIENT_ID')
        secret = current_app.config.get('PAYMENT_SVC_CLIENT_SECRET')
        auth = requests.post(
            auth_url,
            auth=(client_id, secret),
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data={
                'grant_type': 'client_credentials',
                'client_id': client_id,
                'client_secret': secret
            }
        )
        if auth.status_code != 200:
            return False, auth.json()

        token = dict(auth.json())['access_token']
        return True, token

    @staticmethod
    def _get_request_action_cd_description(request_cd: str):
        request_cd_description = {
            'NEW': 'New Business',
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
            'CONDITIONAL': 'Conditional Approval',
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
            'SO': 'BC Social Enterprise',
            'PA': 'BC Private Act',
            'FI': 'BC Credit Union',
            'PAR': 'BC Parish',
            # XPRO and Foreign Types
            'XCR': 'Extraprovincial Limited Company',
            'XUL': 'Extraprovincial Unlimited Liability Company',
            'RLC': 'Extraprovincial Limited Liability Company',
            'XLP': 'Extraprovincial Limited Partnership',
            'XLL': 'Extraprovincial Limited Liability Partnership',
            'XCP': 'Extraprovincial Cooperative Association',
            'XSO': 'Extraprovincial Social Enterprise',
            # Used for mapping back to legacy oracle codes, description not required
            'FIRM': 'FIRM (Legacy Oracle)'
        }
        return entity_type_descriptions.get(entity_type_cd, None)

    @staticmethod
    def _get_action_url(entity_type_cd: str):

        DECIDE_BUSINESS_URL =  current_app.config.get('DECIDE_BUSINESS_URL')
        CORP_FORMS_URL =  current_app.config.get('CORP_FORMS_URL')
        BUSINESS_URL = current_app.config.get('BUSINESS_URL')
        CORP_ONLINE_URL = current_app.config.get('COLIN_URL')

        next_action_text = {
            # BC Types
            'CR':  CORP_ONLINE_URL,
            'UL':  CORP_ONLINE_URL,
            'FR':  DECIDE_BUSINESS_URL,
            'GP':  DECIDE_BUSINESS_URL,
            'DBA': DECIDE_BUSINESS_URL,
            'LP':  CORP_FORMS_URL,
            'LL':  CORP_FORMS_URL,
            'CP':  BUSINESS_URL,
            'BC':  BUSINESS_URL,
            'CC':  CORP_ONLINE_URL,
            'SO': 'BC Social Enterprise',
            'PA': 'Submit appropriate form to BC Registries. Call if assistance required',
            'FI': 'Submit appropriate form to BC Registries. Call if assistance required',
            'PAR': 'Submit appropriate form to BC Registries. Call if assistance required',
            # XPRO and Foreign Types
            'XCR': CORP_ONLINE_URL,
            'XUL': CORP_ONLINE_URL,
            'RLC': CORP_ONLINE_URL,
            'XLP': CORP_FORMS_URL,
            'XLL': CORP_FORMS_URL,
            'XCP': 'Extraprovincial Cooperative Association',
            'XSO': 'Extraprovincial Cooperative Association',
        }
        return next_action_text.get(entity_type_cd, None)

    @staticmethod
    def _get_legal_act(entity_type_cd: str):

        next_action_text = {
            # BC Types
            'CR':  'Business Corporations Act',
            'UL':  'Business Corporations Act',
            'FR':  'Partnership Act',
            'GP':  'Partnership Act',
            'DBA': 'Partnership Act',
            'LP':  'Partnership Act',
            'LL':  'Partnership Act',
            'CP':  'Cooperative Association Act',
            'BC':  'Business Corporations Act',
            'CC':  'Business Corporations Act',
            'SO':  'Business Corporations Act',
            'PA':  '',
            'FI':  'Credit Union Incorporation Act',
            'PAR': 'Trustee (Church Property) Act',
            # XPRO and Foreign Types
            'XCR': '',
            'XUL': '',
            'RLC': '',
            'XLP': '',
            'XLL': '',
            'XCP': '',
            'XSO': '',
        }
        return next_action_text.get(entity_type_cd, None)

    @staticmethod
    def _get_next_action_text(entity_type_cd: str):

        DECIDE_BUSINESS_URL =  current_app.config.get('DECIDE_BUSINESS_URL')
        BUSINESS_CHANGES_URL =  current_app.config.get('BUSINESS_CHANGES_URL')
        CORP_FORMS_URL =  current_app.config.get('CORP_FORMS_URL')
        BUSINESS_URL = current_app.config.get('BUSINESS_URL')
        CORP_ONLINE_URL = current_app.config.get('COLIN_URL')

        next_action_text = {
            # BC Types
            'CR':  {
               'DEFAULT': f'Use this name request to register a business by visiting <a href="{CORP_ONLINE_URL}">'
                          f'{CORP_ONLINE_URL}</a> for more information'
            },
            'UL': {
               'DEFAULT': f'Use this name request to register a business by visiting <a href="{CORP_ONLINE_URL}">'
                          f'{CORP_ONLINE_URL}</a> for more information'
            },
            'FR': {
               'NEW': f'Use this name request to register a business by visiting <a href="{DECIDE_BUSINESS_URL}">'
                        'Registering Proprietorships and Partnerships'
                      '</a> for more information',
               'DEFAULT': f'Use this name request to register a business by visiting <a href="{DECIDE_BUSINESS_URL}">'
                          'Registering Proprietorships and Partnerships</a> for more information. To learn more, visit '
                          f'<a href="{BUSINESS_CHANGES_URL}">Making Changes to your Proprietorship or'
                          ' Partnership</a>'
            },
            'GP': {
               'NEW': f'Use this name request to register a business by visiting <a href="{DECIDE_BUSINESS_URL}">'
                        'BC Registries and Online Services'
                     '</a> for more information',
               'DEFAULT': f'Use this name request to register a business by visiting <a href="{DECIDE_BUSINESS_URL}">'
                          'BC Registries and Online Services</a> for more information. To learn more, visit '
                          f'<a href="{BUSINESS_CHANGES_URL}">Making Changes to your Proprietorship or'
                          ' Partnership</a>'
            },
            'DBA': {
               'NEW': f'Use this name request to register a business by visiting <a href="{DECIDE_BUSINESS_URL}">'
                        'Registering Proprietorships and Partnerships'
                      '</a> for more information',
               'DEFAULT': f'Use this name request to register a business by visiting <a href="{DECIDE_BUSINESS_URL}">'
                          'Registering Proprietorships and Partnerships</a> for more information. To learn more, visit '
                          f'<a href="{BUSINESS_CHANGES_URL}">Making Changes to your Proprietorship or'
                          ' Partnership</a>'
            },
            'LP': {
               'DEFAULT': f'To complete your filing, <a href= "{CORP_FORMS_URL}">visit our Forms page</a> to'
                          ' download and submit a form'
            },
            'LL': {
               'DEFAULT': f'To complete your filing, <a href= "{CORP_FORMS_URL}">visit our Forms page</a> to'
                          ' download and submit a form'
            },
            'CP': {
               'DEFAULT': f'Use this name request to register a business by visiting <a href="{BUSINESS_URL}">{BUSINESS_URL}</a>'
                          ' for more information'
            },
            'BC': {
               'DEFAULT': f'Use this name request to register a business by visiting <a href="{BUSINESS_URL}">{BUSINESS_URL}</a>'
                          ' for more information'
            },
            'CC': {
               'DEFAULT': f'Use this name request to register a business by visiting <a href="{CORP_ONLINE_URL}">'
                          f'{CORP_ONLINE_URL}</a> for more information'
            },
            'SO': {
               'DEFAULT': 'BC Social Enterprise'
            },
            'PA': {
               'DEFAULT': 'Submit appropriate form to BC Registries. Call if assistance required.'
            },
            'FI': {
               'DEFAULT': 'Submit appropriate form to BC Registries. Call if assistance required.'
            },
            'PAR': {
               'DEFAULT': 'Submit appropriate form to BC Registries. Call if assistance required.'
            },
            # XPRO and Foreign Types
            'XCR': {
               'NEW': f'Use this name request to register a business by visiting <a href="{CORP_ONLINE_URL}">'
                      f'{CORP_ONLINE_URL}</a> for more information',
               'CHG': f'Use this name request to register a business by visiting <a href="{CORP_ONLINE_URL}">'
                      f'{CORP_ONLINE_URL}</a> for more information',
               'DEFAULT': f'To complete your filing, <a href= "{CORP_FORMS_URL}">visit our Forms page</a> to'
                          ' download and submit a form'
            },
            'XUL': {
               'DEFAULT': f'Use this name request to register a business by visiting <a href="{CORP_ONLINE_URL}">'
                          f'{CORP_ONLINE_URL}</a> for more information'
            },
            'RLC': {
                'DEFAULT': f'Use this name request to register a business by visiting <a href="{CORP_ONLINE_URL}">'
                          f'{CORP_ONLINE_URL}</a> for more information'
            },
            'XLP': {
               'DEFAULT': f'To complete your filing, <a href= "{CORP_FORMS_URL}">visit our Forms page</a> to'
                          ' download and submit a form'
            },
            'XLL': {
               'DEFAULT': f'To complete your filing, <a href= "{CORP_FORMS_URL}">visit our Forms page</a> to'
                          ' download and submit a form'
            },
            'XCP': {
                'DEFAULT': 'Extraprovincial Cooperative Association'
            },
            'XSO': {
                'DEFAULT': 'Extraprovincial Social Enterprise'
            },
            # Used for mapping back to legacy oracle codes, description not required
            'FIRM': {
                'DEFAULT': 'FIRM (Legacy Oracle)'
            }
        }
        return next_action_text.get(entity_type_cd, None)
