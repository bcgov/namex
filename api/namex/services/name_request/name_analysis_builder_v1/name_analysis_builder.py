import itertools
import pandas as pd
import collections
from sqlalchemy import create_engine

from namex.services.name_request.auto_analyse.name_analysis_utils import build_query_distinctive, \
    build_query_descriptive, get_substitution_list, get_synonym_list, get_stop_word_list, get_fr_designation_end_list, \
    get_prefix_list, clean_name_words, get_classification, \
    data_frame_to_list, get_words_to_avoid, get_words_requiring_consent, \
    get_en_LL_entity_type_end_designation, get_en_RLC_entity_type_end_designation, \
    get_en_CR_entity_type_end_designation, get_en_BC_entity_type_end_designation, get_en_UL_entity_type_end_designation, \
    get_en_CC_entity_type_end_designation, get_en_CC_entity_type_any_designation, \
    get_en_XCP_entity_type_any_designation, get_en_CP_entity_type_any_designation, get_entity_type_by_value, \
    get_entity_type_end_designation, get_entity_type_any_designation, get_en_designation_end_all_list, \
    get_en_designation_any_all_list, get_designation_any_in_name, get_designation_end_in_name, \
    get_designation_by_entity_type, get_wrong_place_end_designations, get_wrong_place_any_designations
from ..auto_analyse.abstract_name_analysis_builder \
    import AbstractNameAnalysisBuilder, ProcedureResult

from ..auto_analyse import AnalysisResultCodes, MAX_LIMIT

'''
Sample builder
# TODO: What convention should we use? Nice to use _v<BuilderVersion> if it doesn't break PEP8
'''


