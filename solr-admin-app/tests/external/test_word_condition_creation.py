from hamcrest import *

from solr_admin.models.restricted_condition import RestrictedCondition
from tests.external.pages.word_condition_creation_page import WordConditionCreationPage


def test_populates_restricted_condition(browser, base_url, db):
    page = WordConditionCreationPage(browser, base_url)
    page.fill('rc_consenting_body', 'needs approval')
    page.save()

    result = db.session.query(RestrictedCondition).all()

    assert_that(len(result), equal_to(1))
    assert_that(result[0].consenting_body, equal_to('needs approval'))
