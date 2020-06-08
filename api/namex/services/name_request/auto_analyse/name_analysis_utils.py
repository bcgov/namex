import re
import collections
from collections import OrderedDict

from . import porter

from namex.services.name_request.auto_analyse import DataFrameFields

from namex.utils.common import parse_dict_of_lists


# TODO: Fix caps and stuff...
def data_frame_to_list(df):
    df_dist = df.loc[df.word_classification == DataFrameFields.DISTINCTIVE.value]
    df_desc = df.loc[df.word_classification == DataFrameFields.DESCRIPTIVE.value]
    df_none = df.loc[df.word_classification == DataFrameFields.UNCLASSIFIED.value]

    list_dist = list(df_dist.word)
    list_desc = list(df_desc.word)
    list_none = list(df_none.word)

    return list_dist, list_desc, list_none


def get_dataframe_list(df, field):
    return df[field].str.split(',').tolist()


def get_flat_list(lst):
    subs_list = [item for sublist in lst for item in sublist]
    return [x.strip() for x in subs_list]
    # return subs_list


'''
def remove_french(text, fr_designation_end_list):
    compound = re.findall(r'[^/]+(?://[^/]*)*', text)
    if len(compound) == 2:
        fr_list_text = [x.lower() for x in compound[1].split(" ") if x]
        if any(item in fr_designation_end_list for item in fr_list_text):
            compound.pop()
            text = ' '.join(map(str, compound))
    return text
'''

'''
Previous behaviour: The section after slash considered french designations to imply the section was in French.
Current behaviour: The section after slash is not longer considering french designation.
Rules:  1) Before and after slash has to be at least two words to removed string after slash.
           Eg.
           ABC ENGINEERING/CENTRAL CARE  --> ABC ENGINEERING
        2) In the case just having a word at the beginning then the string is kept with no changes.
           Eg.
           RE/MAX WALNUT DEVELOPMENT  --> RE/MAX WALNUT DEVELOPMENT
        3) In the case just having a word at the end, this is kept removing the slash.
           Eg.
           ABC ENGINEERING 7/24 --> ABC ENGINEERING 7 24
'''


def remove_french(text, all_designations_alternators):
    text = re.sub(r'^([^-/]*?\b({0})(?!\w)[^-/\n]*)(?:[-/]\s*(.*))?$'.format(all_designations_alternators),
                  r'\1 ',
                  text,
                  0,
                  re.IGNORECASE)
    return " ".join(text.lower().split())


def remove_stop_words(name, stop_words, exception_stop_word_designation):
    exception_designation_rx = '|'.join(map(re.escape, exception_stop_word_designation))
    stop_words_rx = '|'.join(map(re.escape, stop_words))
    ws_generic_rx = r'\b({0})\b'.format(stop_words_rx)
    ws_rx = re.compile(r'({0})|{1}'.format(exception_designation_rx, ws_generic_rx), re.I)

    text = ws_rx.sub(lambda x: x.group(1) or "", name)

    return " ".join(text.split())


def list_distinctive_descriptive_same(name_list):
    queue = collections.deque(name_list)
    dist_list = []
    desc_list = []

    while len(queue) > 1:
        queue.pop()
        dist_list.append(list(queue))

    dist_list.reverse()

    for dist in dist_list:
        desc_list.append([i for i in name_list if i not in dist])

    if len(dist_list) == 0 and len(desc_list) == 0:
        return [name_list], [desc_list]

    return dist_list, desc_list


'''
validate_distinctive_descriptive_lists function to be deprecated: This function is not longer useful. The logic was decomposed in 
list_distinctive_descriptive and check_name_is_well_formed.
'''


def validate_distinctive_descriptive_lists(list_name, list_dist, list_desc):
    current_category = None
    list_dist_tmp = []
    list_desc_tmp = []
    list_incorrect_classification = []
    for idx, token_name, has_more in lookahead(list_name):
        if idx == 0:
            current_category = None
        if ((token_name in list_dist and token_name in list_desc) or (
                token_name not in list_dist and token_name not in list_desc)) and has_more and (
                current_category is None):
            list_dist_tmp.extend([token_name])
            current_category = DataFrameFields.DISTINCTIVE.value
        elif ((token_name in list_dist and token_name in list_desc) or (
                token_name not in list_dist and token_name not in list_desc)) and has_more and (
                current_category == DataFrameFields.DISTINCTIVE.value):
            list_dist_tmp.extend([token_name])
            list_desc_tmp.extend([token_name])
            current_category = DataFrameFields.DISTINCTIVE.value
        elif ((token_name in list_dist and token_name in list_desc) or (
                token_name not in list_dist and token_name not in list_desc)) and has_more and (
                current_category is None or current_category == DataFrameFields.DESCRIPTIVE.value):
            list_desc_tmp.extend([token_name])
            current_category = DataFrameFields.DESCRIPTIVE.value
        elif token_name in list_dist and token_name not in list_desc and (
                current_category is None or current_category == DataFrameFields.DISTINCTIVE.value) and has_more:
            current_category = DataFrameFields.DISTINCTIVE.value
            list_dist_tmp.extend([token_name])
        elif token_name in list_desc and (
                current_category == DataFrameFields.DISTINCTIVE.value or current_category == DataFrameFields.DESCRIPTIVE.value):
            current_category = DataFrameFields.DESCRIPTIVE.value
            list_desc_tmp.extend([token_name])
        else:
            list_incorrect_classification.append({token_name: idx})
            # break

    return list_dist_tmp, list_desc_tmp, list_incorrect_classification


