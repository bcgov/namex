from flask import json
import jsonpickle


class Serializable:
    def to_json(self):
        return jsonpickle.encode(self)