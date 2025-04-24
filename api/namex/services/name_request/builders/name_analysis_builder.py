from flask import current_app
import re
import itertools
from collections import ChainMap
import warnings

import requests
from . import (
    EXACT_MATCH,
    HIGH_CONFLICT_RECORDS,
    HIGH_SIMILARITY,
    CURRENT_YEAR,
    LOWER_LIMIT_TIME,
    UPPER_LIMIT_TIME,
    EXCEPTION_YEARS,
    CURRENT_MONTH,
    CURRENT_DAY,
)
from ..auto_analyse.abstract_name_analysis_builder import AbstractNameAnalysisBuilder, ProcedureResult
from ..auto_analyse import AnalysisIssueCodes, MAX_LIMIT, MAX_MATCHES_LIMIT, porter
from ..auto_analyse.name_analysis_utils import (
    get_conflicts_same_classification,
    get_all_dict_substitutions,
    subsequences,
    remove_double_letters,
    remove_double_letters_list_dist_words,
)

from namex.models.request import Request

from namex.utils.common import parse_dict_of_lists, get_plural_singular_name
from namex.services.name_request.auto_analyse import DataFrameFields

WORD = re.compile(r'\w+')

"""
Sample builder
# TODO: What convention should we use? Nice to use _v<BuilderVersion> if it doesn't break PEP8
"""


