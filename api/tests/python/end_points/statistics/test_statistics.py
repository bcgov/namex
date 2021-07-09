import json

import pytest
from unittest.mock import patch

from .common import API_BASE_URI, save_names_queue, save_name, save_auto_approved_names, save_approved_names_by_examiner
from ..common.logging import log_request_path

from namex.services.statistics import wait_time_statistics
from namex.services.cache import cache
from tests.python.end_points.common.utils import create_utc_min_date_time, create_utc_date_time


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




@pytest.mark.parametrize('oldest_draft_nr_date, todays_date, expected_wait_days', [
    ('2021-07-03', '2021-07-04', 1)
    ,('2021-07-02', '2021-07-05', 2)
    ,('2021-05-30', '2021-07-10', 30)
    ,('2021-06-28', '2021-07-02', 5)
    ,('2021-07-01', '2021-07-08', 6)
    ,('2021-05-02', '2021-05-23', 15)
    ,('2020-01-01', '2021-07-10', 398)
])
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

    # mock out get_utc_now function in wait_time_statistics to simulate today's date
    with patch.object(wait_time_statistics, 'get_utc_now', return_value=todays_dt):
        response = client.get(request_uri)
        payload = json.loads(response.data)
        assert payload
        assert payload['regular_wait_time'] == expected_wait_days
