import re
import pandas as pd
import collections
from sqlalchemy import create_engine

from namex.services.name_request.auto_analyse import DataFrameFields

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
    # subs_list = []
    return df[field].str.split(',').tolist()

    # subs_list = [item for sublist in subs_list for item in sublist]
    # subs_list = [x.strip() for x in subs_list]

    # return dataframe_list


def get_flat_list(lst):
    subs_list = [item for sublist in lst for item in sublist]
    return [x.strip() for x in subs_list]
    # return subs_list

def build_query_distinctive(dist_all_permutations, l):
    query = "select n.name " + \
            "from requests r, names n " + \
            "where r.id = n.nr_id and " + \
            "r.state_cd IN ('APPROVED','CONDITIONAL') and " + \
            "r.request_type_cd IN ('PA','CR','CP','FI','SO', 'UL','CUL','CCR','CFI','CCP','CSO','CCC','CC') and " + \
            "n.state IN ('APPROVED','CONDITION') and " + \
            "lower(n.name) similar to " + "'"
    st = ''
    for s in range(l):
        st += '%s '

    permutations = "|".join(st % tup for tup in dist_all_permutations)
    query += "(" + permutations + ")%%" + "'"

    return query


def build_query_descriptive(desc_substitution_list, query):
    for element in desc_substitution_list:
        query += " and lower(n.name) similar to "
        substitutions = ' ?| '.join(map(str, element))
        query += "'" + "%%( " + substitutions + " ?)%%" + "'"

    return query


def remove_french(text, fr_designation_end_list):
    compound = re.findall(r'[^/]+(?://[^/]*)*', text)
    if len(compound) == 2:
        fr_list_text = [x.lower() for x in compound[1].split(" ") if x]
        if any(item in fr_designation_end_list for item in fr_list_text):
            compound.pop()
            text = ' '.join(map(str, compound))
    return text


def words_distinctive_descriptive(name_list):
    queue = collections.deque(name_list)
    dist_list = []
    desc_list = []

    while 1 < len(queue):
        queue.pop()
        dist_list.append(list(queue))
    dist_list.reverse()

    for dist in dist_list:
        desc_list.append([i for i in name_list if i not in dist])

    idx = 0
    for dist, desc in zip(dist_list, desc_list):
        if not dist + desc == name_list:
            dist_list.pop(idx)
            desc_list.pop(idx)
        idx += 1

    return dist_list, desc_list
