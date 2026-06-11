"""Tests for the test-only set-NR-state endpoint (#32707).

Verifies the endpoint updates NR state WITHOUT publishing a names state-change
event (so Solr is never notified), and is disabled (404) when the
ALLOW_TEST_ENDPOINT flag is off.
"""
import json

from namex.models import Name, Request, State

from ..common.http import get_test_headers
from .configuration import API_BASE_URI
from .test_setup_utils.test_helpers import create_draft_nr


def _test_state_path(nr_id):
    return f'{API_BASE_URI}{nr_id}/test-state'


def test_test_state_updates_nr_without_solr_publish(client, jwt, app, mocker):
    """When enabled, the endpoint sets the NR state and does NOT publish to the names queue."""
    app.config['ALLOW_TEST_ENDPOINT'] = True

    # spy on the Solr-trigger publish helpers - they must NOT be called
    nr_pub = mocker.patch('namex.utils.queue_util.send_name_request_state_msg')
    name_pub = mocker.patch('namex.utils.queue_util.send_name_state_msg')

    nr = create_draft_nr(client, use_api=False)

    response = client.patch(
        _test_state_path(nr.id),
        data=json.dumps({'state': 'APPROVED'}),
        headers=get_test_headers(),
    )

    assert response.status_code == 200
    payload = json.loads(response.data)
    assert payload['stateCd'] == State.APPROVED

    # NR + names updated in the DB (re-query to avoid a stale reference)
    updated = Request.query.get(nr.id)
    assert updated.stateCd == State.APPROVED
    # first choice approved; any alternatives rejected
    ordered = sorted(updated.names, key=lambda n: n.choice or 0)
    assert ordered[0].state == Name.APPROVED
    assert all(n.state == Name.REJECTED for n in ordered[1:])

    # the whole point: nothing was published, so Solr was never notified
    nr_pub.assert_not_called()
    name_pub.assert_not_called()


def test_test_state_rejects_invalid_state(client, jwt, app):
    """An unsupported state returns 400."""
    app.config['ALLOW_TEST_ENDPOINT'] = True
    nr = create_draft_nr(client, use_api=False)

    response = client.patch(
        _test_state_path(nr.id),
        data=json.dumps({'state': 'CONSUMED'}),
        headers=get_test_headers(),
    )

    assert response.status_code == 400


def test_test_state_disabled_returns_404(client, jwt, app):
    """When the flag is off (production), the endpoint is not available."""
    app.config['ALLOW_TEST_ENDPOINT'] = False
    nr = create_draft_nr(client, use_api=False)

    response = client.patch(
        _test_state_path(nr.id),
        data=json.dumps({'state': 'APPROVED'}),
        headers=get_test_headers(),
    )

    assert response.status_code == 404
