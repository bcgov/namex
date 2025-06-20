import json
from unittest.mock import MagicMock, patch

import pytest

from namex.models import Request
from namex.services.cache import cache
from namex.services.statistics import wait_time_statistics

from ...end_points.common.utils import create_utc_date_time, create_utc_min_date_time
from ..common.logging import log_request_path
from .common import API_BASE_URI, save_approved_names_by_examiner, save_auto_approved_names, save_name, save_names_queue


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


@pytest.mark.parametrize(
    'oldest_draft_nr_date, todays_date, expected_wait_days',
    [
        ('2021-07-03', '2021-07-04', 1),
        ('2021-07-02', '2021-07-05', 2),
        ('2021-05-30', '2021-07-10', 30),
        ('2021-06-28', '2021-07-02', 5),
        ('2021-07-01', '2021-07-08', 6),
        ('2021-05-02', '2021-05-23', 15),
        ('2020-01-01', '2021-07-10', 398),
    ],
)
def test_get_statistics_wait_time(client, jwt, app, oldest_draft_nr_date, todays_date, expected_wait_days):
    """Assert that wait time statistics are being generated correctly."""
    request_uri = API_BASE_URI
    # create some NR data to simulate real scenario
    save_auto_approved_names(1000)
    save_approved_names_by_examiner(150)
    save_names_queue(20)
    save_names_queue(80, True)

    oldest_draft_nr_dt = create_utc_min_date_time(oldest_draft_nr_date)
    # save the oldest unexamined NR to db
    save_name(oldest_draft_nr_dt, 1111111, False)
    todays_dt = create_utc_date_time(todays_date, 12, 30, 59, 999999)

    # need to clear cache on statistics resource to test different test param values
    cache.clear()

    # Mock out Request.get_waiting_time to simulate wait time calculation for regular and priority queues
    with patch.object(Request, 'get_oldest_draft') as mock_get_oldest_draft, \
        patch.object(Request, 'get_waiting_time') as mock_get_waiting_time:
        mock_get_oldest_draft.return_value = MagicMock(submittedDate=oldest_draft_nr_dt)
        mock_get_waiting_time.side_effect = lambda priority_queue: expected_wait_days if not priority_queue else 0
        response = client.get(request_uri)
        payload = json.loads(response.data)
        assert payload
        assert isinstance(payload.get('regular_wait_time'), int)
        assert payload['regular_wait_time'] == expected_wait_days, \
            f"[ASSERT FAILED] Expected {expected_wait_days} but got {payload['regular_wait_time']}"
