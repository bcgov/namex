from datetime import (datetime)

from .name_analysis_director import NameAnalysisDirector

from .mixins.set_designation_lists import SetDesignationsListsMixin

'''
The ProtectedNameAnalysisService returns an analysis response using the strategies in analysis_strategies.py
The response API return cases are as follows:

- Requires addition of distinctive word
- Requires addition of descriptive word
- Name Contains a Word To Avoid
- Designation Mismatch
- Too Many Words
- Name Requires Consent
- Contains Unclassifiable Word
- Conflicts with the Corporate Database

Notes:
- The 'algorithm' / process we use to analyse names may change in the future
- Using the builder pattern allows us delegate and isolate custom / changing business logic to the builder,
  while exposing a consistent API for consumers of the service.
'''

d = datetime.now()  # Was just used for perf analysis


class ProtectedNameAnalysisService(NameAnalysisDirector, SetDesignationsListsMixin):
    _d = d  # Just used for perf

    def __init__(self):
        super(ProtectedNameAnalysisService, self).__init__()

    '''
    do_analysis is an abstract method inherited from NameAnalysisDirector must be implemented.
    This is the main execution call for running name analysis checks.
    @:return ProcedureResult[]
    '''

    def do_analysis(self):
        builder = self.builder

        results = []

        # Return any combination of these checks
        if not self.skip_search_conflicts:
            check_conflicts = builder.search_conflicts(
                [self.get_list_dist()],
                [self.get_list_desc()],
                self.name_tokens,
                self.processed_name
            )

            if not check_conflicts.is_valid:
                results.append(check_conflicts)

        # TODO: Use the list_name array, don't use a string in the method!
        # check_words_requiring_consent = builder.check_words_requiring_consent(list_name)  # This is correct
        check_words_requiring_consent = builder.check_words_requiring_consent(
            self.name_tokens, self.processed_name
        )

        if not check_words_requiring_consent.is_valid:
            results.append(check_words_requiring_consent)

        # Set designations and run our check
        self._set_designations()

        check_designation_existence = builder.check_designation_existence(
            self.get_original_name_tokenized(),
            self.get_all_designations(),
            self.get_all_designations_user()
        )

        if not check_designation_existence.is_valid:
            results.append(check_designation_existence)
        else:
            check_designation_mismatch = builder.check_designation_mismatch(
                self.get_original_name_tokenized(),
                self.entity_type,
                self.get_all_designations(),
                self.get_all_designations_user()
                # self.get_all_designations_user_no_periods()
            )

            if not check_designation_mismatch.is_valid:
                results.append(check_designation_mismatch)

            check_designation_more_than_one = builder.check_end_designation_more_than_once(
                self.get_original_name_tokenized(),
                self.get_designation_end_list(),
                self.get_all_designations_user(),
                self.get_misplaced_designation_end()
            )

            if not check_designation_more_than_one.is_valid:
                results.append(check_designation_more_than_one)
            else:
                check_designation_misplaced = builder.check_designation_misplaced(
                    self.get_original_name_tokenized(),
                    self.get_misplaced_designation_end()
                )

                if not check_designation_misplaced.is_valid:
                    results.append(check_designation_misplaced)

        check_special_words = builder.check_word_special_use(
            self.name_tokens,
            self.get_processed_name()
        )

        if not check_special_words.is_valid:
            results.append(check_special_words)

        return results
