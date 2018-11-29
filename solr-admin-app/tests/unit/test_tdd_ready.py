from hamcrest import *


def test_can_assert():
    assert_that(1+1, equal_to(2))
    import os
    print(os.name)
    import platform
    print(platform.system())


def test_can_access_home_page(browser, base_url):
    browser.get(base_url + '/')
    body = browser.find_element_by_tag_name('body').text

    assert 'Click me to get to Synonyms!' == body

