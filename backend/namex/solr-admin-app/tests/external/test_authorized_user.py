import time
from hamcrest import *
from selenium.webdriver.common.by import By


def test_can_access_synonyms(browser, base_url, db):
    browser.get(base_url + '/admin/synonym')
    assert_that(browser.find_element(By.TAG_NAME, 'body').text, contains_string('Namex Administration'))


def test_can_access_virtual_word_condition(browser, base_url, db):
    browser.get(base_url + '/admin/virtualwordcondition')
    assert_that(browser.find_element(By.TAG_NAME, 'body').text, contains_string('Namex Administration'))

