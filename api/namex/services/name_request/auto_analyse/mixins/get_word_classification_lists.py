class GetWordClassificationListsMixin(object):
    _list_name_words = []
    _list_dist_words = []
    _list_desc_words = []
    _list_none_words = []

    def get_list_name(self):
        return self._list_name_words

    def get_list_dist(self):
        return self._list_dist_words

    def get_list_desc(self):
        return self._list_desc_words

    def get_list_none(self):
        return self._list_none_words
