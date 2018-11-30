from hamcrest import *
from solr_admin.models.restricted_condition import RestrictedCondition2


def test_conditions_list(browser, base_url, db):
    db.session.add(RestrictedCondition2(
        consenting_body='this body needs to give approval',
        word_phrase='tdd, code, bdd, quality'))
    db.session.commit()

    browser.get(base_url + '/')
    browser.find_element_by_tag_name('a').click()
    browser.find_element_by_link_text('Restricted Condition2').click()
    selection = browser.find_elements_by_css_selector('li.active')

    assert_that(selection[0].text, equal_to('Restricted Condition2'))
    assert_that(selection[1].text, equal_to('List (1)'))

    cell = browser.find_element_by_css_selector('table.model-list tbody tr:nth-child(1) td:nth-child(8)')
    assert_that(cell.text, equal_to('tdd, code, bdd, quality'))
