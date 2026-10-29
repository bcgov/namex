from namex.resources.name_requests.report_resource import to_vancouver_datetime


def test_to_vancouver_datetime_after_november_transition():
    result = to_vancouver_datetime("2026-11-01T09:00:00Z")

    assert result.isoformat() == "2026-11-01T02:00:00-07:00"
