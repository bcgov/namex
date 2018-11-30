

def nro_examiner_name(examiner_name): #-> (str)
    """returns an examiner name, formated and tuncated to fit in NRO
    :examiner_name (str): an examiner name, as found in NameX
    :returns (str): an examiner name that is 7 or less chars in length
    """
    #namex examiner_names are {domain}{/}{username}
    start = examiner_name.find('/')+1
    return examiner_name[start:start+7]


def row_to_dict(row):
    """
    This takes a row from a resultset and returns a dict with the same structure
    :param row:
    :return: dict
    """
    return {key: value for (key, value) in row.items()}


def ora_row_to_dict(col_names, row):
    """
    This takes a row from a resultset and returns a dict with the same structure
    :param row:
    :return: dict
    """
    return dict(zip([col.lower() for col in col_names], row))


def validNRFormat(nr):
    '''NR should be of the format "NR 1234567"
    '''

    if len(nr) != 10 or nr[:2] != 'NR' or nr[2:3] != ' ':
        return False

    try:
        num = int(nr[3:])
    except:
        return False

    return True
