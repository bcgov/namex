from behave import fixture, given, when, then, step
from hamcrest import *


@when('I access the home page')
def access_home_page(context):
    context.browser.get(context.base_url + '/')


@then('I see the greetings "{expected}"')
def verify_greetings(context, expected):
    body = context.browser.find_element_by_tag_name('body').text
    assert_that(body, equal_to(expected))

