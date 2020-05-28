from hamcrest import *

from namex.services.name_request.auto_analyse.auto_analyse import AutoAnalyseService
from namex.services.name_request.builders.name_analysis_builder import NameAnalysisBuilder

list_dist = ['MOUNTAIN', 'VIEW']
list_desc = ['FOOD', 'GROWERS']
list_none = ['MOUNTAIN', 'VIEW', 'FOOD', 'GROWERS']
name = ['MOUNTAIN', 'VIEW', 'FOOD', 'GROWERS']
preprocessed_name_consent = 'MOUNTAIN SMILE FOOD GROWERS'
name_avoid = 'MOUNTAIN VSE FOOD GROWERS'
name_consent = 'ROYAL BC MOUNTAIN FOOD GROWERS'

#user_input = 'ABC COOP PLUMBING INC.'
user_input = "ART's ASSOCIATION OF PLUMBING INC"
entity_type_user = 'UL'
#entity_type_any_desig_user = 'CP'

# Do our service stuff
service = AutoAnalyseService()
builder = NameAnalysisBuilder(service)

# Register and initialize the desired builder
service.use_builder(builder)
service.set_name(name)

'''
def test_check_name_is_well_formed(client, jwt, app):
    assert_that(builder.check_name_is_well_formed(list_desc, list_dist, list_none, name), False)


def test_check_words_to_avoid(client, jwt, app):
    assert_that(builder.check_words_to_avoid(name_avoid), False)


def test_check_words_requiring_consent(client, jwt, app):
    assert_that(builder.check_words_requiring_consent(name_consent), True)
'''

def test_search_conflicts(client, jwt, app):
    assert_that(builder.search_conflicts(list_dist, list_desc), True)


#def test_check_designation(client, jwt, app):
#    assert_that(builder.check_designation(user_input, entity_type_user),
#                [[], ['UL']])

'''
def test_do_analysis(client, jwt, app):
    assert_that(builder.do_analysis(user_input,entity_type_end_desig_user, entity_type_any_desig_user), True)
'''