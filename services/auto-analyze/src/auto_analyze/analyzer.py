# Copyright © 2020 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Analyzes a single name."""
import itertools
import logging
import math
from collections import Counter

from synonyms.services import SynonymService
from namex.services.name_request.auto_analyse.protected_name_analysis import ProtectedNameAnalysisService
from namex.services.name_request.builders.name_analysis_builder import NameAnalysisBuilder
from namex.services.name_processing.name_processing import NameProcessingService
from namex.services.name_request.auto_analyse.name_analysis_utils import (
    get_classification,
    get_flat_list,
    remove_double_letters_list_dist_words,
    remove_spaces_list,
    subsequences,
    get_compound_descriptives,
    update_compound_tokens
)

from namex.utils.profiling import print_time, profile

from nltk.stem import PorterStemmer

porter = PorterStemmer()

# TODO: Swap this out for the actual service we don't want to call service via API, it's too slow
synonym_service = SynonymService()
name_processing_service = NameProcessingService()
name_analysis_service = ProtectedNameAnalysisService()
builder = NameAnalysisBuilder(name_analysis_service)

STEM_W = 0.85
SUBS_W = 0.65
OTHER_W_DESC = 3.0
OTHER_W_DIST = 0.35

EXACT_MATCH = 1.0
HIGH_SIMILARITY = 0.85
MEDIUM_SIMILARITY = 0.71
MINIMUM_SIMILARITY = 0.66

HIGH_CONFLICT_RECORDS = 20


# ok deep function
@print_time()
@profile(sort_by='cumulative', lines_to_print=30, strip_dirs=False)
async def auto_analyze(name: str,
                       name_tokens: list,  # pylint: disable=too-many-locals, too-many-arguments
                       list_name: list, list_dist: list,
                       list_desc: list, dict_substitution: dict,
                       dict_synonyms: dict,
                       dict_compound_synonyms_all: dict,
                       stand_alone_words: list,
                       np_svc_prep_data: name_analysis_service) -> dict:

    # print('--- Connection pool status ---')
    # print(db.engine.pool.status())
    """Return a dictionary with name as key and similarity as value, 1.0 is an exact match."""
    logging.getLogger(__name__).debug(
        'name: %s ,  list_name %s,  list_dist: %s, list_desc: %s, dict_subst: %s,  dict_syns: %s',
        name_tokens, list_name, list_dist, list_desc, dict_substitution, dict_synonyms)

    service = np_svc_prep_data
    wc_svc = service.word_classification_service
    token_svc = service.token_classifier_service

    dict_matches_counter = {}
    all_dict_synonyms = {**dict_synonyms, **dict_compound_synonyms_all}

    if name_tokens == list_name:
        similarity = EXACT_MATCH
    else:
        match_list = name_tokens

        get_classification(service, match_list, wc_svc, token_svc, dict_compound_synonyms_all, dict_synonyms,
                           conflict=True)

        dist_db_substitution_dict = get_substitutions(service.get_list_dist(), dict_substitution)
        service._list_dist_words, match_list, _ = remove_double_letters_list_dist_words(service.get_list_dist(),
                                                                                        match_list)

        desc_tmp_synonym_dict = get_substitutions(service.get_list_desc(), all_dict_synonyms)
        desc_tmp_synonym_dict = remove_extra_value(desc_tmp_synonym_dict, all_dict_synonyms)

        # Update key in desc_db_synonym_dict
        service._dict_desc_words_search_conflicts = stem_key_dictionary(  # pylint: disable=protected-access
            desc_tmp_synonym_dict
        )
        service._dict_desc_words_search_conflicts = add_key_values(  # pylint: disable=protected-access
            service.get_dict_desc_search_conflicts()
        )

        # Get dictionary for original words
        dict_desc = update_dict(all_dict_synonyms, list_desc)

        # Stem dictionary for original name
        dict_desc_stemmed = stem_key_dictionary(dict_desc)
        dict_desc_stemmed = add_key_values(dict_desc_stemmed)

        list_desc, dict_desc_stemmed = remove_descriptive_same_category(dict_desc_stemmed)

        service._list_desc_words = list(  # pylint: disable=protected-access
            service.get_dict_desc_search_conflicts().keys()
        )

        list_dist = [element.replace(" ","")for element in list_dist]
        service._list_dist_words = [element.replace(" ","") for element in service.get_list_dist()]

        list_dist_stem = [porter.stem(word) for word in list_dist]
        vector1_dist = text_to_vector(list_dist_stem)

        vector2_dist, entropy_dist = get_vector(service.get_list_dist(), list_dist,
                                                dist_db_substitution_dict, True)

        if all(value == OTHER_W_DIST for value in vector2_dist.values()):
            vector2_dist, entropy_dist, _ = check_compound_dist(list_dist=list(vector2_dist.keys()),
                                                                list_desc=None,
                                                                original_class_list=list_dist,
                                                                class_subs_dict=dist_db_substitution_dict)

        if not vector2_dist:
            match_list_desc = list(service.get_list_desc())
            match_list_dist_desc = service.get_list_dist() + match_list_desc[0:-1]
            vector2_dist, entropy_dist, service._list_desc_words = check_compound_dist(
                list_dist=match_list_dist_desc,
                list_desc=service.get_list_desc(),
                original_class_list=list_dist,
                class_subs_dict=dict_desc_stemmed)

        similarity_dist = round(get_similarity(vector1_dist, vector2_dist, entropy_dist), 2)

        list_desc_stem = [porter.stem(word) for word in list_desc]
        vector1_desc = text_to_vector(list_desc_stem)

        vector2_desc, entropy_desc = get_vector(
            remove_spaces_list(service.get_list_desc()), list_desc,
            service.get_dict_desc_search_conflicts())
        similarity_desc = round(
            get_similarity(vector1_desc, vector2_desc, entropy_desc), 2)

        similarity = round((similarity_dist + similarity_desc) / 2, 2)
        logging.getLogger(__name__).debug('similarity: %s', similarity)

    if similarity >= MINIMUM_SIMILARITY:
        dict_matches_counter.update({name: similarity})

    return dict_matches_counter


