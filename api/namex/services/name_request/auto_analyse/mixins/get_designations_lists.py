class GetDesignationsListsMixin(object):
    # designated_end/any_words contain all the end/any designations for all Entity Types
    _designated_end_words = []
    _designated_any_words = []

    _designated_all_words = []

    _eng_designated_end_words = []
    _eng_designated_any_words = []

    _fr_designated_end_words = []
    _fr_designated_any_words = []

    # Designation_any_list_user and designation_end_list_user based on entity type typed by user:
    _designation_any_list_correct = []
    _designation_end_list_correct = []

    _eng_designation_any_list_correct = []
    _eng_designation_end_list_correct = []

    _fr_designation_any_list_correct = []
    _fr_designation_end_list_correct = []

    _eng_designation_all_list_correct = []
    _fr_designation_all_list_correct = []

    _all_designations_user = []
    # _all_designations_user_no_periods = []

    # All designations for entity type typed bu user
    designations_entity_type_user = []

    # Designation_any_list and designation_end_list based on company name typed by user
    _all_designations = []
    _designation_any_list = []
    _designation_end_list = []

    # Wrong any_list and end_list based on company name typed by user
    _misplaced_designation_any_list = []
    _misplaced_designation_end_list = []
    _misplaced_designation_all_list = []

    # Entity type(s) for designations related to company name typed by user:
    _entity_type_any_designation = []
    _entity_type_end_designation = []

    # All possible entity types found related to company name.
    _all_entity_type = []

    _designation_any_list_all = []
    _designation_end_list_all = []

    _entity_end_designation_dict = {}
    _entity_any_designation_dict = {}

    def get_designated_end_words(self):
        return self._designated_end_words

    def get_designated_any_words(self):
        return self._designated_any_words

    def get_designated_all_words(self):
        return self._designated_all_words

    def get_eng_designated_end_words(self):
        return self._eng_designated_end_words

    def get_eng_designated_any_words(self):
        return self._eng_designated_any_words

    def get_fr_designated_end_words(self):
        return self._fr_designated_end_words

    def get_fr_designated_any_words(self):
        return self._fr_designated_any_words

    def get_designation_any_list_correct(self):
        return self._designation_any_list_correct

    def get_designation_end_list_correct(self):
        return self._designation_end_list_correct

    def get_eng_designation_any_list_correct(self):
        return self._eng_designation_any_list_correct

    def get_eng_designation_end_list_correct(self):
        return self._eng_designation_end_list_correct

    def get_fr_designation_any_list_correct(self):
        return self._fr_designation_any_list_correct

    def get_fr_designation_end_list_correct(self):
        return self._fr_designation_end_list_correct

    def get_misplaced_designation_any(self):
        return self._misplaced_designation_any_list

    def get_misplaced_designation_end(self):
        return self._misplaced_designation_end_list

    def get_misplaced_designation_all(self):
        return self._misplaced_designation_all_list

    def get_entity_type_any_designation(self):
        return self._entity_type_any_designation

    def get_entity_type_end_designation(self):
        return self._entity_type_end_designation

    def get_all_designations_user(self):
        return self._all_designations_user

    # def get_all_designations_user_no_periods(self):
    #    return self._all_designations_user_no_periods

    def get_all_designations(self):
        return self._all_designations

    def get_designation_any_list(self):
        return self._designation_any_list

    def get_designation_end_list(self):
        return self._designation_end_list

    def get_designation_any_list_all(self):
        return self._designation_any_list_all

    def get_designation_end_list_all(self):
        return self._designation_end_list_all
