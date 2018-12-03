from solr_admin.views.restricted_condition_view import RestrictedCondition2View
from solr_admin.models.restricted_condition import RestrictedCondition2
from tests.support.seeds import seed_condition, seed_word, seed_full_condition
from hamcrest import *


def test_aggregation(db):
    seed_condition(db, cnd_id=1, consenting_body='needs approval')
    seed_word(db, word_id=1, cnd_id=1, word='tdd')
    seed_word(db, word_id=2, cnd_id=1, word='quality')
    view = RestrictedCondition2View(RestrictedCondition2, db.session)
    count, data = view.get_list(page=0, sort_column=None, sort_desc=None, search=None, filters=None)

    assert_that(len(data), equal_to(1))
    assert_that(data[0].cnd_id, equal_to(1))
    assert_that(data[0].consenting_body, equal_to('needs approval'))
    assert_that(data[0].word_phrase, equal_to('tdd, quality'))


def test_resists_bad_order(db):
    seed_condition(db, cnd_id=1, consenting_body='condition-1')
    seed_condition(db, cnd_id=2, consenting_body='condition-2')
    seed_word(db, word_id=2, cnd_id=2, word='quality')
    seed_word(db, word_id=3, cnd_id=1, word='word-1')
    seed_word(db, word_id=1, cnd_id=2, word='tdd')
    view = RestrictedCondition2View(RestrictedCondition2, db.session)
    count, data = view.get_list(page=0, sort_column=None, sort_desc=None, search=None, filters=None)

    assert_that(len(data), equal_to(2))
    assert_that(data[0].cnd_id, equal_to(1))
    assert_that(data[0].consenting_body, equal_to('condition-1'))
    assert_that(data[0].word_phrase, equal_to('word-1'))
    assert_that(data[1].cnd_id, equal_to(2))
    assert_that(data[1].consenting_body, equal_to('condition-2'))
    assert_that(data[1].word_phrase, equal_to('tdd, quality'))


def test_populates_all_fields(db):
    seed_full_condition(db,
                        cnd_id=1,
                        cnd_text='this-text',
                        allow_use='Y',
                        consent_required='N',
                        consenting_body='needs approval',
                        instructions='those-instructions')
    seed_word(db, word_id=1, cnd_id=1, word='tdd')
    view = RestrictedCondition2View(RestrictedCondition2, db.session)
    count, data = view.get_list(page=0, sort_column=None, sort_desc=None, search=None, filters=None)

    assert_that(len(data), equal_to(1))
    assert_that(data[0].cnd_id, equal_to(1))
    assert_that(data[0].cnd_text, equal_to('this-text'))
    assert_that(data[0].allow_use, equal_to('Y'))
    assert_that(data[0].consent_required, equal_to('N'))
    assert_that(data[0].consenting_body, equal_to('needs approval'))
    assert_that(data[0].instructions, equal_to('those-instructions'))
    assert_that(data[0].word_phrase, equal_to('tdd'))
