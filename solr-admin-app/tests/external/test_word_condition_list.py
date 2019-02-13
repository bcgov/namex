from hamcrest import *

from solr_admin.models.virtual_word_condition import VirtualWordCondition
from tests.external.pages.word_condition_page import WordConditionListPage


def test_lists_restricted_word_condition(browser, base_url, db):
    page = WordConditionListPage(browser, base_url)

    result = db.session.query(VirtualWordCondition).all()

    assert_that(len(result), equal_to(0))




