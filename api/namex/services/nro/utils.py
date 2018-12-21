import re


def nro_examiner_name(examiner_name):  # -> (str)
    """returns an examiner name, formated and tuncated to fit in NRO
    :examiner_name (str): an examiner name, as found in NameX
    :returns (str): an examiner name that is 7 or less chars in length
    """
    # namex examiner_names are {domain}{/}{username}
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


def generate_compressed_name(original_name: str) -> str:
    """
    returns a compressed name, formatted and truncated to fit in NRO
    :param original_name : a company full name
    :return: (str): a compressed name
    """
    # Removing all instances of "THE " and " THE "; no need to removed " THE".
    def _delete_the(in_name):
        out_name = in_name
        if len(in_name) > 4:
            if in_name[:4] == "THE ":
                out_name = in_name[4:]

            out_name = out_name.replace(" THE ", "")

        return out_name

    def _remove_char(in_name):
        chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ#&0123456789')

        return ''.join([c for c in in_name if c in chars])

    def _translate_char(in_name):

        rep = {"&": "AND",
               "#": "NUMBER",
               "1": "ONE",
               "2": "TWO",
               "3": "THREE",
               "4": "FOUR",
               "5": "FIVE",
               "6": "SIX",
               "7": "SEVEN",
               "8": "EIGHT",
               "9": "NINE",
               "0": "ZERO"}  # define desired replacements here

        rep = dict((re.escape(k), v) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))

        return pattern.sub(lambda m: rep[re.escape(m.group(0))], in_name)

    result_name = original_name.strip().upper()
    result_name = _delete_the(result_name)
    result_name = result_name.replace(" ", "")
    result_name = _remove_char(result_name)
    result_name = _translate_char(result_name)

    if result_name.startswith("BRITISHCOLUMBIA"):
        result_name = result_name.replace("BRITISHCOLUMBIA", "BC", 1)

    result_name = result_name[:30]  # Maximum 30 chars

    return result_name


