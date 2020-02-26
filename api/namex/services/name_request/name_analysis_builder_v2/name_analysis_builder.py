import itertools

from . import porter
from ..auto_analyse.abstract_name_analysis_builder \
    import AbstractNameAnalysisBuilder, ProcedureResult

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

    def check_name_is_well_formed(self, list_dist, list_desc, list_name):
        result = ProcedureResult()
        result.is_valid = True

        _, _, list_incorrect_classification = validate_distinctive_descriptive_lists(list_name, list_dist, list_desc)

        if list_incorrect_classification:
            result.is_valid = False
            result.result_code = AnalysisResultCodes.INCORRECT_CATEGORY
            result.values = list_incorrect_classification
        if len(list_dist) < 1:
            result.is_valid = False
            result.result_code = AnalysisResultCodes.ADD_DISTINCTIVE_WORD
        elif len(list_desc) < 1:
            result.is_valid = False
            result.result_code = AnalysisResultCodes.ADD_DESCRIPTIVE_WORD
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

    def search_conflicts(self, list_dist, list_desc, list_name, name):
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

            dist_substitution_dict = self.get_synonym_service().get_all_substitutions_synonyms(w_dist)
            dist_substitution_list = dist_substitution_dict.values()
            dist_all_permutations.append(list(itertools.product(*dist_substitution_list)))

            # Inject distinctive section in query
            for element in dist_all_permutations:
                query = Request.get_query_distinctive(element, len(element[0]))

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
                words_consent_list_response.append({idx: token})

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
                word_special_use_list_response.append({idx: token})

        if word_special_use_list_response:
            result.is_valid = False
            result.result_code = AnalysisResultCodes.WORD_SPECIAL_USE
            result.values = word_special_use_list_response

        return result

    def get_most_similar_names(self, dict_highest_counter, dict_highest_detail, matches, list_dist, list_desc,
                               list_name, name):
        if matches:
            dist_substitution_dict = self.get_synonym_service().get_all_substitutions_synonyms(list_dist)
            dist_substitution_list = dist_substitution_dict.values()
            dist_substitution_list = [item for sublist in dist_substitution_list for item in sublist]

            desc_substitution_dict = self.get_synonym_service().get_all_substitutions_synonyms(list_desc, False)
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

    '''
    Override the abstract / base class method
    @return ProcedureResult
    @deprecated The DIRECTOR CONTROLS THE BUILD PROCESS
    '''
    '''
    def do_analysis(self, name):
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

            return ProcedureResult(is_valid=True)
    '''
