from hamcrest import *


class RestrictedWordConditionAuditListPage:

    def __init__(self, browser, base_url):
        self.browser = browser
        self.base_url = base_url
        self.refresh()

    def refresh(self):
        self.browser.get(self.base_url + '/admin/restrictedconditionaudit')
        assert_that(self.browser.find_element_by_tag_name('body').text, contains_string('Namex Administration'))
        self.browser.find_element_by_link_text('Restricted Condition Audit').click()

    def list_size(self):
        rows_css = 'table.model-list tbody tr '
        rows = self.browser.find_elements_by_css_selector(rows_css)

        return len(rows) if 'There are no items in the table' not in rows[0].text else 0

    def row(self, index):
        return 'table.model-list tbody tr:nth-child(' + str(index) + ') '

    def element(self, what, index):
        selector = self.row(index) + what
        cell = self.browser.find_element_by_css_selector(selector)

        return cell

    def consenting_body_of_row(self, index):
        return self.element('td.col-consenting_body ', index)

    def words_of_row(self, index):
        return self.element('td.col-words ', index)

    def instructions_of_row(self, index):
        return self.element('td.col-instructions ', index)

    def condition_text_of_row(self, index):
        return self.element('td.col-cnd_text ', index)

