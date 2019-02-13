from hamcrest import *


def test_can_access_home_page(browser, base_url):
    browser.get(base_url + '/')
    body = browser.find_element_by_tag_name('body').text

    assert_that(body, equal_to('Login to administration.'))
