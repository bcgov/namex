"""Test-only endpoint to set a Name Request state without notifying Solr.

Intended for API partners and QA to drive NR workflows in non-production
environments. It updates the NR (and its names) state directly and
intentionally does NOT publish a names state-change event, so the change is
never propagated to the Solr conflict index.

Guarded by the ALLOW_TEST_ENDPOINT config flag - returns 404 when not enabled
(prod never sets the flag).
"""
from http import HTTPStatus

from flask import current_app, g, jsonify, make_response, request
from flask_restx import Resource

from namex import jwt
from namex.models import Event, Name, Request, State
from namex.services import EventRecorder
from namex.services.name_request.utils import get_or_create_user_by_jwt
from namex.utils.auth import cors_preflight

from .api_namespace import api

# States this test helper is permitted to set (extend as needed).
ALLOWED_TEST_STATES = [State.APPROVED, State.REJECTED]

MSG_NOT_FOUND = 'Resource not found'


@cors_preflight('PATCH')
@api.route('/<int:nr_id>/test-state', strict_slashes=False, methods=['PATCH', 'OPTIONS'])
class TestNameRequestState(Resource):
    """TEST ONLY: force an NR state without pushing to Solr."""

    @jwt.requires_auth
    @api.doc(
        description=(
            'TEST ONLY. Force a name request to APPROVED or REJECTED without publishing a '
            'names state-change event - the update is NOT propagated to Solr. '
            'Available only when ALLOW_TEST_ENDPOINT is enabled (non-production).'
        ),
        params={'nr_id': 'Internal ID of the name request'},
        responses={
            200: 'NR state updated (Solr not notified)',
            400: 'Invalid or unsupported state',
            401: 'Unauthorized',
            404: 'Endpoint disabled, or name request not found',
            500: 'Internal server error',
        },
    )
    def patch(self, nr_id):
        # Hard guard: only available when explicitly enabled. Prod never sets the flag.
        if not current_app.config.get('ALLOW_TEST_ENDPOINT'):
            return make_response(jsonify(message=MSG_NOT_FOUND), HTTPStatus.NOT_FOUND)

        json_input = request.get_json(silent=True) or {}
        state = str(json_input.get('state', '')).upper()
        if state not in ALLOWED_TEST_STATES:
            return make_response(
                jsonify(message=f'Invalid state. Allowed: {", ".join(ALLOWED_TEST_STATES)}'),
                HTTPStatus.BAD_REQUEST,
            )

        nr_model = Request.query.get(nr_id)
        if not nr_model:
            return make_response(jsonify(message='Name Request not found'), HTTPStatus.NOT_FOUND)

        # Update the NR and its names directly.
        # Mirror a real decision: APPROVED approves the first choice and rejects the
        # alternatives; REJECTED rejects every name. (nr_model.names is ordered by choice.)
        nr_model.stateCd = state
        if state == State.APPROVED:
            for index, name in enumerate(nr_model.names):
                name.state = Name.APPROVED if index == 0 else Name.REJECTED
        else:
            for name in nr_model.names:
                name.state = Name.REJECTED

        # IMPORTANT: deliberately DO NOT call send_name_request_state_msg() /
        # send_name_state_msg() here. Skipping the queue publish is the entire point
        # of this endpoint - the state change must never reach Solr.
        nr_model.save_to_db()

        user = get_or_create_user_by_jwt(g.jwt_oidc_token_info)
        EventRecorder.record(user, Event.PATCH + ' [test-state-override]', nr_model, {'stateCd': state})

        return make_response(
            jsonify(nrNum=nr_model.nrNum, stateCd=nr_model.stateCd, message='State updated (Solr not notified)'),
            HTTPStatus.OK,
        )
