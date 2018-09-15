

def nro_examiner_name(examiner_name): #-> (str)
    """returns an examiner name, formated and tuncated to fit in NRO
    :examiner_name (str): an examiner name, as found in NameX
    :returns (str): an examiner name that is 7 or less chars in length
    """
    #namex examiner_names are {domain}{/}{username}
    start = examiner_name.find('/')+1
    return examiner_name[start:start+7]
