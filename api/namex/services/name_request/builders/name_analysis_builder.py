import re

from . import porter
from ..auto_analyse.abstract_name_analysis_builder import AbstractNameAnalysisBuilder, ProcedureResult

from ..auto_analyse import AnalysisIssueCodes, MAX_LIMIT, MAX_MATCHES_LIMIT
from ..auto_analyse.name_analysis_utils import get_all_substitutions

from namex.models.request import Request
from ..auto_analyse.protected_name_analysis import ProtectedNameAnalysisService

from namex.utils.common import parse_dict_of_lists, get_plural_singular_name

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

    def check_name_is_well_formed(self, list_dist, list_desc, list_name, list_original_name):
        result = ProcedureResult()
        result.is_valid = True

        # list_name contains the clean name. For instance, the name 'ONE TWO THREE CANADA' is just 'CANADA'. Then,
        # the original name should be passed to get the correct index when reporting issues to front end.
        if list_name.__len__() == 0:
            # If we have no words in our name, obviously we need to add a distinctive... this is kind of redundant as
            # we shouldn't have a name with no words but we still need to handle the case in our API
            result = ProcedureResult()
            result.is_valid = False
            result.result_code = AnalysisIssueCodes.ADD_DISTINCTIVE_WORD
            result.values = {
                'list_original': [],
                'list_name': [],
                'list_dist': []
            }
        elif list_name.__len__() == 1:
            # If there's only one word and it's distinctive, we need to add a descriptive word
            if list_dist.__len__() == 1:
                result = ProcedureResult()
                result.is_valid = False
                result.result_code = AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD
                result.values = {
                    'list_original': list_original_name or [],
                    'list_name': list_name or [],
                    'list_dist': list_dist or []
                }
            else:
                result = ProcedureResult()
                result.is_valid = False
                result.result_code = AnalysisIssueCodes.ADD_DISTINCTIVE_WORD
                result.values = {
                    'list_original': list_original_name or [],
                    'list_name': list_name or [],
                    'list_dist': list_dist or []
                }
        else:
            if list_dist.__len__() == 0:
                result = ProcedureResult()
                result.is_valid = False
                result.result_code = AnalysisIssueCodes.ADD_DISTINCTIVE_WORD
                result.values = {
                    'list_original': list_original_name or [],
                    'list_name': list_name or [],
                    'list_dist': list_dist or []
                }
            elif list_desc.__len__() == 0:
                result = ProcedureResult()
                result.is_valid = False
                result.result_code = AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD
                result.values = {
                    'list_original': list_original_name or [],
                    'list_name': list_name or [],
                    'list_dist': list_dist or []
                }

        return result

    '''
    Override the abstract / base class method.
    @return ProcedureResult
    '''

    def check_word_limit(self, list_name):
        result = ProcedureResult()
        result.is_valid = True

        length_name = len(list_name)
        if length_name > MAX_LIMIT:
            result = ProcedureResult()
            result.is_valid = False
            result.result_code = AnalysisIssueCodes.TOO_MANY_WORDS

            result.values = {
                'list_name': list_name,
                'length_name': length_name
            }

        return result

    '''
    Override the abstract / base class method.
    @return ProcedureResult
    '''

    def check_unclassified_words(self, list_name, list_none):
        result = ProcedureResult()
        result.is_valid = True
        if list_none.__len__() > 0:
            unclassified_words_list_response = []
            for idx, token in enumerate(list_name):
                if not token.isdigit() and any(token in word for word in list_none):
                    unclassified_words_list_response.append(token)

            if unclassified_words_list_response:
                result = ProcedureResult()
                result.is_valid = False
                result.result_code = AnalysisIssueCodes.CONTAINS_UNCLASSIFIABLE_WORD

                result.values = {
                    'list_name': list_name or [],
                    'list_none': unclassified_words_list_response
                }

        return result

    '''
    Override the abstract / base class method.
    @return ProcedureResult
    '''

    def check_words_to_avoid(self, list_name, name):
        result = ProcedureResult()
        result.is_valid = True

        # TODO: Arturo plz check the word against the list, provide it as an input for word_condition_service.get_words_to_avoid()
        all_words_to_avoid_list = self.word_condition_service.get_words_to_avoid()
        all_words_to_avoid_list = [word.lower() for word in all_words_to_avoid_list]
        all_words_to_avoid_list.sort(key=len, reverse=True)

        word_avoid_alternators = '|'.join(map(re.escape, all_words_to_avoid_list))
        regex = re.compile(r'(?<!\w)({0})(?!\w)'.format(word_avoid_alternators))
        word_avoid_compound_list = regex.findall(name.lower())

        word_avoid_tokenized_list = [element.split(' ') for element in word_avoid_compound_list]
        word_avoid_tokenized_list = [item for sublist in word_avoid_tokenized_list for item in sublist]

        if word_avoid_tokenized_list.__len__() > 0:
            result.is_valid = False
            result.result_code = AnalysisIssueCodes.WORDS_TO_AVOID
            result.values = {
                'list_name': list_name,
                'list_avoid': word_avoid_tokenized_list,
                'list_avoid_compound': word_avoid_compound_list
            }

        return result

    '''
    Override the abstract / base class method
    Input: list_dist = ['MOUNTAIN', 'VIEW']
           list_desc = ['FOOD', 'GROWERS']
    @return ProcedureResult
    '''

    def search_conflicts(self, list_dist_words, list_desc_words, list_name, name):
        result = ProcedureResult()
        result.is_valid = False
        all_matches_list = []  # Contains all the conflicts from database
        most_similar_names = []
        dict_highest_counter = {}
        dict_highest_detail = {}
        response = {}

        for w_dist, w_desc in zip(list_dist_words, list_desc_words):
            dict_highest_counter, dict_highest_detail, similar_matches = self.get_conflicts(
                dict_highest_counter, dict_highest_detail, w_dist, w_desc, list_name, name
            )

            all_matches_list.extend(similar_matches)
            # If exact match is found stop searching and return response
            if any(score == 1.0 for score in list(dict_highest_counter.values())):
                break

        most_similar_names.extend(
            list({k for k, v in
                  sorted(dict_highest_counter.items(), key=lambda item: (-item[1], len(item[0])))[
                  0:MAX_MATCHES_LIMIT]}))

        if most_similar_names:
            response = self.prepare_response(all_matches_list, most_similar_names, dict_highest_detail)

        if response:
            result.is_valid = False
            result.result_code = AnalysisIssueCodes.CORPORATE_CONFLICT
            result.values = {
                'list_name': list_name,
                'list_dist': list_dist_words,
                'list_desc': list_desc_words,
                'list_conflicts': response['names'],
                'corp_num': response['corp_num'],
                'consumption_date': response['consumption_date']
            }
        else:
            result.is_valid = True
            result.result_code = AnalysisIssueCodes.CHECK_IS_VALID
            result.values = []
        return result

    def get_conflicts(self, dict_highest_counter, dict_highest_detail, w_dist, w_desc, list_name, name):
        syn_svc = self.synonym_service
        dist_substitution_list = []
        desc_synonym_list = []
        all_matches_list = []

        all_dist_substitutions_synonyms = syn_svc.get_all_substitutions_synonyms(
            words=w_dist,
            words_are_distinctive=True
        ).data

        dist_substitution_dict = parse_dict_of_lists(all_dist_substitutions_synonyms)
        dist_substitution_list = dist_substitution_dict.values()

        all_desc_substitutions_synonyms = syn_svc.get_all_substitutions_synonyms(
            words=w_desc,
            words_are_distinctive=False
        ).data

        desc_synonym_dict = parse_dict_of_lists(all_desc_substitutions_synonyms)
        desc_synonym_list = desc_synonym_dict.values()
        for dist in dist_substitution_list:
            criteria = Request.get_general_query()
            criteria = Request.get_query_distinctive_descriptive(dist, criteria, True)
            # Inject descriptive section into query, execute and add matches to list
            for desc in desc_synonym_list:
                matches = Request.get_query_distinctive_descriptive(desc, criteria)
                dict_highest_counter, dict_highest_detail, matches_similar = self.get_most_similar_names(dict_highest_counter,
                                                                                        dict_highest_detail,
                                                                                        matches, w_dist,
                                                                                        w_desc, list_name, name)
                all_matches_list.extend(matches_similar)
                if any(score == 1.0 for score in list(dict_highest_counter.values())):
                    return dict_highest_counter, dict_highest_detail, all_matches_list

        return dict_highest_counter, dict_highest_detail, all_matches_list

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
        words_consent_dict = {}
        word_consent_original_list=[]
        name_singular_plural_list = list(set(get_plural_singular_name(name)))

        for words_consent in all_words_consent_list:
            for name_sin_plural in name_singular_plural_list:
                if re.search(r'\b{}\b'.format(re.escape(words_consent.lower())), name_sin_plural.lower()):
                    words_consent_dict.update(self.get_position_word_consent(words_consent, name_sin_plural))
                    word_consent_original_list.append(words_consent)
                    break

        words_consent_list_response = []
        for key in sorted(words_consent_dict):
            words_consent_list_response.append(list_name[key])

        if words_consent_list_response:
            result.is_valid = False
            result.result_code = AnalysisIssueCodes.NAME_REQUIRES_CONSENT

            result.values = {
                'list_name': list_name,
                'list_consent': words_consent_list_response,
                'list_consent_original': word_consent_original_list
            }

        return result

    def get_position_word_consent(self, words_consent, name_sin_plural):
        word_consent_tokenized = words_consent.lower().split()
        name_sin_plur_tokenized = name_sin_plural.split()
        words_consent_dict = {}
        for word in word_consent_tokenized:
            if word.lower() in name_sin_plural:
                idx = name_sin_plur_tokenized.index(word.lower())
                words_consent_dict[idx] = word

        return words_consent_dict

    def check_designation_existence(self, list_name, all_designations, all_designations_user):
        result = ProcedureResult()
        result.is_valid = True

        if not all_designations:
            result.is_valid = False
            result.result_code = AnalysisIssueCodes.DESIGNATION_NON_EXISTENT
            result.values = {
                'list_name': list_name,
                'correct_designations': all_designations_user
            }

        return result

    '''
    Override the abstract / base class method
    list_name: original name tokenized by designation. For instance, designation composed of many words is tokenized as one.
    entity_type_user: Entity type typed by user. 'CR' by default
    all_designations: All Designations found in name (either misplaced or not)
    all_designations_user: All designations for the entity type typed by the user. 
    @return ProcedureResult
    '''

    def check_designation_mismatch(self, list_name, entity_type_user, all_designations, all_designations_user):
        result = ProcedureResult()
        result.is_valid = True

        mismatch_entity_designation_list = []
        for idx, token in enumerate(list_name):
            if token in all_designations and token not in all_designations_user:
                mismatch_entity_designation_list.append(token)

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
    list_name: original name tokenized by designation. For instance, designation composed of many words is tokenized as one.
    designation_end_list: Correct end designations
    misplaced_designation_end: Misplaced end designations
    @return ProcedureResult
    '''
    def check_end_designation_more_than_once(self, list_name, designation_end_list, misplaced_designation_end):
        result = ProcedureResult()
        result.is_valid = True

        if designation_end_list.__len__() > 1 or misplaced_designation_end.__len__() > 1:
            correct_end_designations = designation_end_list + list(
                set(misplaced_designation_end) - set(designation_end_list))
            corrected_end_designations_sorted = []

            for word in list_name:
                if word in correct_end_designations:
                    corrected_end_designations_sorted.append(word)

            result.is_valid = False
            result.result_code = AnalysisIssueCodes.END_DESIGNATION_MORE_THAN_ONCE
            result.values = {
                'list_name': list_name,
                'correct_end_designations': corrected_end_designations_sorted
            }

        return result

    '''
    Override the abstract / base class method
    Just <end> designation can be misplaced in other position, it can be at the beginning, middle or before end in the name
    Note: <any> designation can be anywhere in the name, so to be misplaced is not possible.
    @return ProcedureResult
    '''

    def check_designation_misplaced(self, list_name, misplaced_designation_end):
        result = ProcedureResult()
        result.is_valid = True

        if misplaced_designation_end:
            result.is_valid = False
            result.result_code = AnalysisIssueCodes.DESIGNATION_MISPLACED
            result.values = {
                'list_name': list_name,
                'misplaced_end_designation': misplaced_designation_end
            }

        return result

    '''
    Override the abstract / base class method
    @return ProcedureResult
    '''

    def check_word_special_use(self, list_name, name_processed):
        result = ProcedureResult()
        result.is_valid = True

        all_word_special_use_list = self.word_condition_service.get_word_special_use()
        all_word_special_use_list = [word.lower() for word in all_word_special_use_list]
        all_word_special_use_list.sort(key=len, reverse=True)

        word_special_alternators = '|'.join(map(re.escape, all_word_special_use_list))
        regex = re.compile(r'(?<!\w)({0})(?!\w)'.format(word_special_alternators))
        word_special_compound_list = regex.findall(name_processed.lower())

        word_special_tokenized_list = [element.split(' ') for element in word_special_compound_list]
        word_special_tokenized_list = [item for sublist in word_special_tokenized_list for item in sublist if item]

        if word_special_tokenized_list.__len__() > 0:
            result.is_valid = False
            result.result_code = AnalysisIssueCodes.WORD_SPECIAL_USE
            result.values = {
                'list_name': list_name,
                'list_special': word_special_tokenized_list,
                'list_special_compound': word_special_compound_list
            }

        return result

    def get_most_similar_names(self, dict_highest_counter, dict_highest_detail, matches, list_dist, list_desc,
                               list_name, name):
        selected_matches = []
        if matches:
            syn_svc = self.synonym_service
            service = ProtectedNameAnalysisService()

            all_subs_dict, dist_subs_dict, desc_subs_dict = get_all_substitutions(syn_svc, list_dist, list_desc,
                                                                                  list_name)
            list_name_stem = [porter.stem(name.lower()) for name in list_name]
            length_original = len(list_name)

            dict_matches_counter, dict_matches_words = {}, {}

            for match in matches:
                np_svc = service.name_processing_service
                np_svc.set_name(match.name)
                # TODO: Get rid of this when done refactoring!
                match_list = np_svc.name_tokens
                counter = 0
                for idx, word in enumerate(match_list):
                    if length_original > idx and word.lower() == list_name[idx]:
                        counter += 1
                    elif length_original > idx and porter.stem(word.lower()) == list_name_stem[idx]:
                        counter += 0.95
                    elif length_original > idx and porter.stem(word.lower()) in list(all_subs_dict.values())[idx]:
                        counter += 0.9
                    elif word.lower() in list_name:
                        counter += 0.8
                    elif porter.stem(word.lower()) in list_name_stem:
                        counter += 0.7
                    elif porter.stem(word.lower()) in all_subs_dict.values():
                        counter += 0.6
                    else:
                        counter -= 0.2

                similarity = round(counter / length_original, 2)
                if similarity >= 0.67:
                    dict_matches_counter.update({match.name: similarity})
                    selected_matches.append(match)
                    if similarity == 1.0:
                        break

            if dict_matches_counter:
                dict_matches_words.update(
                    self.get_details_most_similar(list(dict_matches_counter), dist_subs_dict,
                                                  desc_subs_dict))
                # Get highest score (values) and shortest names (key)
                dict_highest_counter.update({k: v for k, v in
                                             sorted(dict_matches_counter.items(), key=lambda item: (-item[1], item[0]))[
                                             0:MAX_MATCHES_LIMIT]})

                for k in dict_highest_counter.keys():
                    dict_highest_detail.update({k: dict_matches_words.get(k)})

        return dict_highest_counter, dict_highest_detail, selected_matches

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

    def prepare_response(self, all_matches_list, most_similar_names, dict_highest_detail):
        conflict_name, corp_num, consumption_date = {}, [], []
        matches_list, response = [], []

        matches_list = [match for match in all_matches_list if match not in matches_list]

        for similar_name in most_similar_names:
            conflict_name.update({similar_name: dict_highest_detail.get(similar_name, {})})
            for record in matches_list:
                if record.name == similar_name:
                    corp_num.append(record.corpNum)
                    consumption_date.append(record.consumptionDate)

        if conflict_name:
            response = {'names': conflict_name,
                        'corp_num': corp_num,
                        'consumption_date': consumption_date,
                        }

        return response
