from solr_admin.models.virtual_word_condition import VirtualWordCondition
from hamcrest import *


def test_allow_use_defaults_to_true(db):
    record = VirtualWordCondition()
    db.session.add(record)
    db.session.commit()

    assert_that(record.rc_allow_use, equal_to(True))


def test_consent_required_defaults_to_false(db):
    record = VirtualWordCondition()
    db.session.add(record)
    db.session.commit()

    assert_that(record.rc_consent_required, equal_to(False))
