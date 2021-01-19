import base64
import json
import os
from http import HTTPStatus
from pathlib import Path

import requests
from flask import current_app, jsonify
from flask_restx import Resource, cors

from namex.models import Request
from namex.utils.api_resource import handle_exception
from namex.utils.auth import cors_preflight
from namex.utils.logging import setup_logging

from .api_namespace import api

setup_logging()  # Important to do this first


@cors_preflight('GET')
@api.route('/<int:nr_id>/result', strict_slashes=False, methods=['GET', 'OPTIONS'])
@api.doc(params={
    'nr_id': 'NR ID - This field is required'
})
class ReportResource(Resource):
    @cors.crossdomain(origin='*')
    def get(self, nr_id):
        try:
            nr_model = Request.query.get(nr_id)
            if not nr_model:
                return jsonify(message='{nr_id} not found'.format(nr_id=nr_model.id)), HTTPStatus.NOT_FOUND

            authenticated, token = ReportResource.get_service_client_token()
            if not authenticated:
                return jsonify(message='Error in authentication'.format(nr_id=nr_model.id)),\
                       HTTPStatus.INTERNAL_SERVER_ERROR

            headers = {
                'Authorization': 'Bearer {}'.format(token),
                'Content-Type': 'application/json'
            }
            data = {
                'reportName': ReportResource._get_report_filename(nr_model),
                'template': "'" + base64.b64encode(bytes(self._get_template(), 'utf-8')).decode() + "'",
                'templateVars': ReportResource._get_template_data(nr_model)
            }
            response = requests.post(url=current_app.config.get('REPORT_SVC_URL'), headers=headers,
                                     data=json.dumps(data))

            if response.status_code != HTTPStatus.OK:
                return jsonify(message=str(response.content)), response.status_code
            return response.content, response.status_code
        except Exception as err:
            return handle_exception(err, 'Error retrieving the report.', 500)

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
        ]
        # substitute template parts - marked up by [[filename]]
        for template_part in template_parts:
            template_part_code = Path(f'{template_path}/template-parts/{template_part}.html').read_text()
            template_code = template_code.replace('[[{}.html]]'.format(template_part), template_part_code)

        return template_code

    @staticmethod
    def _get_template_data(nr_model):
        nr_report_json = nr_model.json()
        return nr_report_json

    @staticmethod
    def get_service_client_token():
        auth_url = os.getenv('PAYMENT_SVC_AUTH_URL')
        client_id = os.getenv('PAYMENT_SVC_AUTH_CLIENT_ID')
        secret = os.getenv('PAYMENT_SVC_CLIENT_SECRET')
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
