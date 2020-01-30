import itertools

import pandas as pd
from sqlalchemy import create_engine

from namex.services.name_request.auto_analyse.name_analysis_utils import build_query_distinctive, \
    build_query_descriptive, get_substitution_list, get_synonym_list
from ..auto_analyse.abstract_name_analysis_builder \
    import AbstractNameAnalysisBuilder, ProcedureResult

from ..auto_analyse import AnalysisResultCodes, MAX_LIMIT

'''
Sample builder
# TODO: What convention should we use? Nice to use _v<BuilderVersion> if it doesn't break PEP8
'''


class NameAnalysisBuilder(AbstractNameAnalysisBuilder):
    # These properties are inherited from the parent
    # The build director (eg. NameAnalysisDirector) populates these properties
    # as part of its prepare_data
    # _synonyms = []
    # _substitutions = []
    # _stop_words = []
    # _designated_end_words = []
    # _designated_any_words = []
    #
    # _in_province_conflicts = []
    # _all_conflicts = []
    #
    # _name = ''

    _distinctive_words = []
    _descriptive_words = []

    POSTGRES_ADDRESS = 'localhost'
    POSTGRES_PORT = '5432'
    POSTGRES_USERNAME = 'postgres'
    POSTGRES_PASSWORD = ''
    POSTGRES_DBNAME_SYNS = 'local-sandbox-dev'
    POSTGRES_DBNAME_DATA = 'namex-local'

    postgres_str = ('postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'.format(username=POSTGRES_USERNAME,
                                                                                            password=POSTGRES_PASSWORD,
                                                                                            ipaddress=POSTGRES_ADDRESS,
                                                                                            port=POSTGRES_PORT,
                                                                                            dbname=POSTGRES_DBNAME_DATA))

    cnx = create_engine(postgres_str)

    '''
    Check to see if a provided name is valid
    Override the abstract / base class method
    @return ProcedureResult
    '''

    def check_name_is_well_formed(self, list_desc, list_dist, list_none, name):

        result = ProcedureResult()
        result.is_valid = False

        # if (len(list_desc) > 0 and len(list_dist) > 0) and (list_desc != list_dist) and (
        #        (list_dist + list_desc) == name):
        #    success = True

        # Return one of the following:
        # AnalysisResultCodes.CONTAINS_UNCLASSIFIABLE_WORD
        # AnalysisResultCodes.TOO_MANY_WORDS
        # AnalysisResultCodes.ADD_DISTINCTIVE_WORD
        # AnalysisResultCodes.ADD_DESCRIPTIVE_WORD

        if len(list_none) > 0:
            result.is_valid = False
            result.result_code = AnalysisResultCodes.CONTAINS_UNCLASSIFIABLE_WORD
        elif len(list_dist) < 1:
            result.is_valid = False
            result.result_code = AnalysisResultCodes.ADD_DISTINCTIVE_WORD
        elif len(list_desc) < 1:
            result.is_valid = False
            result.result_code = AnalysisResultCodes.ADD_DESCRIPTIVE_WORD
        elif len(name) > MAX_LIMIT:
            result.is_valid = False
            result.result_code = AnalysisResultCodes.TOO_MANY_WORDS
        elif list_desc == list_dist:
            result.is_valid = False
            result.result_code = AnalysisResultCodes.CONTAINS_UNCLASSIFIABLE_WORD
        elif list_dist + list_desc != name:
            result.is_valid = False
            result.result_code = AnalysisResultCodes.CONTAINS_UNCLASSIFIABLE_WORD

        return result
        '''
        success = False
        if (len(list_desc) > 0 and len(list_dist) > 0) and (list_desc != list_dist) and (
                (list_dist + list_desc) == name):
            success = True
        return success
    '''
    Override the abstract / base class method
    @return ProcedureResult
    '''

    def check_words_to_avoid(self):
        result = ProcedureResult()
        result.is_valid = True

        if not result.is_valid:
            result.result_code = AnalysisResultCodes.WORD_TO_AVOID

        return result

    '''
    Override the abstract / base class method
    Input: list_dist= ['MOUNTAIN', 'VIEW']
           list_desc= ['FOOD', 'GROWERS']
    @return ProcedureResult
    '''

    def search_conflicts(self, list_dist, list_desc, cnx=create_engine(postgres_str)):
        result = ProcedureResult()
        result.is_valid = True

        # dist_substitution_list:  [['mount', 'mountain', 'mt', 'mtn'], ['view', 'vu']]
        # desc_substitution_list: [['food, restaurant, bar'],['growers']]

        distinctive = ' '.join(map(str, list_dist)).replace(',', ' ').upper().strip()

        dist_substitution_list = []

        for w_dist in list_dist:
            substitution_list = get_substitution_list(w_dist)
            if substitution_list:
                dist_substitution_list.append(substitution_list)
            else:
                dist_substitution_list.append(w_dist.lower())

        # All possible permutations of elements in dist_list
        # [('mount', 'view'), ('mount', 'vu'), ('mountain', 'view'), ('mountain', 'vu'), ('mt', 'view'), ('mt', 'vu'), ('mtn', 'view'),
        #  ('mtn', 'vu')]
        if dist_substitution_list:
            dist_all_permutations = list(itertools.product(*dist_substitution_list))
            query = build_query_distinctive(dist_all_permutations)

            desc_synonym_list = []
            for w_desc in list_desc:
                synonym_list = get_synonym_list(w_desc)
                if synonym_list:
                    desc_synonym_list.extend(synonym_list)
                else:
                    desc_synonym_list.extend([w_desc.lower()])

            if desc_synonym_list:
                query = build_query_descriptive(desc_synonym_list, query)
                matches = pd.read_sql_query(query, cnx)

                if matches.values.tolist():
                    result.is_valid = False
                    result.result_code = AnalysisResultCodes.CORPORATE_CONFLICT
                else:
                    result.is_valid = True
                    result.result_code = AnalysisResultCodes.VALID_NAME
            else:
                result.is_valid = False
                result.result_code = AnalysisResultCodes.ADD_DESCRIPTIVE_WORD
        else:
            result.is_valid = False
            result.result_code = AnalysisResultCodes.ADD_DISTINCTIVE_WORD

        return result
        '''
        # dist_substitution_list:  [['mount', 'mountain', 'mt', 'mtn'], ['view', 'vu']]
        # desc_substitution_list: [['food, restaurant, bar'],['growers']]

        distinctive = ' '.join(map(str, list_dist)).replace(',', ' ').upper().strip()

        # This section depends on Synonyms API to get the substitution list:
        # For w_dist in list_dist:
        #    substitution_list= get_substitution_list(w_dist)
        #    If not substitution_list:
        #       dist_list.append(w_dist)
        #    else:
        #       dist_list.extend(substitution_list)

        #  dist_substitution_list= [w_dist if not get_substitution_list(w_dist) else get_substitution_list(w_dist) for w_dist in list_dist]
        #  Next line to be removed hard-coded dist_list response when having API results:
        dist_substitution_list = [['mount', 'mountain', 'mt', 'mtn'], ['view', 'vu']]

        # All possible permutations of elements in dist_list
        # [('mount', 'view'), ('mount', 'vu'), ('mountain', 'view'), ('mountain', 'vu'), ('mt', 'view'), ('mt', 'vu'), ('mtn', 'view'), ('mtn', 'vu')]
        dist_all_permutations = list(itertools.product(*dist_substitution_list))

        query = build_query_distinctive(dist_all_permutations)

        print("Distinctive query: ", query)

        # This section depends on Synonyms API to get the substitution list:
        # for w_desc in list_desc:
        #    substitution_list= get_substitution_list(w_desc)
        #    If not substitution_list:
        #       desc_substitution_list.append(w_desc)
        #    else:
        #       desc_substitution_list.extend(substitution_list)

        #  desc_substitution_list= [w_desc if not get_substitution_list(w_desc) else get_substitution_list(w_desc) for w_desc in list_desc]

        desc_substitution_list:  ['bar', 'bistro', 'breakfast', 'buffet', 'cabaret', 'cafe', 'cantina', 'cappuccino', 'chai', 'coffee', 'commissary', 'cuisine', \
                                  'deli', 'dhaba', 'dine', 'diner', 'dining', 'eat', 'eater', 'eats', 'edible', 'espresso', 'expresso', 'food', 'galley', \
                                  'gastropub', 'grill', 'java', 'kitchen', 'latte', 'lounge', 'pizza', 'pizzeria', 'pub', 'publichouse', 'restaurant', 'roast', \
                                  'sandwich', 'snack', 'snax', 'socialhouse', 'steak', 'sub', 'sushi', 'takeout', 'taphouse', 'taverna', 'tea', 'tiffin', \
                                  'trattoria', 'treat', 'treatery', 'convenience', 'food', 'grocer', 'grocery', 'market', 'mart', 'shop', 'store', 'variety', \
                                  'growers']

        query = build_query_descriptive(desc_substitution_list, query)

        matches = pd.read_sql_query(query, cnx)

        return matches

    '''
    Override the abstract / base class method
    @return ProcedureResult
    '''

    def check_words_requiring_consent(self):
        result = ProcedureResult()
        result.is_valid = True

        if not result.is_valid:
            result.is_valid = False
            result.result_code = AnalysisResultCodes.NAME_REQUIRES_CONSENT

        return result

    '''
    Override the abstract / base class method
    @return ProcedureResult
    '''

    def check_designation(self):
        result = ProcedureResult()
        result.is_valid = True

        if not result.is_valid:
            result.is_valid = False
            result.result_code = AnalysisResultCodes.DESIGNATION_MISMATCH

        return result
