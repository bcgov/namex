from hamcrest import *
from solr_admin.models.restricted_condition_audit import RestrictedConditionAudit
from tests.external.pages.word_condition_creation_page import WordConditionCreationPage

from tests.external.pages.restricted_word_condition_audit_list_page import RestrictedWordConditionAuditListPage

def test_word_conditon_audit_creation(browser, base_url, db):

    page = WordConditionCreationPage(browser, base_url)
    page.fill('rc_consenting_body', 'me')
    page.fill('rc_words', 'needs, BC, approval')
    page.fill('rc_instructions', 'needs approval')
    page.fill('rc_condition_text', 'This means something')
    page.save()

    page = RestrictedWordConditionAuditListPage(browser, base_url)
    assert_that(page.list_size(), equal_to(1))

    assert_that(page.consenting_body_of_row(1).text, equal_to('me'))
    assert_that(page.words_of_row(1).text, equal_to('needs, BC, approval'))
    assert_that(page.instructions_of_row(1).text, equal_to('needs approval'))
    assert_that(page.condition_text_of_row(1).text, equal_to('This means something'))


