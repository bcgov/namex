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
from collections import Counter
import math

from namex.services.name_request.auto_analyse.name_analysis_utils \
    import get_classification, subsequences, get_flat_list, remove_spaces_list

from namex.services.name_processing.name_processing \
    import NameProcessingService

from namex.services.name_request.auto_analyse.protected_name_analysis \
    import ProtectedNameAnalysisService

from swagger_client import SynonymsApi as SynonymService

from nltk.stem import PorterStemmer
porter = PorterStemmer()

STEM_W = 0.85
SUBS_W = 0.65
OTHER_W = 3.0

EXACT_MATCH = 1.0
HIGH_SIMILARITY = 0.85
MEDIUM_SIMILARITY = 0.71
MINIMUM_SIMILARITY = 0.66

HIGH_CONFLICT_RECORDS = 20

# async def auto_analyze(name: str) -> bool:
#     """Return either True/False if the name passes auto analysis.
#
#     For fun it approves all names of even length.
#     """
#     print(f'> {name}')
#     rand = int(random.uniform(1, 5))
#     await asyncio.sleep(rand)
#     print(f'< {name} {rand}')
#
#     if len(name) % 2:
#         return False
#     return True

'''
TO DO: Call services from namex api:
Synonym Service
ProtectedNameAnalysisService()
    -Name Processing Service
    -Word Classification Service
name_analysis_utils to call functions such as get_classification, remove_spaces_list
service: word_classification

name_analysis_utils to call functions get_classification, remove_spaces_list
'''

synonym_service = SynonymService()
name_processing_service = NameProcessingService()
name_analysis_service = ProtectedNameAnalysisService()


async def auto_analyze(name: str, list_name: list, list_dist: list,
                       list_desc: list, dict_substitution: dict,
                       dict_synonyms: dict) -> bool:
    print(
        'name: {0}  ,  list_name {1},  list_dist: {2}  , list_desc: {3}  , dict_sybst: {4},  dict_syns{5}'.format(
            name, list_name, list_dist, list_desc, dict_substitution, dict_synonyms))
    syn_svc = synonym_service
    service = name_analysis_service
    np_svc = service.name_processing_service
    wc_svc = service.word_classification_service
    token_svc = service.token_classifier_service

    vector1_dist = text_to_vector(list_dist)
    vector1_desc = text_to_vector(list_desc)

    dict_matches_counter = {}

    np_svc.set_name(name)
    stand_alone_words = np_svc.get_stand_alone_words()

    if np_svc.name_tokens == list_name:
        similarity = EXACT_MATCH
    else:
        match_list = np_svc.name_tokens
        get_classification(service, stand_alone_words, syn_svc, match_list, wc_svc, token_svc)

        vector2_dist, entropy_dist = get_vector(service.get_list_dist_search_conflicts(), list_dist,
                                                dict_substitution)

        if all(value == OTHER_W for value in vector2_dist.values()):
            vector2_dist, entropy_dist, _ = check_compound_dist(list_dist=list(vector2_dist.keys()),
                                                                list_desc=None,
                                                                original_class_list=list_dist,
                                                                class_subs_dict=dict_substitution)

        if not vector2_dist:
            match_list_desc = list(service.get_list_desc())
            match_list_dist_desc = service.get_list_dist() + match_list_desc[0:-1]
            vector2_dist, entropy_dist, service._list_desc_words = check_compound_dist(
                list_dist=match_list_dist_desc,
                list_desc=service.get_list_desc(),
                original_class_list=list_dist,
                class_subs_dict=dict_substitution)

        similarity_dist = round(get_similarity(vector1_dist, vector2_dist, entropy_dist), 2)

        vector2_desc, entropy_desc = get_vector(
            remove_spaces_list(service.get_list_desc_search_conflicts()), list_desc,
            dict_synonyms)
        similarity_desc = round(
            get_similarity(vector1_desc, vector2_desc, entropy_desc), 2)

        similarity = round((similarity_dist + similarity_desc) / 2, 2)
        print(similarity)

    if similarity == EXACT_MATCH or (
            similarity >= MINIMUM_SIMILARITY and not is_not_real_conflict(list_name,
                                                                          stand_alone_words,
                                                                          list_dist,
                                                                          dict_synonyms,
                                                                          service)):
        dict_matches_counter.update({name: similarity})

    return dict_matches_counter


'''
TO DO: connect to name_analysis_utils to call functions such as get_flat_list
'''


def get_vector(conflict_class_list, original_class_list, class_subs_dict):
    vector = dict()
    entropy = list()
    original_class_list = original_class_list if original_class_list else []
    class_subs_dict = class_subs_dict if class_subs_dict else {}

    original_class_stem = [porter.stem(name.lower()) for name in original_class_list]

    for idx, word in enumerate(conflict_class_list):
        k = word.lower()
        word_stem = porter.stem(k)
        counter = 1
        if word.lower() in original_class_list:
            entropy.append(1)
        elif word_stem in original_class_stem:
            idx = original_class_stem.index(word_stem)
            k = original_class_list[idx]
            entropy.append(STEM_W)
        elif word_stem in get_flat_list(class_subs_dict.values()):
            k = ''.join([key for (key, value) in class_subs_dict.items() if word_stem in value])
            entropy.append(SUBS_W)
        else:
            counter = OTHER_W
            entropy.append(0.0)
        if counter == 1:
            vector[k] = counter
        else:
            vector[word] = counter

    # Make sure we don't divide by zero!
    entropy_score = sum(entropy) / len(entropy) if len(entropy) > 0 else 0
    return vector, entropy_score


'''
TO DO: connect to name_analysis_utils to call functions such as subsequences
'''


def check_compound_dist(list_dist, list_desc, original_class_list, class_subs_dict):
    vector_dist = {}
    entropy_dist = 0.0
    for i in range(2, len(list_dist) + 1):
        compound_space_list = [x for x in subsequences(list_dist, i)]
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
    return Counter(list_name)


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])

    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def get_similarity(vector1, vector2, entropy):
    return get_cosine(vector1, vector2) * entropy


def is_not_real_conflict(list_name, stand_alone_words, list_dist, dict_desc, service):
    list_desc = list(dict_desc.keys())
    if is_standalone_name(list_name, stand_alone_words):
        return stand_alone_additional_dist_desc(list_dist, service.get_list_dist(), list_desc,
                                                service.get_list_desc())
    else:
        return check_additional_dist_desc(list_dist, service.get_list_dist(), dict_desc,
                                          service)


def is_standalone_name(list_name, stand_alone_words):
    if any(stand_alone in list_name for stand_alone in stand_alone_words):
        return True
    return False


def stand_alone_additional_dist_desc(lst_dist_name1, lst_dist_name2, lst_desc_name1, lst_desc_name2):
    if lst_dist_name1.__len__() != lst_dist_name2.__len__() or lst_desc_name1.__len__() != lst_desc_name2.__len__():
        return True

    return False


def check_additional_dist_desc(list_dist_user_name, list_dist_conflict, dict_desc_user_name, service):
    for (k, v), (k2, v2) in zip(service.get_dict_desc_search_conflicts().items(), dict_desc_user_name.items()):
        same_synonym_category = porter.stem(k2) in v
        if (
                k != k2 and k2 not in service.get_list_desc() and same_synonym_category and list_dist_user_name.__len__() > list_dist_conflict.__len__()) or \
                not same_synonym_category:
            print("Name '{}' is not considered a real conflict.".format(service.get_processed_name()))
            return True
    return False
