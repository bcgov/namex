from hamcrest import *


def test_can_assert():
    assert_that(1+1, equal_to(2))


def test_can_access_home_page(browser, base_url):
    browser.get(base_url + '/')
    body = browser.find_element_by_tag_name('body').text

    assert 'Click me to get to Synonyms!' == body


def test_can_access_synonyms_list(browser, base_url, db):
    db.engine.execute("insert into public.synonym(category, synonyms_text) values('hello', 'world');")
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