class NameAnalysisBuilder(AbstractNameAnalysisBuilder):
    POSTGRES_ADDRESS = 'localhost'
    POSTGRES_PORT = '5432'
    POSTGRES_USERNAME = 'postgres'
    POSTGRES_PASSWORD = ''
    POSTGRES_DBNAME_SYNS = 'namex-local'
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
        result.is_valid = True

        # if (len(list_desc) > 0 and len(list_dist) > 0) and (list_desc != list_dist) and (
        #        (list_dist + list_desc) == name):
        #    success = True

        # Return one of the following:
        # AnalysisResultCodes.CONTAINS_UNCLASSIFIABLE_WORD
        # AnalysisResultCodes.TOO_MANY_WORDS
        # AnalysisResultCodes.ADD_DISTINCTIVE_WORD
        # AnalysisResultCodes.ADD_DESCRIPTIVE_WORD

        if len(list_none) > 0:
            unclassified_words_list_response = []
            name_list = name.split()

            for idx, token in enumerate(name_list):
                if any(token in word for word in list_none):
                    unclassified_words_list_response.append({idx: token})

            result.is_valid = False
            result.result_code = AnalysisResultCodes.CONTAINS_UNCLASSIFIABLE_WORD
            result.value = unclassified_words_list_response
        elif len(list_dist) < 1:
            result.is_valid = False
            result.result_code = AnalysisResultCodes.ADD_DISTINCTIVE_WORD
        elif len(list_desc) < 1:
            result.is_valid = False
            result.result_code = AnalysisResultCodes.ADD_DESCRIPTIVE_WORD
        elif len(name) > MAX_LIMIT:
            result.is_valid = False
            result.result_code = AnalysisResultCodes.TOO_MANY_WORDS

        return result

    '''
    Override the abstract / base class method
    @return ProcedureResult
    '''
    def check_words_to_avoid(self, preprocessed_name):
        result = ProcedureResult()
        result.is_valid = True

        all_words_to_avoid_list = get_words_to_avoid()
        words_to_avoid_list = []

        for words_to_avoid in all_words_to_avoid_list:
            if words_to_avoid.lower() in name.lower():
                words_to_avoid_list.append(words_to_avoid)

        name_list = name.split()
        words_to_avoid_list_response = []

        for idx, token in enumerate(name_list):
            if any(token in word for word in words_to_avoid_list):
                words_to_avoid_list_response.append({idx: token})

        if words_to_avoid_list_response:
            result.is_valid = False
            result.result_code = AnalysisResultCodes.WORD_TO_AVOID
            result.values = words_to_avoid_list_response

        return result

    '''
    Override the abstract / base class method
    Input: list_dist= ['MOUNTAIN', 'VIEW']
           list_desc= ['FOOD', 'GROWERS']
    @return ProcedureResult
    '''
    def search_conflicts(self, list_dist, list_desc, cnx=create_engine(postgres_str)):
        result = ProcedureResult()
        result.is_valid = False

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

                matches_response = matches.values.tolist()
                if matches_response:
                    result.is_valid = False
                    result.result_code = AnalysisResultCodes.CORPORATE_CONFLICT
                    result.values = matches_response
                else:
                    result.is_valid = True
                    result.result_code = AnalysisResultCodes.VALID_NAME
                    result.values = []
            else:
                result.is_valid = False
                result.result_code = AnalysisResultCodes.ADD_DESCRIPTIVE_WORD
                result.values = []

        else:
            result.is_valid = False
            result.result_code = AnalysisResultCodes.ADD_DISTINCTIVE_WORD
            result.values = []

        return result

    '''
    Override the abstract / base class method
    @return ProcedureResult
    '''
    def check_words_requiring_consent(self, preprocessed_name):
        result = ProcedureResult()
        result.is_valid = True

        all_words_consent_list = get_words_requiring_consent()
        words_consent_list = []

        for words_consent in all_words_consent_list:
            if words_consent.lower() in name.lower():
                words_consent_list.append(words_consent)

        name_list = name.split()
        words_consent_list_response = []

        for idx, token in enumerate(name_list):
            if any(token in word for word in words_consent_list):
                words_consent_list_response.append({idx: token})

        if words_consent_list_response:
            result.is_valid = False
            result.result_code = AnalysisResultCodes.WORD_TO_AVOID
            result.values = words_consent_list_response

        return result

    '''
    Override the abstract / base class method
    @return ProcedureResult
    '''
    def check_designation(self, name, entity_type_end_desig_user, entity_type_any_desig_user):
        result = ProcedureResult()
        result.is_valid = True

        entity_end_designation_dict = {'RLC': get_en_RLC_entity_type_end_designation(),
                                       'LL': get_en_LL_entity_type_end_designation(),
                                       'CC': get_en_CC_entity_type_end_designation(),
                                       'UL': get_en_UL_entity_type_end_designation(),
                                       'BC': get_en_BC_entity_type_end_designation(),
                                       'CR': get_en_CR_entity_type_end_designation()}

        entity_any_designation_dict = {'CP': get_en_CP_entity_type_any_designation(),
                                       'XCP': get_en_XCP_entity_type_any_designation(),
                                       'CC': get_en_CC_entity_type_any_designation()}

        # Get all designations for entity_type as list of dictionaries key:[any|stop], value: designations
        designations_entity_type_user = get_designation_by_entity_type(entity_type_user)
        designation_any_list_user = list()
        designation_end_list_user = list()

        # Get designation_any_list_user and designation_end_list_user based on entity type typed by user
        for k, v in designations_entity_type_user.items():
            if k.lower() == 'any':
                designation_any_list_user.extend(v)
            else:
                designation_end_list_user.extend(v)

        # Get designation_any_list and designation_end_list based on company name typed by user
        designation_any_list = get_designation_any_in_name(name)
        designation_end_list = get_designation_end_in_name(name)

        wrong_designation_any_list = get_wrong_place_any_designations(name)
        wrong_designation_end_list = get_wrong_place_end_designations(name)

        wrong_designation_place = wrong_designation_any_list + wrong_designation_end_list

        # Get the entity type(s) for designations related to company name:
        entity_type_any_designation = []
        entity_type_end_designation = []
        if designation_any_list:
            entity_type_any_designation = get_entity_type_any_designation(entity_any_designation_dict,
                                                                          designation_any_list)
        if designation_end_list:
            entity_type_end_designation = get_entity_type_end_designation(entity_end_designation_dict,
                                                                          designation_end_list)
        # All possible entity types found related to company name.
        all_entity_types = [item for item, count in collections.Counter(entity_type_any_designation + entity_type_end_designation).items() if
                            count > 1]
        if not all_entity_types:
            all_entity_types = entity_type_any_designation + entity_type_end_designation

        all_designations_user = designation_any_list_user + designation_end_list_user
        all_designations = designation_any_list + designation_end_list

        name_list = name.lower().split()
        mismatch_entity_designation_list = []
        mismatch_wrong_designation_place = []
        for idx, token in enumerate(name_list):
            if any(token in designation for designation in all_designations):
                if token not in all_designations_user:
                    mismatch_entity_designation_list.append({idx: token.upper()})

        if wrong_designation_place:
            for idx, token in enumerate(name_list):
                if any(token in wrong_designation for wrong_designation in wrong_designation_place):
                    mismatch_wrong_designation_place.append({idx: token.upper()})

        if mismatch_entity_designation_list or wrong_designation_place:
            response = list()
            response.append(mismatch_wrong_designation_place)
            response.append(mismatch_entity_designation_list)
            if mismatch_entity_designation_list:
                response.append(list(map(str.upper, all_designations_user)))
            else:
                response.append(list())
            result.is_valid = False
            result.result_code = AnalysisResultCodes.DESIGNATION_MISMATCH
            result.values = response

        return result

    '''
    Override the abstract / base class method
    @return ProcedureResult
    @deprecated The DIRECTOR CONTROLS THE BUILD PROCESS
    '''
    '''def do_analysis(self, name):
        result = ProcedureResult()
        result.is_valid = False

        stop_words = get_stop_word_list()
        en_designation_any = get_en_designation_any_all_list()
        en_designation_end = get_en_designation_end_all_list()
        fr_designation_end = get_fr_designation_end_list()
        prefixes = get_prefix_list()
        cf = pd.DataFrame(columns=['word', 'word_classification'])

        preprocessed_name_list = clean_name_words(name, stop_words, en_designation_any, en_designation_end,
                                                  fr_designation_end, prefixes)

        for word in preprocessed_name_list:
            # TODO: Get classification shouldn't be done here
            classification = get_classification(word)
            new_row = {'word': word.lower().strip(), 'word_classification': classification.strip()}
            cf = cf.append(new_row, ignore_index=True)

        distinctive_list, descriptive_list, unclassified_list = data_frame_to_list(cf)

        check_name_is_well_formed = self.check_name_is_well_formed(descriptive_list, distinctive_list,
                                                                   unclassified_list, \
                                                                   preprocessed_name_list)
        # TODO: The DIRECTOR CONTROLS THE BUILD PROCESS
        if check_name_is_well_formed.is_valid:
            # preprocessed_name = ' '.join(map(str, preprocessed_name_list))
            check_words_to_avoid = self.check_words_to_avoid(name)
            check_conflicts = self.search_conflicts(distinctive_list, descriptive_list)

            if not check_conflicts:
                check_words_requiring_consent = self.check_words_requiring_consent(name)
                check_designation_mismatch = self.check_designation(name, entity_type_end_desig_user,
                                                                    entity_type_any_desig_user)

                # check_designation_mismatch = self.check_designation()
                if not check_name_is_well_formed.is_valid:
                    return check_name_is_well_formed

                if not check_words_to_avoid.is_valid:
                    return check_words_to_avoid

                if not check_conflicts.is_valid:
                    return check_conflicts

                if not check_words_requiring_consent.is_valid:
                    return check_words_requiring_consent

                if not check_designation_mismatch.is_valid:
                    return check_designation_mismatch

            else:
                return result
        else:
            return result

            return ProcedureResult(is_valid=True)'''
