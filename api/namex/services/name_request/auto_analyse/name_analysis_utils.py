import re
import collections

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

    return all_substitution_dict, dist_substitution_dict, desc_substitution_dict


def get_distinctive_substitutions(syn_svc, list_dist):
    all_dist_substitutions_synonyms = syn_svc.get_all_substitutions_synonyms(
        words=list_dist,
        words_are_distinctive=True
    ).data

    dist_substitution_dict = parse_dict_of_lists(all_dist_substitutions_synonyms)

    return dist_substitution_dict


def get_descriptive_substitutions(syn_svc, list_desc):
    all_desc_substitutions_synonyms = syn_svc.get_all_substitutions_synonyms(
        words=list_desc,
        words_are_distinctive=False
    ).data

    desc_substitution_dict = parse_dict_of_lists(all_desc_substitutions_synonyms)

    return desc_substitution_dict


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


def check_synonyms(syn_svc, list_dist_words, list_desc_words):
    both_list = list(set(list_dist_words) & set(list_desc_words))
    for word in both_list:
        if syn_svc.get_word_synonyms(word=word).data:
            list_dist_words.remove(word)
        else:
            list_desc_words.remove(word)

    return list_dist_words, list_desc_words


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


def get_classification_summary(list_name, list_dist_words, list_desc_words):
    return {word: DataFrameFields.DISTINCTIVE.value if word in list_dist_words else DataFrameFields.DESCRIPTIVE.value \
        if word in list_desc_words else DataFrameFields.UNCLASSIFIED.value for word in list_name}


def get_conflicts_same_classification(builder, name_tokens, processed_name, list_dist, list_desc):
    list_dist, list_desc = \
        list_distinctive_descriptive(name_tokens, list_dist, list_desc)
    check_conflicts = builder.search_conflicts(list_dist, list_desc, name_tokens, processed_name, True)

    return check_conflicts


def get_classification(director, service, syn_svc, match, wc_svc, token_svc):
    service.token_classifier = wc_svc.classify_tokens(match)
    service._list_dist_words, service._list_desc_words, service._list_none_words = service.word_classification_tokens

    if service.get_list_none() and service.get_list_none().__len__() > 0:
        service._list_dist_words, service._list_desc_words = \
            token_svc.handle_unclassified_words(
                service.get_list_dist(),
                service.get_list_desc(),
                service.get_list_none(),
                service.name_tokens
            )

    service._list_dist_words, service._list_desc_words = check_synonyms(syn_svc,
                                                                        service.get_list_dist(),
                                                                        service.get_list_desc())

    service._list_dist_words, service._list_desc_words = change_descriptive(service.get_list_dist(),
                                                                            service.get_list_desc(),
                                                                            service.name_tokens)

    service._dict_name_words = get_classification_summary(service.name_tokens,
                                                          service.get_list_dist(),
                                                          service.get_list_desc())
