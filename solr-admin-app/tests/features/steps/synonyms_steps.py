from behave import fixture, given, when, then, step
from hamcrest import *


@given(u'the database is seeded with the synonyms')
def seed(context):
    for row in context.table:
        category = row['category']
        synonyms = row['synonyms']
        context.db.engine.execute(
            "insert into public.synonym(category, synonyms_text) values('{}', '{}');".format(category, synonyms))


@when(u'I access the synonym list')
def synonym_list(context):
    context.browser.get(context.base_url + '/')
    context.browser.find_element_by_tag_name('a').click()
    context.browser.find_element_by_link_text('Synonym').click()


@then(u'I see that the list contains {expected:d} lines')
def verify_list(context, expected):
    lines = context.browser.find_elements_by_css_selector('table.model-list tbody tr')

    assert_that(len(lines), equal_to(expected))
