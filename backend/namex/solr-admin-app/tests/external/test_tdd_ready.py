from hamcrest import *
from selenium.webdriver.common.by import By


def test_can_access_home_page(browser, base_url):
    browser.get(base_url + '/')
    body = browser.find_element(By.TAG_NAME, 'body').text

    assert_that(body, equal_to('Login to administration.'))
