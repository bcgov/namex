"""
SQL Alchemy utils.
"""


def query_result_to_dict(key, values):
    """
    SQLAlchemy returns tuples, they need to be converted to dict so we can jsonify
    :return:
    """
    return dict(zip(key, values))
