from hamcrest import *
from solr_admin.models.restricted_condition_audit import RestrictedConditionAudit
from tests.external.pages.word_condition_creation_page import WordConditionCreationPage

def test_word_conditon_audit_creation(browser, base_url, db):

    page = WordConditionCreationPage(browser, base_url)
    page.fill('rc_consenting_body', 'me')
    page.fill('rc_words', 'needs, BC, approval')
    page.fill('rc_instructions', 'needs approval')
    page.fill('rc_condition_text', 'This means something')
    page.save()


    browser.get(base_url + '/admin/restrictedconditionaudit')
    browser.find_element_by_link_text('Restricted Condition Audit').click()
    selection = browser.find_elements_by_css_selector('li.active')

    assert_that(selection[0].text, equal_to('Restricted Condition Audit'))
    assert_that(selection[1].text, equal_to('List (1)'))

    cell = browser.find_element_by_css_selector('table.model-list tbody tr:nth-child(1) td.col-username')
    assert_that(cell.text, equal_to('names-with-admin-access'))
    cell = browser.find_element_by_css_selector('table.model-list tbody tr:nth-child(1) td.col-action')
    assert_that(cell.text, equal_to('CREATE'))
    cell = browser.find_element_by_css_selector('table.model-list tbody tr:nth-child(1) td.col-cnd_text')
    assert_that(cell.text, equal_to('This means something'))
    cell = browser.find_element_by_css_selector('table.model-list tbody tr:nth-child(1) td.col-words')
    assert_that(cell.text, equal_to('needs, BC, approval'))
    cell = browser.find_element_by_css_selector('table.model-list tbody tr:nth-child(1) td.col-consenting_body')
    assert_that(cell.text, equal_to('me'))
    cell = browser.find_element_by_css_selector('table.model-list tbody tr:nth-child(1) td.col-instructions')
    assert_that(cell.text, equal_to('needs approval'))

