import itertools

import collections

from . import porter
from ..auto_analyse.abstract_name_analysis_builder import AbstractNameAnalysisBuilder, ProcedureResult

from ..auto_analyse import AnalysisIssueCodes, MAX_LIMIT, MAX_MATCHES_LIMIT
from ..auto_analyse.name_analysis_utils import validate_distinctive_descriptive_lists

from namex.models.request import Request
from ..auto_analyse.protected_name_analysis import ProtectedNameAnalysisService

'''
Sample builder
# TODO: What convention should we use? Nice to use _v<BuilderVersion> if it doesn't break PEP8
'''


class NameAnalysisBuilder(AbstractNameAnalysisBuilder):
    '''
    Check to see if a provided name is valid
    Override the abstract / base class method
    @return ProcedureResult[] An array of procedure results
    '''

    def check_name_is_well_formed(self, list_dist, list_desc, list_none, list_name, list_original_name):
        results = []
        # TODO: We're doing two checks for name is well formed, that should probably not be the case

        # list_name = ['victoria', 'abc', 'view', 'book']
        # list_dist = ['victoria', 'book']
        # list_desc = ['victoria', 'abc', 'view']
        # Returns words in wrong classification following distinctive | descriptive: [{book:3}]
        _, _, list_incorrect_classification = validate_distinctive_descriptive_lists(list_name, list_dist, list_desc)

        # First, check to make sure the name doesn't have too many words
        if len(list_name) > MAX_LIMIT:
            result = ProcedureResult()
            result.is_valid = False
            result.result_code = AnalysisIssueCodes.TOO_MANY_WORDS

            results.append(result)

        # Next, we check for unclassified words
        if len(list_none) > 0:
            unclassified_words_list_response = []
            for idx, token in enumerate(list_name):
                if any(token in word for word in list_none):
                    unclassified_words_list_response.append(token)

            result = ProcedureResult()
            result.is_valid = False
            result.result_code = AnalysisIssueCodes.CONTAINS_UNCLASSIFIABLE_WORD
            result.values = {
                'list_name': list_name or [],
                'list_none': unclassified_words_list_response
            }

            results.append(result)

        # Now that too many words and unclassified words are handled, handle distinctive and descriptive issues
        result = None

        # list_name contains the clean name. For instance, the name 'ONE TWO THREE CANADA' is just 'CANADA'. Then,
        # the original name should be passed to get the correct index when reporting issues to front end.

        if len(list_name) == 0:
            # If we have no words in our name, obviously we need to add a distinctive... this is kind of redundant as
            # we shouldn't have a name with no words but we still need to handle the case in our API
            result = ProcedureResult()
            result.is_valid = False
            result.result_code = AnalysisIssueCodes.ADD_DISTINCTIVE_WORD
            result.values = {
                'list_name': [],
                'list_dist': []
            }
        elif len(list_name) == 1:
            # If there's only one word and it's distinctive, we need to add a descriptive word
            if len(list_dist) == 1:
                result = ProcedureResult()
                result.is_valid = False
                result.result_code = AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD
                result.values = {
                    'list_name': list_original_name or [],
                    'list_dist': list_dist or []
                }
            else:
                result = ProcedureResult()
                result.is_valid = False
                result.result_code = AnalysisIssueCodes.ADD_DISTINCTIVE_WORD
                result.values = {
                    'list_name': list_original_name or [],
                    'list_dist': list_dist or []
                }
        else:
            if len(list_dist) == 0:
                result = ProcedureResult()
                result.is_valid = False
                result.result_code = AnalysisIssueCodes.ADD_DISTINCTIVE_WORD
                result.values = {
                    'list_name': list_original_name or [],
                    'list_dist': []
                }
            elif len(list_desc) == 0:
                result = ProcedureResult()
                result.is_valid = False
                result.result_code = AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD
                result.values = {
                    'list_name': list_original_name or [],
                    'list_dist': list_dist or []
                }
                # elif collections.Counter(list_dist) == collections.Counter(list_desc):
                # If there's more than one word and all words are both distinctive and descriptive ~~add another distinctive~~
                # Then we find all possible combinations in search_conflicts
                '''
                result = ProcedureResult()
                result.is_valid = False
                result.result_code = AnalysisIssueCodes.ADD_DISTINCTIVE_WORD
                result.values = {
                    'list_name': list_name,
                    'list_dist': []
                }
                '''

        if result:
            results.append(result)

        return results

    '''
    Override the abstract / base class method.
    
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
            result.result_code = AnalysisIssueCodes.WORDS_TO_AVOID
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

            desc_synonym_dict = syn_svc.get_all_substitutions_synonyms(w_desc, False)
            desc_synonym_list = desc_synonym_dict.values()

            # Inject distinctive section in query
            for dist in dist_substitution_list:
                criteria = Request.get_general_query()
                criteria = Request.get_query_distinctive_descriptive(dist, criteria, True)
                # Inject descriptive section into query, execute and add matches to list
                for desc in desc_synonym_list:
                    matches = Request.get_query_distinctive_descriptive(desc, criteria)
                    matches_response = list(dict.fromkeys(matches))
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
            result.result_code = AnalysisIssueCodes.CORPORATE_CONFLICT
            result.values = {
                'list_name': list_name,
                'list_dist': list_dist_words,
                'list_desc': list_desc_words,
                'list_conflicts': response
            }
        else:
            result.is_valid = True
            result.result_code = AnalysisIssueCodes.CHECK_IS_VALID
            result.values = []
        return result

    def search_exact_match(self, preprocess_name, list_name):
        result = ProcedureResult()
        result.is_valid = False

        criteria = Request.get_general_query()
        exact_match = Request.get_query_exact_match(criteria, preprocess_name)

        if exact_match:
            result.is_valid = False
            result.result_code = AnalysisIssueCodes.CORPORATE_CONFLICT
            result.values = {
                'list_name': list_name,
                'list_dist': None,
                'list_desc': None,
                'list_conflicts': exact_match
            }
        else:
            result.is_valid = True
            result.result_code = AnalysisIssueCodes.CHECK_IS_VALID
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
            result.result_code = AnalysisIssueCodes.NAME_REQUIRES_CONSENT
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
    all_designations_user: All designations for the entity type typed by the user. 
    @return ProcedureResult
    '''

    def check_designation_mismatch(self, list_name, entity_type_user, all_designations, all_designations_user):
        result = ProcedureResult()
        result.is_valid = True

        mismatch_entity_designation_list = []
        for idx, token in enumerate(list_name):
            if any(token in designation for designation in all_designations):
                if token not in all_designations_user:
                    mismatch_entity_designation_list.append(token.upper())

        if mismatch_entity_designation_list:
            result.is_valid = False
            result.result_code = AnalysisIssueCodes.DESIGNATION_MISMATCH
            result.values = {
                'list_name': list_name,
                'incorrect_designations': mismatch_entity_designation_list,
                'correct_designations': all_designations_user,
            }

        return result

    '''
        Override the abstract / base class method
        misplaced_designation_any, misplaced_designation_end, misplaced_designation_all
        @return ProcedureResult
        '''

    def check_designation_misplaced(self, list_name, misplaced_designation_any, misplaced_designation_end,
                                    misplaced_designation_all):
        result = ProcedureResult()
        result.is_valid = True

        if misplaced_designation_all:
            result.is_valid = False
            result.result_code = AnalysisIssueCodes.DESIGNATION_MISPLACED
            result.values = {
                'list_name': list_name,
                'misplaced_any_designation': misplaced_designation_any,
                'misplaced_end_designation': misplaced_designation_end,
                'misplaced_all_designation': misplaced_designation_all
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
            result.result_code = AnalysisIssueCodes.WORD_SPECIAL_USE
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
            all_subs_stem = [porter.stem(substitution.lower()) for substitution in all_substitutions]

            list_name_stem = [porter.stem(name.lower()) for name in list_name]
            length_original = len(list_name)

            dict_matches_counter = {}
            dict_matches_words = {}

            service = ProtectedNameAnalysisService()
            for match in matches:
                np_svc = service.name_processing_service
                np_svc.set_name(match)
                # TODO: Get rid of this when done refactoring!
                match_list = np_svc.name_tokens
                counter = 0
                for idx, word in enumerate(match_list):
                    # Compare in the same place
                    if length_original == len(match_list) and word.lower() == list_name[idx]:
                        counter += 1
                    elif length_original == len(match_list) and porter.stem(word.lower()) == list_name_stem[idx]:
                        counter += 0.95
                    elif word.lower() in list_name:
                        counter += 0.85
                    elif porter.stem(word.lower()) in list_name_stem:
                        counter += 0.75
                    elif porter.stem(word.lower()) in all_subs_stem:
                        counter += 0.7
                similarity = counter / length_original
                dict_matches_counter.update({match: similarity})

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
