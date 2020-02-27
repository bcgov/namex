import itertools

from ..auto_analyse.abstract_name_analysis_builder import AbstractNameAnalysisBuilder, ProcedureResult

from ..auto_analyse import AnalysisResultCodes, MAX_LIMIT
from ..auto_analyse.name_analysis_utils import validate_distinctive_descriptive_lists

from namex.models.request import Request

'''
Sample builder
# TODO: What convention should we use? Nice to use _v<BuilderVersion> if it doesn't break PEP8
'''


class NameAnalysisBuilder(AbstractNameAnalysisBuilder):
    '''
    Check to see if a provided name is valid
    Override the abstract / base class method
    @return ProcedureResult
    '''

    def check_name_is_well_formed(self, list_dist, list_desc, list_none, list_name):
        result = ProcedureResult()
        result.is_valid = True

        _, _, list_incorrect_classification = validate_distinctive_descriptive_lists(list_name, list_dist, list_desc)

        if len(list_none) > 0:
            unclassified_words_list_response = []
            for idx, token in enumerate(list_name):
                if any(token in word for word in list_none):
                    unclassified_words_list_response.append(token)

            result.is_valid = False
            result.result_code = AnalysisResultCodes.CONTAINS_UNCLASSIFIABLE_WORD
            result.values = {
                'list_name': list_name or [],
                'list_none': unclassified_words_list_response
            }

        # TODO: These checks might be of use, but they don't really belong in here
        # if list_incorrect_classification:
        #    result.is_valid = False
        #    result.result_code = AnalysisResultCodes.INCORRECT_CATEGORY
        #    result.values = list_incorrect_classification
        # elif not list_all == list_name:
        #    reverse_order_list = []
        #    for idx, (token_dist_desc, token_name) in enumerate(zip(list_all, list_name)):
        #        if token_dist_desc != token_name:
        #            reverse_order_list.append({idx: token_name})

        #    result.is_valid = False
        #    result.result_code = AnalysisResultCodes.REVERSE_ORDER
        #    result.values = reverse_order_list
        elif len(list_dist) < 1:
            result.is_valid = False
            result.result_code = AnalysisResultCodes.ADD_DISTINCTIVE_WORD
            result.values = list_name

        elif len(list_desc) < 1:
            result.is_valid = False
            result.result_code = AnalysisResultCodes.ADD_DESCRIPTIVE_WORD
            result.values = {
                'list_name': list_name or [],
                'list_dist': list_dist or []
            }

        elif len(list_name) > MAX_LIMIT:
            result.is_valid = False
            result.result_code = AnalysisResultCodes.TOO_MANY_WORDS

        return result

    '''
    Add unclassified words to distinctive and descriptive list
    Override the abstract / base class method
    @return list_dist, list_desc
    '''
    def handle_unclassified_words(self, list_dist, list_desc, list_none, list_name):
        idx_dist = -1
        idx_desc = -1
        for word in list_name:
            if word in list_none:
                idx_dist += 1
                idx_desc += 1
                list_dist.insert(idx_dist, word)
                list_desc.insert(idx_desc, word)
            else:
                try:
                    idx_dist = list_dist.index(word)
                    idx_desc = list_desc.index(word)
                except ValueError:
                    pass

        return list_dist, list_desc

    '''
    Override the abstract / base class method
    @return ProcedureResult
    '''

    def check_words_to_avoid(self, list_name, name):
        result = ProcedureResult()
        result.is_valid = True

        # TODO: Arturo plz check the word against the list, provide it as an input for get_virtual_word_condition_service().get_words_to_avoid()
        all_words_to_avoid_list = self.get_virtual_word_condition_service().get_words_to_avoid()
        words_to_avoid_list = []

        for words_to_avoid in all_words_to_avoid_list:
            if words_to_avoid.lower() in name.lower():
                words_to_avoid_list.append(words_to_avoid.lower())

        words_to_avoid_list_response = []

        for idx, token in enumerate(list_name):
            if any(token in word for word in words_to_avoid_list):
                words_to_avoid_list_response.append(token)

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

    def search_conflicts(self, list_dist, list_desc):
        syn_svc = self.get_synonym_service()

        result = ProcedureResult()
        result.is_valid = False
        matches_response = []  # Contains all the conflicts from database
        most_similar_names = []
        dict_highest_counter = {}
        dict_highest_detail = {}
        response = {}

        for w_dist, w_desc in zip(list_dist, list_desc):
            dist_substitution_list = []
            desc_synonym_list = []
            dist_all_permutations = []

            dist_substitution_list = syn_svc.get_all_substitutions_synonyms(w_dist)
            dist_all_permutations.append(list(itertools.product(*dist_substitution_list)))

            # Inject distinctive section in query
            for element in dist_all_permutations:
                query = Request.get_query_distinctive(element, len(element[0]))

            desc_synonym_list = syn_svc.get_all_substitutions_synonyms(w_desc, False)

            desc_synonym_dict = self.get_synonym_service().get_all_substitutions_synonyms(w_desc, False)
            desc_synonym_list = desc_synonym_dict.values()
            # Inject descriptive section into query, execute and add matches to list
            if desc_synonym_list:
                query = Request.get_query_descriptive(desc_synonym_list, query)
                matches = Request.get_conflicts(query)
                matches_response.extend([val.pop() for i, val in enumerate(matches.values.tolist())])
                matches_response = list(dict.fromkeys(matches_response))
                dict_highest_counter, dict_highest_detail = self.get_most_similar_names(dict_highest_counter,
                                                                                        dict_highest_detail,
                                                                                        matches_response, w_dist,
                                                                                        w_desc, list_name, name)

        most_similar_names.extend(
            list({k for k, v in
                  sorted(dict_highest_counter.items(), key=lambda item: (-item[1], item[0]))[0:MAX_MATCHES_LIMIT]}))

        for element in most_similar_names:
            response.update({element: dict_highest_detail.get(element, {})})

        if response:
            result.is_valid = False
            result.result_code = AnalysisResultCodes.CORPORATE_CONFLICT
            result.values = response
        else:
            result.is_valid = True
            result.result_code = AnalysisResultCodes.VALID_NAME
            result.values = []

        return result

    '''
    Override the abstract / base class method
    @return ProcedureResult
    '''

    def check_words_requiring_consent(self, list_name, name):
        result = ProcedureResult()
        result.is_valid = True

        all_words_consent_list = self.get_virtual_word_condition_service().get_words_requiring_consent()
        words_consent_list = []

        for words_consent in all_words_consent_list:
            if words_consent.lower() in name.lower():
                words_consent_list.append(words_consent.lower())

        words_consent_list_response = []

        for idx, token in enumerate(list_name):
            if any(token in word for word in words_consent_list):
                words_consent_list_response.append(token)

        if words_consent_list_response:
            result.is_valid = False
            result.result_code = AnalysisResultCodes.NAME_REQUIRES_CONSENT
            result.values = words_consent_list_response

        return result

    '''
    Override the abstract / base class method
    @return ProcedureResult
    '''

    def check_designation(self, list_name, entity_type_user, all_designations, wrong_designation_place, all_designations_user):
        result = ProcedureResult()
        result.is_valid = True

        mismatch_entity_designation_list = []
        mismatch_wrong_designation_place = []
        for idx, token in enumerate(list_name):
            if any(token in designation for designation in all_designations):
                if token not in all_designations_user:
                    mismatch_entity_designation_list.append({idx: token.upper()})

        if wrong_designation_place:
            for idx, token in enumerate(list_name):
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
    '''

    def check_word_special_use(self, list_name, name):
        result = ProcedureResult()
        result.is_valid = True

        all_word_special_use_list = self.get_virtual_word_condition_service().get_word_special_use()
        word_special_use_list = []

        for words_special in all_word_special_use_list:
            if words_special.lower() in name.lower():
                word_special_use_list.append(words_special.lower())

        word_special_use_list_response = []

        for idx, token in enumerate(list_name):
            if any(token in word for word in word_special_use_list):
                word_special_use_list_response.append(token)

        if word_special_use_list_response:
            result.is_valid = False
            result.result_code = AnalysisResultCodes.WORD_SPECIAL_USE
            result.values = word_special_use_list_response

        return result
