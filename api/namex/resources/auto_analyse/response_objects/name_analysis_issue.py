from . import Serializable


class NameAnalysisIssue(Serializable):
    def __init__(self, **kwargs):
        self.line1 = kwargs['line1'] if kwargs.get('line1') else None
        self.line2 = kwargs['line2'] if kwargs.get('line2') else None
        self.consenting_body = kwargs['consenting_body'] if kwargs.get('consenting_body') else None  # None <ConsentingBody>[]
        self.designations = kwargs['designations'] if kwargs.get('designations') else None  # <string>[] | None
        self.descriptiveWords = kwargs['descriptiveWords'] if kwargs.get('descriptiveWords') else None  # <DescriptiveWord>[]
        # [add_descriptive | word_to_avoid | excess_words | consent_required | unclassified_word]
        self.issue_type = kwargs['issue_type'] if kwargs.get('issue_type') else None  # <string> | None
        # TODO: Remove word and wordIndex and descriptiveWords
        # self.word = kwargs['word'] if kwargs.get('word') else None  # <string> | None
        # self.word_index = kwargs['wordIndex'] if kwargs.get('word_index') else None  # <integer> | None
        # self.descriptive_words = kwargs['descriptive_words'] if kwargs.get('descriptive_words') else None  # <DescriptiveWord>[]
        self.show_reserve_button = kwargs['show_reserve_button'] if kwargs.get('show_reserve_button') else False  # <boolean>
        self.show_examination_button = kwargs['show_examination_button'] if kwargs.get('show_examination_button') else False  # <boolean>
        self.conflicts = kwargs['conflicts'] if kwargs.get('conflicts') else None  # <Conflict>[] | None
        # TODO: Get rid of options
        self.setup = kwargs['setup'] if kwargs.get('setup') else None
        # options: number, header: text, text1: text, text2: text, checkbox: obj, button: obj
        # self.options = kwargs['options'] if kwargs.get('options') else None  # TODO: What is this shape?
        self.name_actions = kwargs['name_actions'] if kwargs.get('name_actions') else None  # <NameAction>[] | None
