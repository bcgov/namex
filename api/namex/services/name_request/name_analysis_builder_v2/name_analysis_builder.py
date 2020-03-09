import itertools

from . import porter
from ..auto_analyse.abstract_name_analysis_builder import AbstractNameAnalysisBuilder, ProcedureResult

from ..auto_analyse import AnalysisResultCodes, MAX_LIMIT, MAX_MATCHES_LIMIT
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
    Override the abstract / base class method
    @return ProcedureResult
    '''

    def check_words_to_avoid(self, list_name, name):
        result = ProcedureResult()
        result.is_valid = True

        # TODO: Arturo plz check the word against the list, provide it as an input for word_condition_service.get_words_to_avoid()
        all_words_to_avoid_list = self.word_condition_service.get_words_to_avoid()
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
            result.result_code = AnalysisResultCodes.WORDS_TO_AVOID
            result.values = {
                'list_name': list_name,
                'list_avoid': words_to_avoid_list_response
            }

        return result

    '''
    Override the abstract / base class method
    Input: list_dist = ['MOUNTAIN', 'VIEW']
           list_desc = ['FOOD', 'GROWERS']
    @return ProcedureResult
    '''

    def search_conflicts(self, list_dist_words, list_desc_words, list_name, name):
        syn_svc = self.synonym_service

        result = ProcedureResult()
        result.is_valid = False
        matches_response = []  # Contains all the conflicts from database
        most_similar_names = []
        dict_highest_counter = {}
        dict_highest_detail = {}
        response = {}

        for w_dist, w_desc in zip(list_dist_words, list_desc_words):
            dist_substitution_list = []
            desc_synonym_list = []
            dist_all_permutations = []

            dist_substitution_dict = syn_svc.get_all_substitutions_synonyms(w_dist)
            dist_substitution_list = dist_substitution_dict.values()
            dist_all_permutations.append(list(itertools.product(*dist_substitution_list)))

            # Inject distinctive section in query
            for element in dist_all_permutations:
                query = Request.get_query_distinctive(element, len(element[0]))

            desc_synonym_dict = syn_svc.get_all_substitutions_synonyms(w_desc, False)
            desc_synonym_list = desc_synonym_dict.values()

            desc_synonym_dict = syn_svc.get_all_substitutions_synonyms(w_desc, False)
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
            result.values = {
                'list_name': list_name,
                'list_dist': list_dist_words,
                'list_desc': list_desc_words,
                'list_conflicts': response
            }
        else:
            result.is_valid = True
            result.result_code = AnalysisResultCodes.VALID_NAME
            result.values = []
        return result

    def search_exact_match(self, preprocess_name, list_name):
        result = ProcedureResult()
        result.is_valid = False
        matches_response = []  # Contains all the conflicts from database
        response = {}

        query = Request.build_query_exact_match(preprocess_name)
        exact_match = Request.get_conflicts(query)
        exact_match_response = exact_match.values.tolist()

        if exact_match_response:
            result.is_valid = False
            result.result_code = AnalysisResultCodes.CORPORATE_CONFLICT
            result.values = {
                'list_name': list_name,
                'list_dist': None,
                'list_desc': None,
                'list_conflicts': exact_match
            }
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

        all_words_consent_list = self.word_condition_service.get_words_requiring_consent()
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
            result.values = {
                'list_name': list_name,
                'list_consent': words_consent_list_response
            }

        return result

    '''
    Override the abstract / base class method
    list_name: original name tokenized
    entity_type_user: Entity type typed u user in UI
    all_designations: All Designations found in name (either misplaced or not)
    wrong_designation_place: Designations found in name in wrong place
    all_designations_user: All designations for the entity type typed by the user. 
    @return ProcedureResult
    '''

    def check_designation(self, list_name, entity_type_user, all_designations, wrong_designation_place,
                          misplaced_designation_any, misplaced_designation_end, all_designations_user):
        result = ProcedureResult()
        result.is_valid = True

        mismatch_entity_designation_list = []
        # mismatch_wrong_designation_place = []
        for idx, token in enumerate(list_name):
            if any(token in designation for designation in all_designations):
                if token not in all_designations_user:
                    mismatch_entity_designation_list.append(token.upper())
        '''
        if wrong_designation_place:
            for idx, token in enumerate(list_name):
                if any(token in wrong_designation for wrong_designation in wrong_designation_place):
                    mismatch_wrong_designation_place.append({idx: token.upper()})
        '''
        if mismatch_entity_designation_list or wrong_designation_place:
            result.is_valid = False
            result.result_code = AnalysisResultCodes.DESIGNATION_MISMATCH
            result.values = {
                'incorrect_designations': mismatch_entity_designation_list,
                'correct_designations': all_designations_user,
                'misplaced_any_designation': misplaced_designation_any,
                'misplaced_end_designation': misplaced_designation_end
            }

        return result

    '''
    Override the abstract / base class method
    @return ProcedureResult
    '''

    def check_word_special_use(self, list_name, name):
        result = ProcedureResult()
        result.is_valid = True

        all_word_special_use_list = self.word_condition_service.get_word_special_use()
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
            result.values = {
                'list_name': list_name,
                'list_special': word_special_use_list_response
            }

        return result

    def get_most_similar_names(self, dict_highest_counter, dict_highest_detail, matches, list_dist, list_desc,
                               list_name, name):
        syn_svc = self.synonym_service

        if matches:
            dist_substitution_dict = syn_svc.get_all_substitutions_synonyms(list_dist)
            dist_substitution_list = dist_substitution_dict.values()
            dist_substitution_list = [item for sublist in dist_substitution_list for item in sublist]

            desc_substitution_dict = syn_svc.get_all_substitutions_synonyms(list_desc, False)
            desc_substitution_list = desc_substitution_dict.values()
            desc_substitution_list = [item for sublist in desc_substitution_list for item in sublist]

            all_substitutions = dist_substitution_list + desc_substitution_list

            dict_matches_counter = {}
            dict_matches_words = {}
            for match in matches:
                match_list = match.split()
                counter = 0
                word_n = 0
                for word in match_list:
                    word_n += 1
                    if porter.stem(word.lower()) in all_substitutions:
                        counter += 1
                dict_matches_counter.update({match: counter / word_n})

            dict_matches_words.update(
                self.get_details_most_similar(list(dict_matches_counter), dist_substitution_dict,
                                              desc_substitution_dict))
            # Get two highest scores (values) and shortest names (key)
            dict_highest_counter.update({k: v for k, v in
                                         sorted(dict_matches_counter.items(), key=lambda item: (-item[1], item[0]))[
                                         0:MAX_MATCHES_LIMIT]})

            for k in dict_highest_counter.keys():
                dict_highest_detail.update({k: dict_matches_words.get(k)})

        return dict_highest_counter, dict_highest_detail

    def get_details_most_similar(self, list_response, dist_substitution_dict, desc_substitution_dict):
        dict_words_matches = {}
        dict_detail_matches = {}
        for name in list_response:
            name_list = name.split()
            for word in name_list:
                dist_values = dist_substitution_dict.get(word.lower())
                desc_values = desc_substitution_dict.get(word.lower())
                if dist_values is not None:
                    dict_words_matches.update({word.lower(): dist_values})
                if desc_values is not None:
                    dict_words_matches.update({word.lower(): desc_values})
            dict_detail_matches.update({name: dict_words_matches})

        return dict_detail_matches
