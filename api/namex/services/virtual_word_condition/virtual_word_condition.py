from sqlalchemy.sql.expression import false, true

from namex.criteria.virtual_word_condition.query_criteria import VirtualWordConditionCriteria
from namex.models import VirtualWordCondition

from namex.utils.common import flatten_tuple_results


class VirtualWordConditionService:
    _model = None

    def __init__(self):
        self._model = VirtualWordCondition

    def get_model(self):
        return self._model

    def get_words_to_avoid(self):
        model = self.get_model()

        filters = [
            model.rc_allow_use == false(),
        ]

        criteria = VirtualWordConditionCriteria(
            fields=[model.rc_words],
            filters=filters
        )

        results = model.find_by_criteria(criteria)
        flattened = list(map(str.strip, (list(filter(None, flatten_tuple_results(results))))))
        return flattened

    def get_words_requiring_consent(self):
        model = self.get_model()

        filters = [
            model.rc_allow_use == true(),
            model.rc_consent_required == true(),
        ]

        criteria = VirtualWordConditionCriteria(
            fields=[model.rc_words],
            filters=filters
        )

        results = model.find_by_criteria(criteria)
        flattened = list(map(str.strip, (list(filter(None, flatten_tuple_results(results))))))
        return flattened

    def get_word_special_use(self):
        model = self.get_model()

        filters = [
            model.rc_consent_required == false(),
            model.rc_allow_use == true(),
        ]

        criteria = VirtualWordConditionCriteria(
            fields=[model.rc_words],
            filters=filters
        )

        results = model.find_by_criteria(criteria)
        flattened = list(map(str.strip, (list(filter(None, flatten_tuple_results(results))))))
        return flattened
