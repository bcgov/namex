from solr_admin.models.restricted_condition import RestrictedCondition
from solr_admin.models.restricted_word import RestrictedWord
from solr_admin.models.restricted_word_condition import RestrictedWordCondition
from solr_admin.models.virtual_word_condition import VirtualWordCondition
from solr_admin.services.create_records import create_records
from hamcrest import *

from solr_admin.services.update_records import update_records


def test_populates_restricted_condition(db):
    initial = VirtualWordCondition(
        rc_consenting_body='needs approval',
        rc_words='tdd, quality'
    )
    db.session.add(initial)
    create_records(initial, db.session)

    result = db.session.query(VirtualWordCondition).all()
    updated = result[0]
    updated.rc_consenting_body = 'needs signature'
    db.session.commit()
    assert_that(result[0].rc_consenting_body, equal_to('needs signature'))

    result = db.session.query(VirtualWordCondition).all()
    assert_that(len(result), equal_to(1))

    update_records(db.session)
    result = db.session.query(RestrictedCondition).all()

    assert_that(len(result), equal_to(1))
    assert_that(result[0].consenting_body, equal_to('needs signature'))


