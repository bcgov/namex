import jsonpickle


class Serializable:
    def to_json_test(self):
        # Allows us to unwrap the response when we're running pytests
        return jsonpickle.encode(self)

    def to_json(self):
        return jsonpickle.encode(self, unpicklable=False)
