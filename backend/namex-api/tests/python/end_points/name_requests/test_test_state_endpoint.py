"""Tests for the test-only set-NR-state endpoint."""

from namex.models import Name, Request, State

from ..util import create_header
from .configuration import API_BASE_URI
from .test_setup_utils.test_helpers import create_draft_nr


def _test_state_path(nr_id):
    return f'{API_BASE_URI}{nr_id}/test-state'


def _headers(jwt):
    return create_header(jwt, ['staff'])


def test_test_state_updates_nr_without_solr_publish(client, jwt, app, mocker):
    """When enabled, the endpoint sets the NR state and does not publish to the names queue."""
    app.config['ALLOW_TEST_ENDPOINT'] = True
    nr = create_draft_nr(client, use_api=False)

    nr_pub = mocker.patch('namex.utils.queue_util.send_name_request_state_msg')
    name_pub = mocker.patch('namex.utils.queue_util.send_name_state_msg')

    response = client.patch(_test_state_path(nr.id), json={'state': 'APPROVED'}, headers=_headers(jwt))

    assert response.status_code == 200
    assert response.get_json()['stateCd'] == State.APPROVED

    updated = Request.query.get(nr.id)
    assert updated.stateCd == State.APPROVED
    ordered = sorted(updated.names, key=lambda n: n.choice or 0)
    assert ordered[0].state == Name.APPROVED
    assert all(n.state == Name.REJECTED for n in ordered[1:])
    nr_pub.assert_not_called()
    name_pub.assert_not_called()


def test_test_state_rejects_invalid_state(client, jwt, app):
    """An unsupported state returns 400."""
    app.config['ALLOW_TEST_ENDPOINT'] = True
    nr = create_draft_nr(client, use_api=False)

    response = client.patch(_test_state_path(nr.id), json={'state': 'CONSUMED'}, headers=_headers(jwt))

    assert response.status_code == 400


def test_test_state_disabled_returns_404(client, jwt, app):
    """When the flag is off, the endpoint is not available."""
    app.config['ALLOW_TEST_ENDPOINT'] = False
    nr = create_draft_nr(client, use_api=False)

    response = client.patch(_test_state_path(nr.id), json={'state': 'APPROVED'}, headers=_headers(jwt))

    assert response.status_code == 404
