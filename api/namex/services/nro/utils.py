
def nro_examiner_name(examiner_name): #-> (str)
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


def generate_compressed_name(original_name):

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

        out_name = in_name

        for c in out_name:
            if not (c in chars):
                out_name = out_name.replace(c, "")

        return out_name

    def _translate_char(in_name):
        out_name = in_name.replace('&', 'AND')
        out_name = out_name.replace('#', 'NUMBER')
        out_name = out_name.replace('1', 'ONE')
        out_name = out_name.replace('2', 'TWO')
        out_name = out_name.replace('3', 'THREE')
        out_name = out_name.replace('4', 'FOUR')
        out_name = out_name.replace('5', 'FIVE')
        out_name = out_name.replace('6', 'SIX')
        out_name = out_name.replace('7', 'SEVEN')
        out_name = out_name.replace('8', 'EIGHT')
        out_name = out_name.replace('9', 'NINE')
        out_name = out_name.replace('0', 'ZERO')
        return out_name

    def _translate_bc(in_name):
        out_name = in_name
        if len(in_name) > 15:
            if "BRITISHCOLUMBIA" in in_name[:15]:
                out_name = in_name[:15].replace("BRITISHCOLUMBIA", "BC") + in_name[15:]

        return out_name

    def _truncate(in_name):
        out_name = in_name
        if len(in_name) > 30:
            out_name = in_name[:30]

        return out_name

    result_name = original_name.strip().upper()
    result_name = _delete_the(result_name)
    result_name = result_name.replace(" ", "")
    result_name = _remove_char(result_name)
    result_name = _translate_char(result_name)
    result_name = _translate_bc(result_name)
    result_name = _truncate(result_name)

    return result_name
