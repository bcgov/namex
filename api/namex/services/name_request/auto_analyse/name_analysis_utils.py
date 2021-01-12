import re
import collections
import itertools
import ast

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


def get_all_dict_substitutions(dist_substitution_dict, desc_substitution_dict, list_name):
    all_substitution_dict = {}
    for word in list_name:
        key_dist = next((key for key, value in dist_substitution_dict.items() if word == key or word in value), None)
        if key_dist:
            all_substitution_dict[word] = dist_substitution_dict[key_dist]
        key_desc = next((key for key, value in desc_substitution_dict.items() if word == key or word in value), None)
        if key_desc:
            all_substitution_dict[word] = desc_substitution_dict[key_desc]

    return all_substitution_dict


# Lucas - this is just in here for reference
# def get_distinctive_substitutions(syn_svc, list_dist):
#     all_dist_substitutions_synonyms = syn_svc.get_all_substitutions_synonyms(
#         words=list_dist,
#         words_are_distinctive=True
#     ).data
#
#     dist_substitution_dict = parse_dict_of_lists(all_dist_substitutions_synonyms)
#
#     return dist_substitution_dict
#
#
# def get_descriptive_substitutions(syn_svc, list_desc):
#     all_desc_substitutions_synonyms = syn_svc.get_all_substitutions_synonyms(
#         words=list_desc,
#         words_are_distinctive=False
#     ).data
#
#     desc_substitution_dict = parse_dict_of_lists(all_desc_substitutions_synonyms)
#
#     return desc_substitution_dict


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


def check_numbers_beginning(syn_svc, tokens):
    if tokens[0].isdigit():
        for idx, token in enumerate(tokens[1:]):
            if not token.isdigit():
                if not syn_svc.get_word_synonyms(word=token).data:
                    tokens = tokens[idx + 1:]
                break
    return tokens


def check_synonyms(dict_all_synonyms, list_dist_words, list_desc_words, list_none_words, list_name):
    list_desc_words_set = frozenset(list_desc_words)
    list_desc = []
    dict_desc = {}
    intersection = [x for x in list_dist_words if x in list_desc_words_set]

    for word in list_name:
        if word in list_desc_words or word in list_none_words:
            synonyms = None
            if {word} <= dict_all_synonyms.keys():
                synonyms = dict_all_synonyms.get(word)

            if synonyms:
                dict_desc.update({word: synonyms})
                list_desc.append(word)
                if word in intersection:
                    list_dist_words.remove(word)

    return list_dist_words, list_desc, dict_desc


def update_substitution_dictionary(list_dist, dict_substitutions, conflict=False):
    dict_dist = {}
    for dist in list_dist:
        if not conflict:
            substitutions = dict_substitutions.get(dist, [dist])
            if substitutions:
                dict_dist.update({dist: substitutions})
        else:
            dict_dist.update({dist: [dist]})

    return dict_dist


def update_none_list(list_none_words, list_desc):
    return [x for x in list_none_words if x not in list_desc]


def change_descriptive(list_dist_words, list_desc_words, list_name):
    for idx, word in enumerate(list_name[1:], start=1):
        pos = idx - 1
        if word in list_dist_words and list_name[pos] in list_desc_words:
            # Update to distinctive all elements before
            while pos >= 0:
                list_desc_words.remove(list_name[pos])
                list_dist_words.insert(pos, list_name[pos])
                pos -= 1
        break
    return list_dist_words, list_desc_words


def get_classification_summary(list_dist, list_desc, list_name):
    classification_summary = {
        word.replace(" ",
                     ""): DataFrameFields.DISTINCTIVE.value if word in list_dist else DataFrameFields.DESCRIPTIVE.value if any(
            word in desc_word for desc_word in list_desc) else DataFrameFields.UNCLASSIFIED.value for word
        in
        list_name}
    return classification_summary


def get_conflicts_same_classification(service, name_tokens, processed_name, stand_alone_words, list_dist, list_desc):
    list_dist, list_desc = \
        list_distinctive_descriptive(name_tokens, list_dist, list_desc)

    # Update dictionaries
    np_svc = service.name_processing_service
    dict_all_synonyms = {**np_svc.get_compound_synonyms(), **np_svc.get_synonyms()}

    # Search conflicts coming from check_name_is_well_formed analysis
    check_conflicts = service.search_conflicts(list_dist, list_desc, list_desc, dict_all_synonyms,
                                               np_svc.get_substitutions(), name_tokens,
                                               processed_name,
                                               stand_alone_words,
                                               check_name_is_well_formed=True, queue=False)

    return check_conflicts


