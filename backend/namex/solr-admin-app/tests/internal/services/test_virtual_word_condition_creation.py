from solr_admin.models.restricted_condition import RestrictedCondition
from solr_admin.models.restricted_word import RestrictedWord
from solr_admin.models.restricted_word_condition import RestrictedWordCondition
from solr_admin.models.virtual_word_condition import VirtualWordCondition
from solr_admin.services.create_records import create_records
from hamcrest import *


def test_populates_restricted_condition(db):
    model = VirtualWordCondition(
        rc_consenting_body='needs approval',
        rc_condition_text='do that',
        rc_instructions='call me',
        rc_allow_use=True,
        rc_consent_required=True
    )
    create_records(model, db.session)
    result = db.session.query(RestrictedCondition).all()

    assert_that(len(result), equal_to(1))
    assert_that(result[0].consenting_body, equal_to('needs approval'))
    assert_that(result[0].cnd_text, equal_to('do that'))
    assert_that(result[0].instructions, equal_to('call me'))
    assert_that(result[0].allow_use, equal_to('Y'))
    assert_that(result[0].consent_required, equal_to('Y'))


def test_default_flags(db):
    model = VirtualWordCondition(
        rc_consenting_body='needs approval',
        rc_condition_text='do that',
        rc_instructions='call me'
    )
    create_records(model, db.session)
    result = db.session.query(RestrictedCondition).all()

    assert_that(len(result), equal_to(1))
    assert_that(result[0].consenting_body, equal_to('needs approval'))
    assert_that(result[0].cnd_text, equal_to('do that'))
    assert_that(result[0].instructions, equal_to('call me'))
    assert_that(result[0].allow_use, equal_to('Y'))
    assert_that(result[0].consent_required, equal_to('N'))


def test_populates_restricted_word(db):
    model = VirtualWordCondition(
        rc_words='tdd, quality'
    )
    create_records(model, db.session)
    result = db.session.query(RestrictedWord).all()

    assert_that(len(result), equal_to(2))
    assert_that(result[0].word_phrase, equal_to('tdd'))
    assert_that(result[1].word_phrase, equal_to('quality'))


def test_populates_restricted_word_condition(db):
    model = VirtualWordCondition(
        rc_consenting_body='needs approval',
        rc_words='tdd, quality'
    )
    create_records(model, db.session)
    result = db.session.query(RestrictedWordCondition).all()

    assert_that(len(result), equal_to(2))
    assert_that(result[0].cnd_id, equal_to(1))
    assert_that(result[0].word_id, equal_to(1))
    assert_that(result[1].cnd_id, equal_to(1))
    assert_that(result[1].word_id, equal_to(2))


def test_multi_creation(db):
    one = VirtualWordCondition(
        rc_consenting_body='needs approval',
        rc_words='tdd, quality'
    )
    db.session.add(one)
    create_records(one, db.session)

    two = VirtualWordCondition(
        rc_consenting_body='needs signature',
        rc_words='bc, royal'
    )
    db.session.add(two)
    create_records(two, db.session)

    three = VirtualWordCondition(
        rc_consenting_body='needs magic',
        rc_words='one, two, three, four ,five'
    )
    db.session.add(three)
    create_records(three, db.session)

    result = db.session.query(RestrictedWordCondition).all()

    assert_that(len(result), equal_to(9))
