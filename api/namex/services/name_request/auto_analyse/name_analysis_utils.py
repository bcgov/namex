import re


def read_data_frame(file):
    df = pd.read_csv(file, usecols=['category', 'enabled', 'synonyms_text', 'stems_text'])
    return df.loc[(df['enabled'].astype(str).str.lower() == 'true')]


def dataframe_to_list(df):
    df_dist = df.loc[df.classification == 'Distinctive']
    df_desc = df.loc[df.classification == 'Descriptive']
    df_none = df.loc[df.classification == 'None']

    list_dist = list(df_dist.word)
    list_desc = list(df_desc.word)
    list_none = list(df_none.word)

    return list_dist, list_desc, list_none


def clean_name_words(text, dsg_any, dsg_end):
    text = text  # TODO: Enable this stuff again
    # desig_end = '|'.join(dsg_end) + ")$"
    # desig_any = "(" + '|'.join(dsg_any) + ")|"

    # text = re.sub(r'( |-)+',
    #               ' ',
    #               re.sub(
    #                   r"\.COM|" + desig_any + "(?<=[a-zA-Z])\'[A-Z]|[^a-zA-Z0-9 -]+|\s(?=&)|(?<!\w\w)(?:\s+|-)(?!\w\w)|\s(" + desig_end,
    #                   '',
    #                   text,
    #                   0,
    #                   re.IGNORECASE),
    #               0,
    #               re.IGNORECASE)

    return text


def alphanum_subs_list(text):
    sub_regex = []
    regex = []
    words = ' '.join([word for index, word in enumerate(text.split(" ")) if index == 0 or word not in stopWords])
    words = re.sub(r"[^a-zA-Z0-9 -\']+", ' ', words, 0, re.IGNORECASE)

    words_list = words.split(" ")

    subs_list = df_sub['synonyms_text'].str.split(',').tolist()
    subs_list = [item for sublist in subs_list for item in sublist]
    subs_list = [x.strip(' ') for x in subs_list]

    for s in subs_list:
        if s in words:
            sub_regex.extend([s])

    for w in words_list:
        for r in sub_regex:
            if w in r:
                regex.extend([w])

    return list(dict.fromkeys([x for x in regex if x]))

def substitution_regex(subs_list):
    regex = ""
    if subs_list:
        for s in subs_list:
            regex += "(?!" + s + "\b)"
    return regex