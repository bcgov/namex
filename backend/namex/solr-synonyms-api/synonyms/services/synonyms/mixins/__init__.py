class SynonymServiceMixin(object):
    _model = None

    # This must be defined for all mixins
    def get_model(self):
        return self._model
