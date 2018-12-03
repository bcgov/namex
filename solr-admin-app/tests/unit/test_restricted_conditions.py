from hamcrest import *
from tests.support.seeds import seed_condition, seed_word


def test_conditions_list(browser, base_url, db):
    seed_condition(db, cnd_id=1, consenting_body='this body needs to give approval')
    seed_word(db, word_id=1, cnd_id=1, word='tdd')
    seed_word(db, word_id=2, cnd_id=1, word='quality')

    browser.get(base_url + '/')
    browser.find_element_by_tag_name('a').click()
    browser.find_element_by_link_text('Restricted Condition2').click()
    selection = browser.find_elements_by_css_selector('li.active')

    assert_that(len(selection), equal_to(2))
    assert_that(selection[0].text, equal_to('Restricted Condition2'))
    assert_that(selection[1].text, equal_to('List (1)'))

    cell = browser.find_element_by_css_selector('table.model-list tbody tr:nth-child(1) td:nth-child(8)')
    assert_that(cell.text, equal_to('tdd, quality'))
