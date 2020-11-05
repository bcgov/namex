import jsonpickle


class Serializable(dict):
    def as_dict(self):
        return self.__dict__

    def to_json_test(self):
        # Allows us to unwrap the response when we're running pytests
        return jsonpickle.encode(self)

    def to_json(self):
        return jsonpickle.encode(self, unpicklable=False, warn=True)
