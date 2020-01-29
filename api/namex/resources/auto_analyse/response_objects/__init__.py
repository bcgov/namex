from flask import json


class Serializable:
    def to_json(self):
        return json.dumps(self,
              separators=(',', ':'),
              default=lambda o: o.__dict__,
              sort_keys=True, indent=0).replace('\n', '')