from hamcrest import *

from solr_admin.models.restricted_condition import RestrictedCondition
from solr_admin.models.restricted_word import RestrictedWord
from solr_admin.models.restricted_word_condition import RestrictedWordCondition
from tests.external.pages.word_condition_creation_page import WordConditionCreationPage
from tests.external.pages.word_condition_page import WordConditionListPage


def test_delete(browser, base_url, db):
    page = WordConditionCreationPage(browser, base_url)
    page.fill('rc_consenting_body', 'needs approval')
    page.save()

    page = WordConditionListPage(browser, base_url)
    assert_that(page.list_size(), equal_to(1))

    page.delete_record(1)
    assert_that(page.list_size(), equal_to(0))

    result = db.session.query(RestrictedCondition).all()
    assert_that(len(result), equal_to(0))

    result = db.session.query(RestrictedWord).all()
    assert_that(len(result), equal_to(0))

    result = db.session.query(RestrictedWordCondition).all()
    assert_that(len(result), equal_to(0))

