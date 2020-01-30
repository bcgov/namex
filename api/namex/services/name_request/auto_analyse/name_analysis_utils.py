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


def clean_name_words(text, stop_words, dsg_any, dsg_end, subs_list):
    words = text.lower()
    words = ' '.join([word for x, word in enumerate(words.split(" ")) if x == 0 or word not in stop_words])
    # words = remove_french(words)
    tokens = regex_transform(words, dsg_any, dsg_end, subs_list, stop_words)
    tokens = tokens.split()

    return [x.upper() for x in tokens if x]


def regex_transform(text, stop_words, dsg_any, dsg_end, subs_list):
    desig_end = '((lot)+\s+\d+|\d*|' + '|'.join(map(str, dsg_end)) + ')'
    desig_any = "(" + '|'.join(dsg_any) + ")"
    # prefixes = '|'.join(prefixes_list)

    exceptions_ws = substitution_list(re.sub(r'[^a-zA-Z0-9 -\']+', ' ', text, 0, re.IGNORECASE), subs_list, stop_words)
    exceptions_ws.extend(['null'])

    exception_ws_rx = '|'.join(map(re.escape, exceptions_ws))
    ws_generic_rx = r'(?<=\d)(?=[^\d\s])|(?<=[^\d\s])(?=\d)'
    ws_rx = re.compile(rf'({exception_ws_rx})|{ws_generic_rx}', re.I)

    text = re.sub(r'\s+',
                  ' ',
                  re.sub(
                      r'^(?:\d+(?:ST|[RN]D|TH)?\s+)+(?=[^\d]+$)(?!.*?(?:HOLDINGS$|BC$|VENTURES$))|(?<=\b[A-Za-z]\b) +(?=[a-zA-Z]\b)',
                      '',
                      re.sub(r'(?<=[A-Za-z]\b )([ 0-9]*(ST|[RN]D|TH)?\b)',
                             '',
                             re.sub(r'(?<=\b[A-Za-z]\b) +(?=[a-zA-Z]\b)|^\s+|\s+$',
                                    '',
                                    re.sub(r'[&/-]',
                                           ' ',
                                           # re.sub(r'(?<=[0-9])\s+(?=(?:ST|[RN]D|TH)(?: +[^\W\d_]|$))',
                                           #       '',
                                           ws_rx.sub(lambda x: x.group(1) or " ",
                                                     re.sub(r'\b(\d+(ST|[RN]D|TH))(\w+)\b',
                                                            r'\1 \3',
                                                            re.sub(r'\b(\w{2,})(\b\W+\b\1\b)*',
                                                                   r'\1',
                                                                   re.sub(
                                                                       r'(?<=[a-zA-Z])\'[Ss]|\(?No.?\s*\d+\)?|\(?lot.?\s*\d+[-]?\d*\)?|[^a-zA-Z0-9 &/-]+',
                                                                       ' ',
                                                                       # re.sub(r'\b('+prefixes+')([ &\/.-])([A-Za-z]+)',
                                                                       #       r'\1\3',
                                                                       re.sub(
                                                                           r'\.COM|(?<=\d),(?=\d)|(?<=[A-Za-z])+[\/&-](?=[A-Za-z]\b)|\b' + desig_any + '\b|\s' + desig_end + '(?=(\s' + desig_end + ')*$)',
                                                                           '',
                                                                           text,
                                                                           0,
                                                                           re.IGNORECASE),
                                                                       # 0,
                                                                       # re.IGNORECASE),
                                                                       0,
                                                                       re.IGNORECASE),
                                                                   0,
                                                                   re.IGNORECASE),
                                                            0,
                                                            re.IGNORECASE),
                                                     ),
                                           # 0,
                                           # re.IGNORECASE),
                                           0,
                                           re.IGNORECASE),
                                    0,
                                    re.IGNORECASE),
                             0,
                             re.IGNORECASE),
                      0,
                      re.IGNORECASE),
                  0,
                  re.IGNORECASE)
    return text


def substitution_list(text, stop_words, subs_list):
    subs_list = [['accelerate', ' xlr8', ' xlreight'],
                 ['access', ' axis', ' axys'],
                 ['cosi', ' cosy', ' cozi', ' cozy'],
                 ['acqua', ' acwa', ' aqua'],
                 ['aerial', ' arial', ' ariel']]

    sub_regex = []
    regex = []
    num_regex = ".*[0-9].*"

    words = ' '.join([word for index, word in enumerate(text.split(" ")) if index == 0 or word not in stop_words])
    words = re.sub(r"[^a-zA-Z0-9 -\']+", ' ', words, 0, re.IGNORECASE)

    words_list = words.split(" ")

    # Flat list of lists
    subs_list = [item for sublist in subs_list for item in sublist]
    subs_list = [x.strip(' ') for x in subs_list]

    # If any word substitution is in the name string
    for s in subs_list:
        if s in words:
            sub_regex.extend([s])

    # If any word in name is in any word substitution
    for w in words_list:
        for r in sub_regex:
            if w in r:
                regex.extend([w])

    subs_list = list(dict.fromkeys([x for x in regex if x]))

    # Just alphanumeric word substitutions
    return [w for w in subs_list if re.match(num_regex, w)]


def remove_french(text, french_desig_list):
    compound = re.findall(r'[^/]+(?://[^/]*)*', text)
    if len(compound) == 2:
        fr = [x for x in compound[1].split(" ") if x]
        if any(item in french_desig_list for item in fr):
            compound.pop()
            text = ' '.join(map(str, compound))
    return text
