import re

# multi word synonyms are not allowed here
def get_multi_word_synonyms(values) -> None:
    disallowed_values = []
    for value in values:
        if re.search(r'\b\s+\b', value):
            disallowed_values.append(value)

    return disallowed_values
