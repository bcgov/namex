# match whole/start/end string  NR 1234567, NR1234567
import re

nr_num_regex = r'(^(NR( |)\d+)$)|(^(NR( |)\d+)\s)|(\s(NR( |)\d+)$)'
nr_num_fallback_regex = r'(^\d+$)|(^\d+\s)|(\s\d+$)'  # 1234567


def get_nr_num_from_query(value) -> str | None:
    """Look for nr_num in value and return nr_num in NR XXXXXXXX format."""
    nr_number = None
    if result := re.search(nr_num_regex, value, re.IGNORECASE):
        matching_nr = result.group()
        nr_number = re.sub('NR', '', matching_nr, flags=re.IGNORECASE).strip()
    elif result := re.search(nr_num_fallback_regex, value):
        nr_number = result.group().strip()

    if nr_number:
        return f'NR {nr_number}'

    return None
