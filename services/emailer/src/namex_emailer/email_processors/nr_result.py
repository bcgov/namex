import base64
from http import HTTPStatus
from pathlib import Path

from flask import current_app, jsonify, make_response, request
from gcp_queue.logging import structured_log
from namex.models import Request, State
from namex.resources.name_requests import ReportResource
from namex.utils.api_resource import handle_exception
from simple_cloudevent import SimpleCloudEvent
from datetime import datetime

from namex_emailer.services.helpers import get_magic_link, query_nr_number, get_instruction_group

RESULT_EMAIL_SUBJECT = 'Name Request Results from Corporate Registry'
CONSENT_EMAIL_SUBJECT = 'Consent Received by Corporate Registry'
DATE_FORMAT = '%B %-d, %Y at %-I:%M %p Pacific time'

EX_COOP_ASSOC = 'Extraprovincial Cooperative Association'
GENERIC_STEPS = 'Submit appropriate form to BC Registries. Call if assistance required'
BCA = 'Business Corporations Act'
PA = 'Partnership Act'

def email_consent_letter(email_info: SimpleCloudEvent):
    try:
        structured_log(request, "DEBUG", f"NR_notification: {email_info}")
        nr_number = email_info.data['request']['nrNum']
        nr_response = query_nr_number(nr_number)
        if nr_response.status_code != HTTPStatus.OK:
            structured_log(request, "ERROR", f"Failed to get nr info for name request: {nr_number}")
            return {}
        nr_model = nr_response.json()
        # nr_model = Request(**nr_data)
        nr_model['consentFlag'] = 'R' # invariant: this function is only called when the consent letter has been received
        ReportResource._update_entity_and_action_code(nr_model)
        report_name = nr_number + ' - ' + CONSENT_EMAIL_SUBJECT
        recipient_emails = []
        recipient_phones = []
        applicants = nr_model['applicants']
        if isinstance(applicants, dict):
            recipient_emails.append(applicants['emailAddress'])
            recipient_phones.append(applicants['phoneNumber'])
        else:
            for applicant in applicants:
                recipient_emails.append(applicant['emailAddress'])
                recipient_phones.append(applicant['phoneNumber'])
        if not nr_model['expirationDate']:
            ReportResource._add_expiry_date(nr_model)
        recipients = ','.join(recipient_emails)
        template_path = current_app.config.get('REPORT_TEMPLATE_PATH')
        file_name = 'consent'
        legal_type = nr_model['entity_type_cd']
        request_action = nr_model["request_action_cd"]
        corpNum = nr_model["corpNum"]
        instruction_group = get_instruction_group(legal_type, request_action, corpNum)
        if instruction_group:
            file_name = f"{file_name}-{instruction_group}"
        email_template = Path(f'{template_path}/{file_name}.md').read_text()
        email_body = _build_email_body(email_template, nr_model, recipient_emails[0], recipient_phones[0])
        email = {
            'recipients': recipients,
            'content': {
                'subject': report_name,
                'body': email_body,
                'attachments': []
            }
        }
        return email
    except Exception as err:
        return handle_exception(err, 'Error retrieving the report.', 500)

def email_report(email_info: SimpleCloudEvent):
    try:

        structured_log(request, "DEBUG", f"NR_notification: {email_info}")
        nr_number = email_info.data['request']['nrNum']
        nr_response = query_nr_number(nr_number)
        if nr_response.status_code != HTTPStatus.OK:
            structured_log(request, "ERROR", f"Failed to get nr info for name request: {nr_number}")
            return {}
        nr_model = nr_response.json()
        # nr_model = Request(**nr_data)

        report, status_code = ReportResource._get_report(nr_model)
        if status_code != HTTPStatus.OK:
            return make_response(jsonify(message=str(report)), status_code)
        report_name = nr_number + ' - ' + RESULT_EMAIL_SUBJECT
        recipient_emails = []
        recipient_phones = []
        applicants = nr_model['applicants']
        if isinstance(applicants, dict):
            recipient_emails.append(applicants['emailAddress'])
            recipient_phones.append(applicants['phoneNumber'])
        else:
            for applicant in applicants:
                recipient_emails.append(applicant['emailAddress'])
                recipient_phones.append(applicant['phoneNumber'])
        recipients = ','.join(recipient_emails)
        template_path = current_app.config.get('REPORT_TEMPLATE_PATH')
        email_template = Path(f'{template_path}/rejected.md').read_text()
        if nr_model['stateCd'] in [State.APPROVED, State.CONDITIONAL]:
            legal_type = nr_model['entity_type_cd']
            request_action = nr_model["request_action_cd"]
            corpNum = nr_model["corpNum"]
            instruction_group = get_instruction_group(legal_type, request_action, corpNum)
            file_name=''
            if nr_model['consentFlag'] in ['Y', 'R']:
                file_name = 'conditional'
            else:
                file_name = 'approved'

            if instruction_group:
                file_name += '-'
                file_name += instruction_group

            email_template = Path(f'{template_path}/{file_name}.md').read_text()

        email_body = _build_email_body(email_template, nr_model, recipient_emails[0], recipient_phones[0])

        email = {
            'recipients': recipients,
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
                'attachOrder': '1'
            }
        )
        email['content']['attachments'] = attachments
        return email
    except Exception as err:
        return handle_exception(err, 'Error retrieving the report.', 500)


def _build_email_body(template: str, nr_model, email, phone):
    var_map = {
        '{{NAMES_INFORMATION_URL}}': current_app.config.get('NAMES_INFORMATION_URL'),
        '{{NAME_REQUEST_URL}}': current_app.config.get('NAME_REQUEST_URL'),
        '{{NAMEREQUEST_NUMBER}}': nr_model['nrNum'],
        '{{BUSINESS_URL}}': current_app.config.get('BUSINESS_URL'),
        '{{DECIDE_BUSINESS_URL}}': current_app.config.get('DECIDE_BUSINESS_URL'),
        '{{CORP_ONLINE_URL}}': current_app.config.get('COLIN_URL'),
        '{{CORP_FORMS_URL}}': current_app.config.get('CORP_FORMS_URL'),
        '{{SOCIETIES_URL}}': current_app.config.get('SOCIETIES_URL'),
        '{{EXPIRATION_DATE}}': nr_model['expirationDate'],
        '{{MAGIC_LINK}}': get_magic_link(nr_model['nrNum'], email, phone)
    }
    for template_string, val in var_map.items():
        if isinstance(val, datetime):
            val = val.strftime(DATE_FORMAT)
        template = template.replace(template_string, val)
    return template