def get_classification(service, match, wc_svc, token_svc, dict_compound_synonyms_all, dict_simple_synonyms_all={},
                       conflict=False):
    # Update name tokenization based on compound synonyms
    service.set_compound_descriptive_name_tokens(update_compound_tokens(
        list(service.name_processing_service.get_compound_synonyms().keys()),
        match))

    service.token_classifier = wc_svc.classify_tokens(service.get_compound_descriptive_name_tokens())
    service._list_dist_words, service._list_desc_words, service._list_none_words = service.word_classification_tokens

    if service.get_list_none() and service.get_list_none().__len__() > 0:
        service._list_dist_words, service._list_desc_words = \
            token_svc.handle_unclassified_words(
                service.get_list_dist(),
                service.get_list_desc(),
                service.get_list_none(),
                service.compound_descriptive_name_tokens
            )

    # Add to synonyms dictionary elements just in descriptive, but not in distinctive
    dict_synonyms = add_desc_in_dict_synonyms(dict_simple_synonyms_all, service.get_list_desc(), service.get_list_dist(), service.get_list_none(), match)
    if dict_synonyms:
        dict_simple_synonyms_all= dict_synonyms

    dict_all_synonyms = {**dict_compound_synonyms_all, **dict_simple_synonyms_all}
    service._list_dist_words, service._list_desc_words, service._dict_desc_words = check_synonyms(dict_all_synonyms,
                                                                                                  service.get_list_dist(),
                                                                                                  service.get_list_desc(),
                                                                                                  service.get_list_none(),
                                                                                                  service.get_compound_descriptive_name_tokens())

    service._list_none_words = update_none_list(service.get_list_none(), service.get_list_desc())

    # Check if words are in the same category
    if conflict:
        if 2 < service.get_list_dist().__len__() == match.__len__():
            service._list_desc_words = [service.get_list_dist().pop()]
            service._dict_desc_words.update({service.get_list_desc()[0]: service.get_list_desc()})
        elif 2 < service.get_list_desc().__len__() == match.__len__():
            service._list_dist_words = [service.get_list_desc().pop(0)]
            service._dict_desc_words.pop(service.get_list_dist()[0], None)

    service.set_compound_descriptive_name_tokens(
        update_compound_tokens(service.get_list_dist() + service.get_list_desc(),
                               service.compound_descriptive_name_tokens))

    service._dict_name_words = get_classification_summary(service.get_list_dist(), service.get_list_desc(),
                                                          service.compound_descriptive_name_tokens)
    # service.set_name_tokens(remove_spaces_list(service.name_tokens))
    print("Original Classification:")
    print(service.get_dict_name())

    service.set_name_tokens_search_conflict(service.compound_descriptive_name_tokens)
    service._list_dist_words_search_conflicts = remove_misplaced_distinctive(list(service.get_list_dist()),
                                                                             service.get_list_desc(),
                                                                             service.name_tokens_search_conflict)

    service._list_desc_words_search_conflicts, service._dict_desc_words_search_conflicts = remove_descriptive_same_category(
        service.get_dict_desc())

    service.set_name_tokens_search_conflict(
        update_token_list(service.get_list_dist_search_conflicts() + service.get_list_desc_search_conflicts(),
                          service.name_tokens_search_conflict))

    service._dict_name_words_search_conflicts = get_classification_summary(service.get_list_dist_search_conflicts(),
                                                                           service.get_list_desc_search_conflicts(),
                                                                           service.name_tokens_search_conflict)
    service.set_name_tokens_search_conflict(remove_spaces_list(service.name_tokens_search_conflict))

    print("Classification for searching conflicts in NameX DB:")
    print(service.get_dict_name_search_conflicts())


def subsequences(iterable, length):
    return [" ".join(iterable[i: i + length]) for i in range(len(iterable) - length + 1)]


def get_valid_compound_descriptive(syn_svc, original_synonyms_dict, list_compound):
    desc_dist = dict()
    for compound in list_compound:
        synonym_response = original_synonyms_dict.get(compound, None)
        if not synonym_response:
            synonym_response = syn_svc.get_word_synonyms(word=compound.replace(" ", "")).data

        if synonym_response:
            if compound not in synonym_response:
                synonym_response.append(compound.replace(" ", ""))
            desc_dist[compound] = synonym_response

    return desc_dist


