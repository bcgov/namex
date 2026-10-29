from datetime import datetime, timezone
from unittest.mock import patch

import pytest

# Replace this import with the actual module containing your audit models.
from namex.models.admin_tables import (
    DecisionReasonAudit,
    RestrictedConditionAudit,
    SynonymAudit,
)


@pytest.mark.parametrize(
    'test_date',
    [
        datetime(2026, 10, 31, 12, 0, tzinfo=timezone.utc),
        datetime(2026, 11, 1, 12, 0, tzinfo=timezone.utc),
        datetime(2026, 11, 2, 12, 0, tzinfo=timezone.utc),
    ],
)
def test_decision_reason_audit_timestamp_uses_utc(test_date):
    """The audit timestamp should remain UTC across the DST transition date."""
    with patch(
        'namex.models.admin_tables.datetime'
    ) as mock_datetime:
        mock_datetime.now.return_value = test_date

        audit = DecisionReasonAudit(
            username='test_user',
            action='UPDATE',
            id=1,
            name='Test Name',
            reason='Unit test',
        )

    assert audit.timestamp == test_date.replace(tzinfo=None)
    assert audit.timestamp.tzinfo is None


def test_restricted_condition_audit_timestamp_uses_utc():
    """RestrictedConditionAudit stores a UTC-aware timestamp."""
    fixed_utc = datetime(2026, 11, 1, 12, 0, tzinfo=timezone.utc)

    with patch('namex.models.admin_tables.datetime') as mock_datetime:
        mock_datetime.now.return_value = fixed_utc

        audit = RestrictedConditionAudit(
            username='test_user',
            action='UPDATE',
            cnd_id=1,
            cnd_text='Test condition',
            words='test',
            consent_required=True,
            consenting_body='Test body',
            instructions='Test instructions',
            allow_use=True,
        )

    assert audit.timestamp == fixed_utc
    assert audit.timestamp.utcoffset().total_seconds() == 0


def test_synonym_audit_timestamp_uses_utc():
    """SynonymAudit stores a naive timestamp representing UTC."""
    fixed_utc = datetime(2026, 11, 1, 12, 0, tzinfo=timezone.utc)

    with patch('namex.models.admin_tables.datetime') as mock_datetime:
        mock_datetime.now.return_value = fixed_utc

        audit = SynonymAudit(
            username='test_user',
            action='UPDATE',
            synonym_id=1,
            category='Test category',
            synonyms_text='test synonym',
            comment='Unit test',
            enabled=True,
        )

    assert audit.timestamp == fixed_utc.replace(tzinfo=None)
    assert audit.timestamp.tzinfo is None
