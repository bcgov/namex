from hamcrest import *

from namex.services.name_request.auto_analyse.auto_analyse import AutoAnalyseService
from namex.services.name_request.name_analysis_builder_v1.name_analysis_builder import NameAnalysisBuilder
import pandas as pd

list_dist = ['MOUNTAIN', 'VIEW']
list_desc = []
list_none = ['MOUNTAIN', 'VIEW', 'FOOD', 'GROWERS']
name = ['MOUNTAIN', 'VIEW', 'FOOD', 'GROWERS']
user_input = 'MOUNTAIN VIEW FOOD GROWERS LTD.'

# Do our service stuff
service = AutoAnalyseService()
builder = NameAnalysisBuilder(service)

# Register and initialize the desired builder
service.use_builder(builder)
service.set_name(name)


def test_check_name_is_well_formed(client, jwt, app):
    assert_that(builder.check_name_is_well_formed(list_desc, list_dist, list_none, name), False)


def test_check_words_to_avoid(client, jwt, app):
    assert_that(builder.check_words_to_avoid(name), True)


def test_search_conflicts(client, jwt, app):
    assert_that(builder.search_conflicts(list_dist, list_desc), True)


def test_do_analysis(client, jwt, app):
    assert_that(builder.do_analysis(user_input), True)