def search_word(d, search_item):
    for key, values in d.items():
        if key is not None:
            for value in values:
                if search_item in key or search_item in value:
                    return key
    return None


def update_compound_tokens(list_desc_compound, original_list):
    list_compound = sorted(list_desc_compound + original_list, key=len, reverse=True)
    str_original = " ".join(original_list)

    compound_alternators = '|'.join(map(re.escape, list_compound))
    regex = re.compile(r'(?<!\w)({0})(?!\w)'.format(compound_alternators))
    compound_name = regex.findall(str_original)

    return compound_name


def update_token_list(list_dist_desc, list_name):
    list_name_updated = []
    for item in list_name:
        if item in list_dist_desc:
            list_name_updated.append(item)

    return list_name_updated


def get_compound_descriptives(svc, name_tokens, syn_svc, original_synonyms_dict={}):
    list_compound = []
    for i in range(2, len(name_tokens)):
        list_compound.extend(subsequences(name_tokens, i))

    desc_compound_dict_validated = get_valid_compound_descriptive(syn_svc, original_synonyms_dict, list_compound)
    svc._compound_descriptive_name_tokens = update_compound_tokens(list(desc_compound_dict_validated.keys()),
                                                                   name_tokens)

    return desc_compound_dict_validated


def remove_spaces_list(lst):
    return [x.replace(' ', '') for x in lst]


def remove_double_letters(name):
    return re.sub(r'\b(([a-zA-Z])\2+)\b|([a-zA-Z])\3+', r'\1\3', name)


def list_to_string(lst):
    return ' '.join(map(str, lst))


def remove_misplaced_distinctive(list_dist, list_desc, list_name):
    if list_desc.__len__() > 0 and list_dist.__len__() > 0:
        for word in list_name[list_name.index(list_desc[0]) + 1:]:
            if word in list_dist:
                list_dist.remove(word)
    return list_dist


def remove_descriptive_same_category(dict_desc):
    dict_desc_unique_category = {key: val for i, (key, val) in enumerate(dict_desc.items())
                                 if porter.stem(key) not in itertools.chain(*list(dict_desc.values())[:i])}

    return list(dict_desc_unique_category.keys()), dict_desc_unique_category


def remove_double_letters_list_dist_words(list_dist, name_tokens, dist_substitution_dict=None, queue=False):
    list_dist_final = []
    for item in list_dist:
        not_double_letters_item = remove_double_letters(item)
        list_dist_final.append(not_double_letters_item)
        name_tokens = list(map(
            lambda x, value=item, singular_letter_value=not_double_letters_item: str.replace(x, value,
                                                                                             singular_letter_value),
            name_tokens))
        if not queue:
            if dist_substitution_dict:
                dist_substitution_dict[not_double_letters_item] = [remove_double_letters(element) for element in dist_substitution_dict.pop(item)]
                if not dist_substitution_dict.get(not_double_letters_item):
                    dist_substitution_dict[not_double_letters_item].append(not_double_letters_item)

    return list_dist_final, name_tokens, dist_substitution_dict


def get_synonyms_dictionary(syn_svc, synonyms_original_dict, list_words):
    synonyms_dict = {}
    for word in list_words:
        key= get_key_dictionary(word, synonyms_original_dict)
        synonyms = synonyms_original_dict.get(key, None)
        if not synonyms:
            synonyms = syn_svc.get_word_synonyms(word=word).data
        if synonyms:
            synonyms_dict.update({word: synonyms})
    return synonyms_dict


def add_desc_in_dict_synonyms(dict_synonyms, list_desc, list_dist, list_none, list_name):
    dct = {}
    for word in list_name:
        if word in list_desc or word in list_none:
            key = get_key_dictionary(word, dict_synonyms)
            values = dict_synonyms.get(key)
            if values:
                dct.update({word: values})
            elif word not in list_dist:
                dct.update({word: [word]})

    return dct


def update_dict_synonyms(dict_synonyms, list_desc):
    dct = {}
    for desc in list_desc:
        if not dict_synonyms or desc not in dict_synonyms:
            dct.update({desc: [desc]})
        else:
            dct.update({desc: dict_synonyms.get(desc)})

    return dct


def get_key_dictionary(word, dct):
    for key, values in dct.items():
        if word in values:
            return key
    return None
