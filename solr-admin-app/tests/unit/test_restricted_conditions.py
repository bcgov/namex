from hamcrest import *


def test_can_access_synonyms_list(browser, base_url, db):
    db.engine.execute("""
        insert into public.restricted_condition2
        (cnd_id, cnd_text, allow_use, consent_required, consenting_body, instructions, word_phrase) 
        values
        (1, 'first restriction', 'Y', 'Y', 'this body needs to give approval', 'call them', 'tdd, code, bdd, quality');""")
    browser.get(base_url + '/')
    browser.find_element_by_tag_name('a').click()
    browser.find_element_by_link_text('Restricted Condition2').click()
    selection = browser.find_elements_by_css_selector('li.active')

    assert_that(selection[0].text, equal_to('Restricted Condition2'))
    assert_that(selection[1].text, equal_to('List (1)'))

    cell = browser.find_element_by_css_selector('table.model-list tbody tr:nth-child(1) td:nth-child(8)')
    assert_that(cell.text, equal_to('tdd, code, bdd, quality'))
