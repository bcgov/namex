class GetWordClassificationListsMixin(object):
    _list_name_words = []
    _list_dist_words = []
    _list_desc_words = []
    _list_dist_words_search_conflicts = []
    _list_desc_words_search_conflicts = []
    _dict_desc_words_search_conflicts = {}
    _list_none_words = []
    _list_processed_names = []
    _list_incorrect_classification = []
    _dict_name_words_search_conflicts = {}
    _dict_name_words = {}

    def get_list_name(self):
        return self._list_name_words

    def get_list_dist(self):
        return self._list_dist_words

    def get_list_desc(self):
        return self._list_desc_words

    def get_list_dist_search_conflicts(self):
        return self._list_dist_words_search_conflicts

    def get_list_desc_search_conflicts(self):
        return self._list_desc_words_search_conflicts

    def get_dict_desc_search_conflicts(self):
        return self._dict_desc_words_search_conflicts

    def get_list_none(self):
        return self._list_none_words

    def get_list_incorrect_classification(self):
        return self._list_incorrect_classification

    def get_dict_name(self):
        return self._dict_name_words

    def get_dict_name_search_conflicts(self):
        return self._dict_name_words_search_conflicts

    def get_processed_names(self):
        return self._list_processed_names
