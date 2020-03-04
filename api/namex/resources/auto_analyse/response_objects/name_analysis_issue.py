from . import Serializable


class NameAnalysisIssue(Serializable):
    def __init__(self, **kwargs):
        self.line1 = kwargs.get('line1', None)
        self.line2 = kwargs.get('line2', None)
        self.consenting_body = kwargs.get('consenting_body', None)  # None <ConsentingBody>[]
        self.designations = kwargs.get('designations', None)  # <string>[] | None
        # [add_descriptive | word_to_avoid | excess_words | consent_required | unclassified_word]
        self.issue_type = kwargs.get('issue_type', None)  # <string> | None
        # TODO: Remove word and wordIndex and descriptiveWords
        # self.word = kwargs.get('word', None)  # <string> | None
        # self.word_index = kwargs.get('wordIndex', None)  # <integer> | None
        # self.descriptive_words = kwargs.get('descriptive_words', None)  # <DescriptiveWord>[]
        self.show_next_button = kwargs.get('show_next_button', False)  # <boolean>
        self.show_reserve_button = kwargs.get('show_reserve_button', False)  # <boolean>
        self.show_examination_button = kwargs.get('show_examination_button', False)  # <boolean>
        self.conflicts = kwargs.get('conflicts', None)  # <Conflict>[] | None
        # TODO: Get rid of options
        self.setup = kwargs.get('setup', None)
        # options: number, header: text, text1: text, text2: text, checkbox: obj, button: obj
        # self.options = kwargs.get('options', None)  # TODO: What is this shape?
        self.name_actions = kwargs.get('name_actions', None)  # <NameAction>[] | None