def list_distinctive_descriptive(name_list, dist_list, desc_list):
    queue_dist = collections.deque(dist_list)
    dist_list_tmp, dist_list_all, desc_list_tmp, desc_list_all = [], [], [], []

    dist_list_tmp.append(list(queue_dist))

    while len(queue_dist) > 1:
        queue_dist.pop()
        dist_list_tmp.append(list(queue_dist))

    dist_list_tmp.reverse()

    for dist in dist_list_tmp:
        desc_list_tmp.append([i for i in name_list if i not in dist and i in desc_list])

    # Validate generation of list of lists of distinctives and descriptives with the correct combinations:
    for idx, element in enumerate(dist_list_tmp):
        if dist_list_tmp[idx] + desc_list_tmp[idx] == name_list:
            dist_list_all.append(dist_list_tmp[idx])
            desc_list_all.append(desc_list_tmp[idx])

    for idx, element in enumerate(dist_list_all):
        if len(dist_list_all) > 1 and (len(dist_list_all[idx]) == 0 or len(desc_list_all[idx]) == 0):
            del dist_list_all[idx]
            del desc_list_all[idx]

    if len(dist_list_all) == 0 and len(desc_list_all) == 0:
        return [dist_list_all], [desc_list_all]

    return dist_list_all, desc_list_all


def get_all_substitutions(syn_svc, list_dist, list_desc, list_name):
    all_dist_substitutions_synonyms = syn_svc.get_all_substitutions_synonyms(
        words=list_dist,
        words_are_distinctive=True
    ).data

    dist_substitution_dict = parse_dict_of_lists(all_dist_substitutions_synonyms)

    all_desc_substitutions_synonyms = syn_svc.get_all_substitutions_synonyms(
        words=list_desc,
        words_are_distinctive=False
    ).data

    desc_substitution_dict = parse_dict_of_lists(all_desc_substitutions_synonyms)

    all_substitution_dict = collections.OrderedDict()
    for word in list_name:
        if word in dist_substitution_dict:
            all_substitution_dict[word] = dist_substitution_dict[word]
        elif word in desc_substitution_dict:
            all_substitution_dict[word] = desc_substitution_dict[word]

    for k, v in all_substitution_dict.items():
        all_substitution_dict[k] = [porter.stem(e.lower()) for e in v]

    return all_substitution_dict, dist_substitution_dict, desc_substitution_dict


def lookahead(iterable):
    """Pass through all values from the given iterable, augmented by the
    information if there are more values to come after the current one
    (True), or if it is the last value (False).
    """
    # Get an iterator and pull the first value.
    it = iter(iterable)
    last = next(it)
    # Run the iterator to exhaustion (starting from the second value).
    idx = 0
    for idx, val in enumerate(it):
        # Report the *previous* value (more to come).
        yield idx, last, True
        last = val
    # Report the last value.
    yield idx + 1, last, False


'''
Rules:
PROPERTIES OF VICTORIA
1.- Check if the first word is both categories or distinctive and it is a synonym. If it is count it as DESC
2.- Check each word to see if exists in the synonyms in the same category and are together in the name
'''


def check_synonyms_category(list_dist_words, list_desc_words, clean_name, category_dict):
    first = True
    while clean_name:
        first_word = clean_name.pop(0)
        category_first_set = set(category_dict[first_word]) if category_dict[first_word] else None
        if first and category_first_set:
            list_dist_words = list(filter(lambda x, value=first_word: x != value, list_dist_words))
            list_desc_words.append(first_word)
            print("First word " + first_word + " found in synonyms, DIST -> DESC")
        first = False
        if clean_name:
            next_word = clean_name[0]
            category_next_set = set(category_dict[next_word]) if category_dict[next_word] else None

            if category_first_set and category_next_set and category_first_set.intersection(category_next_set):
                list_dist_words = list(filter(lambda x, value=first_word: x != value, list_dist_words))
                list_dist_words = list(filter(lambda x, value=next_word: x != value, list_dist_words))
                list_desc_words.append(first_word)
                list_desc_words.append(next_word)
                print(
                    first_word + " and " + next_word + " found in category: " + str(
                        category_first_set.intersection(category_next_set)))

    list_dist_words = list(OrderedDict.fromkeys(list_dist_words))
    list_desc_words = list(OrderedDict.fromkeys(list_desc_words))

    return list_dist_words, list_desc_words


def check_numbers_beginning(syn_svc, tokens):
    if tokens[0].isdigit():
        for idx, token in enumerate(tokens[1:]):
            if not token.isdigit():
                if not syn_svc.get_word_synonyms(word=token).data:
                    tokens = tokens[idx + 1:]
                    #tokens = [] + tokens
                break
    return tokens
