from hamcrest import *
from solr_admin.models.synonym import Synonym


def test_synonyms_list(browser, base_url, db):
    db.session.add(Synonym(category='hello', synonyms_text='world'))
    db.session.commit()

    browser.get(base_url + '/')
    browser.find_element_by_tag_name('a').click()
    browser.find_element_by_link_text('Synonym').click()
    selection = browser.find_elements_by_css_selector('li.active')

    assert_that(selection[0].text, equal_to('Synonym'))
    assert_that(selection[1].text, equal_to('List (1)'))

    cell = browser.find_element_by_css_selector('table.model-list tbody tr:nth-child(1) td:nth-child(2)')
    assert_that(cell.text, equal_to('hello'))
    cell = browser.find_element_by_css_selector('table.model-list tbody tr:nth-child(1) td:nth-child(3)')
    assert_that(cell.text, equal_to('world'))
