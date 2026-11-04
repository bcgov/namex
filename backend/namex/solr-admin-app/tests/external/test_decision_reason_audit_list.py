from hamcrest import *
from tests.external.pages.decision_reason_audit_list_page import DecisionReasonAuditListPage
from tests.external.pages.decision_reason_creation_page import DecisionReasonCreationPage


def test_decision_reason_audit_creation(browser, base_url, db):

    page = DecisionReasonCreationPage(browser, base_url)
    page.fill('name', 'me')
    page.fill('reason', 'because')
    page.save()

    page = DecisionReasonAuditListPage(browser, base_url)
    assert_that(page.list_size(), equal_to(1))

    assert_that(page.name_of_row(1).text, equal_to('me'))
    assert_that(page.reason_of_row(1).text, equal_to('because'))

