import pytest
from hamcrest import *
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from tests.conftest import get_browser, connect_with, gecko_driver
import os

from tests.external.support.driver.server_driver import ServerDriver


@pytest.fixture(scope="session")
def new_server(port):
    app = os.path.join(os.path.dirname(__file__), '..', '..', 'app.py')
    server = ServerDriver(name='MyServer', port=port+10)
    server.start(cmd=['python', app, str(port+10)])
    yield server
    server.shutdown()


@pytest.fixture(scope="session")
def second_base_url(port):
    return 'http://localhost:' + str(port+10)


@pytest.fixture(scope="session")
def new_browser(new_server, second_base_url):
    browser = get_browser()
    browser.get(second_base_url + '/admin/synonym')
    connect_with(browser, login='names-no-admin-access')
    yield browser
    browser.quit()


def get_browser():
    options = Options()
    options.headless = True
    service = Service(executable_path=gecko_driver())
    browser = WebDriver(options=options, service=service)

    return browser


def test_cannot_access_synonyms(new_browser, second_base_url):
    browser = new_browser
    browser.get(second_base_url + '/admin/synonym')
    body = browser.find_element_by_tag_name('body')

    assert_that(body.text, contains_string('not authorized'))


def test_cannot_access_virtual_word_condition(new_browser, second_base_url):
    browser = new_browser
    browser.get(second_base_url + '/admin/virtualwordcondition')
    body = browser.find_element_by_tag_name('body')

    assert_that(body.text, contains_string('not authorized'))



