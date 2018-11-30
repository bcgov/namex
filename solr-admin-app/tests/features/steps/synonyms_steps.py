from behave import fixture, given, when, then, step
from hamcrest import *
from solr_admin.models.synonym import Synonym


@given(u'the database is seeded with the synonyms')
def seed(context):
    for row in context.table:
        context.db.session.add(Synonym(category=row['category'], synonyms_text=row['synonyms']))
        context.db.session.commit()


@when(u'I access the synonym list')
def synonym_list(context):
    context.browser.get(context.base_url + '/')
    context.browser.find_element_by_tag_name('a').click()
    context.browser.find_element_by_link_text('Synonym').click()


@then(u'I see that the list contains {expected:d} lines')
def verify_list(context, expected):
    lines = context.browser.find_elements_by_css_selector('table.model-list tbody tr')

    assert_that(len(lines), equal_to(expected))