async def clean_name(name: str,
                     np_svc_prep_data: name_analysis_service) -> dict:
    """Return a a list of clean names"""
    logging.getLogger(__name__).debug('name: %s', name)

    service = name_analysis_service
    np_svc = service.name_processing_service

    np_svc.set_name(name, np_svc_prep_data)
    name_tokens = np_svc.name_tokens

    return {name: name_tokens}


def get_vector(conflict_class_list, original_class_list, class_subs_dict, dist=False):
    """Return vector of words (or synonyms) found in original_class_list which are in conflict_class_list."""
    vector = dict()
    entropy = list()
    original_class_list = original_class_list if original_class_list else []
    class_subs_dict = class_subs_dict if class_subs_dict else {}

    conflict_class_stem = [porter.stem(name.lower()) for name in conflict_class_list]

    for idx, word in enumerate(original_class_list):  # pylint: disable=unused-variable
        k = word.lower()
        word_stem = porter.stem(k)
        counter = 1
        if word.lower() in conflict_class_list:
            entropy.append(1)
        elif word_stem in conflict_class_stem:
            entropy.append(STEM_W)
        elif word_stem in get_flat_list(class_subs_dict.values()):
            entropy.append(SUBS_W)
        else:
            counter = OTHER_W_DIST if dist else OTHER_W_DESC
            entropy.append(0.0)
        if counter == 1:
            vector[word_stem] = counter

    # Make sure we don't divide by zero!
    entropy_score = sum(entropy) / len(entropy) if len(entropy) > 0 else 0
    return vector, entropy_score


def check_compound_dist(list_dist, list_desc, original_class_list, class_subs_dict):
    """Return a vector with distinctive compound items and updated list of descriptives."""
    vector_dist = {}
    entropy_dist = 0.0
    for i in range(2, len(list_dist) + 1):
        compound_space_list = [x for x in subsequences(list_dist, i)]  # pylint: disable=unnecessary-comprehension
        compound = [x.replace(' ', '') for x in compound_space_list]
        vector_dist, entropy_dist = get_vector(compound, original_class_list, class_subs_dict)

    # Update descriptive list
    if list_desc and entropy_dist > 0.0:
        token_list = []
        for word in compound_space_list:
            token_list.extend(word.split())
        intersection = [x for x in list_desc if x in token_list]
        for word in intersection:
            list_desc.remove(word)

    return vector_dist, entropy_dist, list_desc


def text_to_vector(list_name):
    """Return a vector."""
    return Counter(list_name)


def get_cosine(vec1, vec2):
    """Return cosine similarity between vector 1 and vector 2."""
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])

    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    return float(numerator) / denominator


def get_similarity(vector1, vector2, entropy):
    """Return similarity between two vectors which are either both distinctives or descriptives."""
    return get_cosine(vector1, vector2) * entropy


