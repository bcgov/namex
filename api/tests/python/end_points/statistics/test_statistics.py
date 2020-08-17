import json
from .common import API_BASE_URI, save_names_queue, save_auto_approved_names, save_approved_names_by_examiner
from ..common.http import build_request_uri
from ..common.logging import log_request_path


def test_get_statistics(client, jwt, app):
    request_uri = API_BASE_URI
    log_request_path(request_uri)

    save_auto_approved_names(1000)
    save_approved_names_by_examiner(150)
    save_names_queue(20)
    save_names_queue(80, True)

    response = client.get(request_uri)
    payload = json.loads(response.data)

    assert isinstance(payload.get('auto_approved_count'), int) is True
    assert isinstance(payload.get('priority_wait_time'), int) is True
    assert isinstance(payload.get('regular_wait_time'), int) is True
