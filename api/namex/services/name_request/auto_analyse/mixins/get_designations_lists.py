class GetDesignationsListsMixin(object):
    _designated_end_words = []
    _designated_any_words = []

    # Designation_any_list_user and designation_end_list_user based on entity type typed by user:
    _designation_any_list_correct = []
    _designation_end_list_correct = []
    _all_designations_user = []

    # All designations for entity type typed bu user
    designations_entity_type_user = []

    # Designation_any_list and designation_end_list based on company name typed by user
    # _designation_any_list = []
    # _designation_end_list = []
    _all_designations = []

    # Wrong any_list and end_list based on company name typed by user
    _misplaced_designation_any_list = []
    _misplaced_designation_end_list = []
    _misplaced_designation_all_list = []

    # Entity type(s) for designations related to company name typed by user:
    _entity_type_any_designation = []
    _entity_type_end_designation = []

    # All possible entity types found related to company name.
    _all_entity_type = []

    _entity_end_designation_dict = {}
    _entity_any_designation_dict = {}

    def get_designated_end_words(self):
        return self._designated_end_words

    def get_designated_any_words(self):
        return self._designated_any_words

    # def get_misplaced_designation_in_input_name(self):
    #    return self._misplaced_designation

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

    def get_all_entity_types(self):
        return self._all_entity_types

    def get_all_designations_user(self):
        return self._all_designations_user

    def get_all_designations(self):
        return self._all_designations