class NameAnalysisBuilder(AbstractNameAnalysisBuilder):
    """
    Check to see if a provided name is valid
    Override the abstract / base class method
    @return ProcedureResult[] An array of procedure results
    """

    def check_name_is_well_formed(self, name_dict, list_dist, list_desc, list_name, processed_name, list_original_name):
        result = ProcedureResult()
        result.is_valid = True
        self.name_processing_service

        first_classification = None
        if name_dict:
            first_classification = next(iter(name_dict.values()))
            first_word = next(iter(name_dict))
            name_dict.pop(first_word)

        if first_classification == DataFrameFields.DISTINCTIVE.value:
            valid = self.check_descriptive(name_dict)
            if not valid:
                # if len(name_dict) > 0:
                #     result = self.check_conflict_well_formed_response(processed_name, list_original_name, list_name,
                #                                                       list_dist,
                #                                                       AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD)
                #     if result.result_code == AnalysisIssueCodes.CORPORATE_CONFLICT:
                #         return result
                # else:
                result = self.check_name_is_well_formed_response(
                    list_original_name, list_name, list_dist, AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD
                )
        else:
            result = result = self.check_name_is_well_formed_response(
                list_original_name, list_name, list_dist, AnalysisIssueCodes.ADD_DISTINCTIVE_WORD
            )
            # if result.result_code == AnalysisIssueCodes.CORPORATE_CONFLICT:
            #     return result

        return result

    """
    Override the abstract / base class method.
    @return ProcedureResult
    """

    def check_word_limit(self, list_name):
        result = ProcedureResult()
        result.is_valid = True

        length_name = len(list_name)
        if length_name > MAX_LIMIT:
            result = ProcedureResult()
            result.is_valid = False
            result.result_code = AnalysisIssueCodes.TOO_MANY_WORDS

            result.values = {'list_name': list_name, 'length_name': length_name}

        return result

    """
    Override the abstract / base class method.
    @return ProcedureResult
    """

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

                result.values = {'list_name': list_name or [], 'list_none': unclassified_words_list_response}

        return result

    """
    Override the abstract / base class method.
    @return ProcedureResult
    """

    def check_words_to_avoid(self, list_name, name):
        result = ProcedureResult()
        result.is_valid = True

        all_words_to_avoid_list = [word.lower() for word in self.word_condition_service.get_words_to_avoid()]
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
                'list_avoid_compound': word_avoid_compound_list,
            }

        return result

    """
    Override the abstract / base class method
    Input: list_dist = ['MOUNTAIN', 'VIEW']
           list_desc = ['FOOD', 'GROWERS']
    @return ProcedureResult
    """

    def search_conflicts(
        self,
        list_dist_words,
        list_desc_criteria,
        list_desc_words,
        list_name,
        name,
        stand_alone_words,
        check_name_is_well_formed=False,
        queue=False,
    ):
        list_conflicts, most_similar_names = [], []
        dict_highest_counter, response = {}, {}
        self._list_processed_names = list()
        for w_dist, w_desc_criteria, w_desc in zip(list_dist_words, list_desc_criteria, list_desc_words):
            if w_dist and w_desc_criteria:
                list_details, forced = self.get_conflicts(
                    dict_highest_counter,
                    w_dist,
                    w_desc_criteria,
                    w_desc,
                    list_name,
                    stand_alone_words,
                    check_name_is_well_formed,
                    queue,
                )
                list_conflicts.extend(list_details)
                list_conflicts = [
                    i for n, i in enumerate(list_conflicts) if i not in list_conflicts[n + 1 :]
                ]  # Remove duplicates
                if forced:
                    break

        most_similar_names.extend(
            sorted(list_conflicts, key=lambda item: (-item['score'], item['name']))[0:MAX_MATCHES_LIMIT]
        )

        return self.prepare_response(most_similar_names, queue, list_name, list_dist_words, list_desc_words)

    def get_conflicts(
        self,
        dict_highest_counter,
        w_dist,
        w_desc_criteria,
        w_desc,
        list_name,
        stand_alone_words,
        check_name_is_well_formed,
        queue,
    ):
        dist_substitution_dict, desc_synonym_dict, dist_substitution_compound_dict, desc_synonym_compound_dict = (
            {},
            {},
            {},
            {},
        )
        desc_synonym_dict = self.get_substitutions_descriptive(w_desc)

        # Check if a token is stand-alone word
        desc_synonym_dict = self.get_stand_alone_substitutions(desc_synonym_dict, stand_alone_words)

        diff_desc = list(set(w_desc) - set(w_desc_criteria))
        desc_synonym_criteria_dict = self.remove_key(diff_desc, desc_synonym_dict)

        # Need to check if the name is well formed?
        if check_name_is_well_formed:
            dist_substitution_dict = self.get_dictionary(dist_substitution_dict, w_dist)
        else:
            dist_substitution_dict = self.get_substitutions_distinctive(w_dist)

        w_dist, list_name, dist_substitution_dict = remove_double_letters_list_dist_words(
            w_dist, list_name, dist_substitution_dict
        )

        list_conflict_details = list()

        change_filter = True if self.director.skip_search_conflicts else False
        list_details, forced = self.get_conflicts_db(
            dist_substitution_dict,
            desc_synonym_criteria_dict,
            desc_synonym_dict,
            dict_highest_counter,
            change_filter,
            list_name,
            check_name_is_well_formed,
            queue,
        )
        list_conflict_details.extend(list_details)

        if not forced:
            current_app.logger.debug('Search for conflicts considering compound-distinctive words.')
            dist_compound_dict = self.get_compound_distinctives(dist_substitution_dict)
            list_details, forced = self.get_conflicts_db(
                dist_compound_dict,
                desc_synonym_criteria_dict,
                desc_synonym_dict,
                dict_highest_counter,
                change_filter,
                list_name,
                check_name_is_well_formed,
                queue,
            )
            list_conflict_details.extend(list_details)

        if not forced:
            current_app.logger.debug(
                'Search for conflicts considering compound-distinctive words taking one simple descriptive'
            )
            dist_compound_dict, desc_synonym_dict_new = self.get_compound_distinctive_hybrid(
                dist_substitution_dict, desc_synonym_dict, list_name
            )
            diff_keys = self.get_different_key(desc_synonym_dict_new, desc_synonym_dict)
            desc_synonym_dict = desc_synonym_dict_new
            desc_synonym_criteria_dict = self.remove_key(diff_keys, desc_synonym_criteria_dict)

            list_details, forced = self.get_conflicts_db(
                dist_compound_dict,
                desc_synonym_criteria_dict,
                desc_synonym_dict,
                dict_highest_counter,
                change_filter,
                list_name,
                check_name_is_well_formed,
                queue,
            )
            list_conflict_details.extend(list_details)

        return list_conflict_details, forced

    def get_conflicts_db(
        self,
        dist_substitution_dict,
        desc_synonym_criteria_dict,
        desc_synonym_dict,
        dict_highest_counter,
        change_filter,
        list_name,
        check_name_is_well_formed,
        queue,
    ):
        stop_word_list = self.name_processing_service.get_stop_words()
        stop_words = '|'.join(stop_word_list)
        list_details = []
        forced = False

        if check_name_is_well_formed:
            current_app.logger.debug('Search conflicts for not well formed name')
        elif queue:
            current_app.logger.debug('Search conflicts for INPROGRESS, HOLD, DRAFT')
        else:
            current_app.logger.debug('Search conflicts for APPROVED, CONDITIONAL, COND_RESERVED, RESERVED')

        for key_dist, value_dist in dist_substitution_dict.items():
            criteria = Request.get_general_query(change_filter, queue)
            name_criteria = Request.get_distinctive_query(value_dist, stop_words, check_name_is_well_formed)
            for key_desc, value_desc in desc_synonym_criteria_dict.items():
                current_app.logger.debug(key_dist, ':DIST ', key_desc, ':DESC')
                criteria = Request.get_descriptive_query(value_desc, criteria, name_criteria)
                matches = Request.find_by_criteria_array(criteria, queue)
                matches = self.skip_name_matches_processed(matches)
                list_conflicts_details, forced = self.get_most_similar_names(
                    dict_highest_counter, set(matches), dist_substitution_dict, desc_synonym_dict, list_name
                )
                list_details.extend(list_conflicts_details)

                if forced:
                    return list_details, forced

        return list_details, forced

    def search_exact_match(
        self,
        list_dist_words,
        list_desc_words,
        list_name,
        queue=False,
        end_list_designations=None,
        any_list_designations=None,
        stop_words=None,
    ):
        result = ProcedureResult()
        result.is_valid = False

        if queue:
            current_app.logger.debug('Search for exact match in INPROGRESS, HOLD, DRAFT')
        else:
            current_app.logger.debug('Search for exact match in APPROVED, CONDITIONAL, COND_RESERVED, RESERVED')

        criteria = Request.get_general_query(change_filter=False, queue=queue)
        criteria = Request.get_query_exact_match(
            criteria,
            list_name,
            list_dist_words,
            list_desc_words,
            end_list_designations,
            any_list_designations,
            stop_words,
        )
        matches = Request.find_by_criteria_array(criteria, queue=queue)

        dict_highest_counter = {}
        list_details = []
        for match in matches:
            dict_highest_counter[match.name] = 1.0
            list_details = self.get_details_higher_score(dict_highest_counter, [match], {})
            current_app.logger.debug('Exact match: {}'.format(match.name))
            break

        return self.prepare_response(list_details, queue, list_name, list_dist_words, list_desc_words)

    """
    Override the abstract / base class method
    @return ProcedureResult
    """

    def check_words_requiring_consent(self, list_name, name):
        result = ProcedureResult()
        result.is_valid = True

        all_words_consent_list = self.word_condition_service.get_words_requiring_consent()
        words_consent_dict = {}
        word_consent_original_list = []
        name_singular_plural_list = list(set(get_plural_singular_name(name)))

        for name_sin_plural in name_singular_plural_list:
            for words_consent in all_words_consent_list:
                if re.search(r'\b{0}\b'.format(re.escape(words_consent.lower())), name_sin_plural.lower()):
                    words_consent_dict.update(self.get_position_word_consent(words_consent, name_sin_plural))
                    word_consent_original_list.append(words_consent)
                elif re.search(
                    r'\b{0}\b'.format(re.escape(words_consent.lower().replace(' ', ''))), name_sin_plural.lower()
                ):
                    words_consent_dict.update(
                        self.get_position_word_consent(words_consent.lower().replace(' ', ''), name_sin_plural)
                    )
                    word_consent_original_list.append(words_consent)
        word_consent_original_list = list(set(word_consent_original_list))
        words_consent_list_response = []
        for key in sorted(words_consent_dict):
            words_consent_list_response.append(list_name[key])

        if words_consent_list_response:
            result.is_valid = False
            result.result_code = AnalysisIssueCodes.NAME_REQUIRES_CONSENT

            result.values = {
                'list_name': list_name,
                'list_consent': words_consent_list_response,
                'list_consent_original': word_consent_original_list,
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

        if all_designations_user and not all_designations:
            result.is_valid = False
            result.result_code = AnalysisIssueCodes.DESIGNATION_NON_EXISTENT
            result.values = {'list_name': list_name, 'correct_designations': all_designations_user}

        return result

    """
    Override the abstract / base class method
    list_name: original name tokenized by designation. For instance, designation composed of many words is tokenized as one.
    entity_type_user: Entity type typed by user. 'CR' by default
    all_designations: All Designations found in name (either misplaced or not)
    all_designations_user: All designations for the entity type typed by the user. 
    @return ProcedureResult
    """

    def check_designation_mismatch(self, list_name, entity_type_user, all_designations, all_designations_user):
        result = ProcedureResult()
        result.is_valid = True
        mismatch_entity_designation_list = []

        if not all_designations_user and all_designations:
            result.is_valid = False
            result.result_code = AnalysisIssueCodes.DESIGNATION_REMOVAL
            result.values = {
                'list_name': list_name,
                'incorrect_designations': all_designations,
                'correct_designations': all_designations_user,
            }
        else:
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

    """
    Override the abstract / base class method
    list_name: original name tokenized by designation. For instance, designation composed of many words is tokenized as one.
    designation_end_list: Correct end designations
    misplaced_designation_end: Misplaced end designations
    @return ProcedureResult
    """

    def check_end_designation_more_than_once(
        self, list_name, all_designation_end_list, correct_designations_user, misplaced_designation_end
    ):
        result = ProcedureResult()
        result.is_valid = True

        designation_end_list = [
            designation for designation in all_designation_end_list if designation in correct_designations_user
        ]
        correct_end_designations = designation_end_list + list(
            set(misplaced_designation_end) - set(designation_end_list)
        )

        if correct_end_designations.__len__() > 1:
            corrected_end_designations_sorted = []

            for word in list_name:
                if word in correct_end_designations:
                    corrected_end_designations_sorted.append(word)

            result.is_valid = False
            result.result_code = AnalysisIssueCodes.END_DESIGNATION_MORE_THAN_ONCE
            result.values = {'list_name': list_name, 'correct_end_designations': corrected_end_designations_sorted}

        return result

    """
    Override the abstract / base class method
    Just <end> designation can be misplaced in other position, it can be at the beginning, middle or before end in the name
    Note: <any> designation can be anywhere in the name, so to be misplaced is not possible.
    @return ProcedureResult
    """

    def check_designation_misplaced(self, list_name, misplaced_designation_end):
        result = ProcedureResult()
        result.is_valid = True

        if misplaced_designation_end:
            result.is_valid = False
            result.result_code = AnalysisIssueCodes.DESIGNATION_MISPLACED
            result.values = {'list_name': list_name, 'misplaced_end_designation': misplaced_designation_end}

        return result

    """
    Override the abstract / base class method
    @return ProcedureResult
    """

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
                'list_special_compound': word_special_compound_list,
            }

        return result

    def get_most_similar_names(
        self, dict_highest_counter, db_matches, dist_substitution_dict, desc_synonym_dict, list_name
    ):
        auto_analyze_url = current_app.config.get('AUTO_ANALYZE_URL', None)
        list_details, selected_matches = [], []
        forced = False
        list_dist = list(dist_substitution_dict.keys())
        list_desc = list(desc_synonym_dict.keys())

        if db_matches:
            total = len(db_matches)
            current_app.logger.debug('Possible conflicts returned: ', total)

            json_analyze = {
                'names': [match.name for match in db_matches],
                'list_name': list_name,
                'list_dist': list_dist,
                'list_desc': list_desc,
                'dict_substitution': dist_substitution_dict,
                'dict_synonyms': desc_synonym_dict,
            }
            conflict_response = requests.post(url=''.join([auto_analyze_url]), json=json_analyze)
            if not conflict_response:
                warnings.warn('Quart Service did not return a result', Warning)
            conflicts = conflict_response.json()
            dict_matches_counter = dict(ChainMap(*conflicts.get('result')))

            selected_matches = [match for match in db_matches if match.name in dict_matches_counter.keys()]

            if dict_matches_counter:
                all_subs_dict = get_all_dict_substitutions(dist_substitution_dict, desc_synonym_dict, list_name)
                # Get  N highest score (values) and shortest names (key)
                dict_highest_counter.update(
                    {
                        k: v
                        for k, v in sorted(dict_matches_counter.items(), key=lambda item: (-item[1], item[0]))[
                            0:MAX_MATCHES_LIMIT
                        ]
                    }
                )
                list_details = self.get_details_higher_score(dict_highest_counter, selected_matches, all_subs_dict)
                forced = True if any(value == EXACT_MATCH for value in dict_highest_counter.values()) else False

        return list_details, forced

    def prepare_response(self, most_similar_names, queue, list_name, list_dist_words, list_desc_words):
        conflict_name = {}
        result = ProcedureResult()
        result.is_valid = False
        response = {}

        for record in most_similar_names:
            conflict_name = {record['name']: record['tokens']}
            id_num = record['corp_num'] if record['corp_num'] else record['nr_num']
            start_date = record['consumption_date'] if record['corp_num'] else record['submitted_date']
            source = 'corp' if record['corp_num'] else 'nr'

        if conflict_name:
            response = {'names': conflict_name, 'id': id_num, 'start_date': start_date, 'source': source}

        if response and not queue:
            result_code = AnalysisIssueCodes.CORPORATE_CONFLICT
            result = self.get_response_search_conflicts_queue(
                result, list_name, list_dist_words, list_desc_words, response, result_code
            )
        elif response and queue:
            result_code = AnalysisIssueCodes.QUEUE_CONFLICT
            result = self.get_response_search_conflicts_queue(
                result, list_name, list_dist_words, list_desc_words, response, result_code
            )

        else:
            result.is_valid = True
            result.result_code = AnalysisIssueCodes.CHECK_IS_VALID
            result.values = []

        return result

    def is_match(self, list_conflicts, forced):
        for record in list_conflicts:
            if record['score'] == 1.0:
                return True
        return False

    def get_details_higher_score(self, dict_highest_counter, selected_matches, all_subs_dict):
        list_details = []
        for key, value in dict_highest_counter.items():
            for record in selected_matches:
                if record.name == key:
                    dict_details = {
                        'score': value,
                        'name': key,
                        'tokens': all_subs_dict,
                        'consumption_date': record.consumptionDate,
                        'submitted_date': record.submittedDate,
                        'corp_num': record.corpNum,
                        'nr_num': record.nrNum,
                    }
                    list_details.append(dict_details)

        return list_details

    def get_substitutions_distinctive(self, w_dist):
        syn_svc = self.synonym_service

        all_dist_substitutions_synonyms = syn_svc.get_all_substitutions_synonyms(
            words=w_dist, words_are_distinctive=True
        ).data

        dist_substitution_dict = parse_dict_of_lists(all_dist_substitutions_synonyms)

        for key, value in dist_substitution_dict.items():
            stem_w = porter.stem(key)
            if stem_w not in value:
                value.append(stem_w)
            if key not in value:
                value.append(key)

        return dist_substitution_dict

    def get_substitutions_descriptive(self, w_desc):
        syn_svc = self.synonym_service

        all_desc_substitutions_synonyms = syn_svc.get_all_substitutions_synonyms(
            words=[desc.replace(' ', '') for desc in w_desc], words_are_distinctive=False
        ).data

        desc_synonym_dict = parse_dict_of_lists(all_desc_substitutions_synonyms)

        for key, value in desc_synonym_dict.items():
            if key not in value:
                value.append(key)

        return desc_synonym_dict

    def get_stand_alone_substitutions(self, desc_synonym_dict, stand_alone):
        for key, value in desc_synonym_dict.items():
            if key in stand_alone:
                value.pop()
                value.extend(stand_alone)

        return desc_synonym_dict

    def check_name_is_well_formed_response(self, list_original_name, list_name, list_dist, result_code):
        result = ProcedureResult()
        result.is_valid = False
        result.result_code = result_code
        result.values = {
            'list_original': list_original_name or [],
            'list_name': list_name or [],
            'list_dist': list_dist or [],
        }

        return result

    def check_conflict_well_formed_response(self, processed_name, list_original_name, list_name, list_dist, issue):
        np_svc = self.name_processing_service
        check_conflicts = get_conflicts_same_classification(
            self, list_name, processed_name, np_svc.get_stand_alone_words(), list_name, list_name
        )
        if check_conflicts.is_valid:
            return self.check_name_is_well_formed_response(list_original_name, list_name, list_dist, issue)
        else:
            return check_conflicts

    def check_descriptive(self, name_dict):
        valid = False
        for i, value in enumerate(name_dict.values()):
            if value == DataFrameFields.DESCRIPTIVE.value:
                valid = True
                break

        return valid

    def stop_search(self, cosine, matches):
        if (len(matches) >= HIGH_CONFLICT_RECORDS and cosine >= HIGH_SIMILARITY) or (cosine == EXACT_MATCH):
            return True
        return False

    def get_response_search_conflicts_queue(
        self, result, list_name, list_dist_words, list_desc_words, response, result_code
    ):
        result.is_valid = False
        result.result_code = result_code
        result.values = {
            'list_name': list_name,
            'list_dist': list_dist_words,
            'list_desc': list_desc_words,
            'list_conflicts': response['names'],
            'id': response['id'],
            'start_date': response['start_date'],
            'source': response['source'],
        }
        return result

    """
    dict_dist: Dictionary of distinctive tokens with its corresponding substitutions (if they exist) included in a list.
    dict_desc: Dictionary of descriptive tokens with its corresponding substitutions (if they exist) included in a list.
    list_name: List of words which form a clean name
    @return dict_compound_dist: dictionary of compound distinctive items (made of two words) with its corresponding 
    substitutions (if they exist) included as list
    """

    def get_compound_distinctives(self, dict_dist):
        list_dict = list(dict_dist.keys())

        list_dist_compound = list()
        for i in range(2, len(list_dict) + 1):
            list_dist_compound.extend(subsequences(list_dict, i))

        dist_compound_dict = self.add_substitutions(list_dist_compound, dict_dist)

        return {x.replace(' ', ''): v for x, v in dist_compound_dict.items()}

    def get_dictionary(self, dct, lst):
        for elem in lst:
            dct[elem] = [elem]
        return dct

    def add_substitutions(self, list_dist_compound, dict_dist):
        dict_compound_dist = dict()
        for dist_compound in list_dist_compound:
            dist = dist_compound.split()
            dist_values = [dict_dist[x] for x in dist]
            compound = list()
            for item in itertools.product(*dist_values):
                compound.append(remove_double_letters(''.join(item)))
            dist_compound = dist_compound.replace(' ', '')
            dict_compound_dist[remove_double_letters(dist_compound)] = compound

        return dict_compound_dist

    def get_compound_distinctive_hybrid(self, dist_substitution_dict, dict_descriptive, list_name):
        dict_compound_dist, dict_desc = {}, {}

        if dict_descriptive.__len__() > 1 and dist_substitution_dict.__len__() > 0:
            dict_desc = dict(dict_descriptive)
            dist_list = list(dist_substitution_dict.keys())[::-1]
            for key_dist in dist_list:
                idx = list_name.index(key_dist)
                key_desc = list(dict_descriptive.keys())[0]
                if idx + 1 < list_name.__len__() and list_name[idx + 1] in dict_descriptive.get(key_desc):
                    compound = [key_dist + key_desc]
                    dict_compound_dist[list_name[idx] + list_name[idx + 1]] = compound

                    if list_name[idx + 1] in dict_desc:
                        del dict_desc[list_name[idx + 1]]

        return dict_compound_dist, dict_desc

    def skip_name_matches_processed(self, matches):
        unique_matches = []
        for match in matches:
            if match.name not in self._list_processed_names:
                self._list_processed_names.append(match.name)
                unique_matches.append(match)

        return unique_matches

    def is_valid_year(self, list_name):
        result = ProcedureResult()
        result.is_valid = True

        years_in_name = []
        incorrect_years = []
        try:
            for item in list_name:
                year = re.search(r'\b[1-2][0-9]{3}\b', item)
                if year:
                    years_in_name.append(int(year.group(0)))
        except ValueError:
            pass

        for year in years_in_name:
            if year == CURRENT_YEAR and CURRENT_YEAR in EXCEPTION_YEARS:
                incorrect_years.append(str(year))
            elif year == CURRENT_YEAR + 1 and CURRENT_MONTH == 12 and CURRENT_DAY >= 15:
                # Following year from Dec 15th to Dec 30th is allowed. Do not add to the list,
                # just continue checking the remaining years if they exist.
                pass
            elif LOWER_LIMIT_TIME <= year <= UPPER_LIMIT_TIME:
                incorrect_years.append(str(year))

        if incorrect_years:
            result.is_valid = False
            result.result_code = AnalysisIssueCodes.INCORRECT_YEAR

            result.values = {'incorrect_years': incorrect_years}
        return result

    def remove_key(self, keys, desc_synonym_dict):
        desc_synonym_criteria_dict = dict(desc_synonym_dict)
        for item in keys:
            desc_synonym_criteria_dict.pop(item)

        return desc_synonym_criteria_dict

    def get_different_key(self, desc_synonym_dict_delta, desc_synonym_dict):
        diff_key = list()
        for key in desc_synonym_dict.keys():
            if not key in desc_synonym_dict_delta:
                diff_key.append(key)
        return diff_key