def is_not_real_conflict(list_name, stand_alone_words, list_dist, dict_desc, service):
    """Return True if the name is not a real conflict. Otherwise, false if the name is a conflict."""
    list_desc = list(dict_desc.keys())
    if is_standalone_name(list_name, stand_alone_words):
        return stand_alone_additional_dist_desc(list_dist, service.get_list_dist(), list_desc,
                                                service.get_list_desc())
    return False


def is_standalone_name(list_name, stand_alone_words):
    """Return True if standalone name."""
    if any(stand_alone in list_name for stand_alone in stand_alone_words):
        return True
    return False


def stand_alone_additional_dist_desc(lst_dist_name1, lst_dist_name2, lst_desc_name1, lst_desc_name2):
    """Return True if there is an additional distinctive or descriptive in the stand-alone name."""
    if lst_dist_name1.__len__() != lst_dist_name2.__len__() or lst_desc_name1.__len__() != lst_desc_name2.__len__():
        return True

    return False


def remove_extra_value(d1, d2):
    """Return d1 with d2 items removed."""
    for k2, v2 in d2.items():  # pylint: disable=unused-variable
        for k1, v1 in d1.items():
            if len(set(v1) ^ set(v2)) == 1 and k1 not in v2:
                try:
                    v1.remove(k1)
                    break
                except ValueError:
                    pass
    return d1


def update_dictionary_key(d1, d2):
    """Update key dictionary in d1 with key in d2."""
    d3 = {}
    skip = False
    for k1, v1 in d1.items():
        for k2, v2 in d2.items():
            if (len(set(v1) ^ set(v2)) == 1 and k1 in v2) or len(set(v1) ^ set(v2)) == 0:
                d3.update({k2: v1})
                skip = True
                break
        if not skip:
            d3.update({k1: v1})
            skip = False
    return d3


def remove_descriptive_same_category(dict_desc):
    """Remove descriptive with the same category."""
    dict_desc_unique_category = {key: val for i, (key, val) in enumerate(dict_desc.items())
                                 if porter.stem(key) not in itertools.chain(*list(dict_desc.values())[:i])}

    return list(dict_desc_unique_category.keys()), dict_desc_unique_category


def stem_key_dictionary(d1):
    """Stem the dictionary key."""
    dict_stem = {porter.stem(k): v for (k, v) in d1.items()}

    return dict_stem


def add_key_values(d1):
    """Add key in dictionary to values if does not exist."""
    for key, values in d1.items():
        if key not in values:
            values.append(key)
    return d1


def get_compound_synonyms(np_svc, name_tokens_clean_dict, syn_svc, dict_all_simple_synonyms):
    dct = {}
    dict_all_compound_synonyms = {}
    for key, value in name_tokens_clean_dict.items():
        dct = get_compound_descriptives(np_svc, value, syn_svc, dict_all_simple_synonyms)
        if dct:
            dict_all_compound_synonyms.update(dct)
            dct.clear()

    return dict_all_compound_synonyms


def update_name_tokens(list_all_compound_synonyms, name_tokens_clean_dict):
    compound_name_tokens_clean_dict = {}
    for key, value in name_tokens_clean_dict.items():
        compound_name = update_compound_tokens(list_all_compound_synonyms, value)
        compound_name_tokens_clean_dict.update({key: compound_name})

    return compound_name_tokens_clean_dict


def get_substitutions(list_dist, all_substitution_dict):
    substitution_dict = {}
    for dist in list_dist:
        substitutions = all_substitution_dict.get(dist)
        if not substitutions:
            substitutions = [dist]
        elif dist not in substitutions:
            substitutions.append(dist)
        substitution_dict[dist] = substitutions

    return substitution_dict


def get_substitutions_dictionary(syn_svc, dict_substitution, dict_synonyms, list_words):
    substitutions_dict = {}
    for word in list_words:
        substitutions = dict_substitution.get(word, None)
        if not substitutions and word not in dict_synonyms:
            substitutions = syn_svc.get_word_substitutions(word=word)
        if substitutions:
            substitutions_dict.update({word: substitutions})

    return substitutions_dict


def update_dict(dict_desc, list_desc):
    dict_desc_new = {}
    for desc in list_desc:
        if desc in dict_desc:
            dict_desc_new.update({desc: dict_desc.get(desc)})
        else:
            dict_desc_new.update({desc: [desc]})
    return dict_desc_new
