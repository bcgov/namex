import time
from hamcrest import *


class SynonymCreationPage:

    def __init__(self, browser, base_url):
        self.browser = browser
        self.base_url = base_url
        self.refresh()

    def refresh(self):
        self.browser.get(self.base_url + '/admin/synonym')
        assert_that(self.browser.find_element_by_tag_name('body').text, contains_string('Namex Administration'))
        self.browser.find_element_by_link_text('Synonym').click()
        self.browser.find_element_by_link_text('Create').click()

    def fill(self, id, value):
        cell = self.browser.find_element_by_css_selector('input#'+id)
        cell.send_keys(value)

    def save(self):
        form = self.browser.find_element_by_css_selector('form')
        form.submit()
        time.sleep(1)

    def getErrorCell(self):
       cell = self.browser.find_element_by_css_selector('div.alert ')
       return cell.text
