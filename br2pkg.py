# Python object representation of a buildroot package with JSON serialization
# (C) Andre Wolokita 2014
import json

class br2pkg():
    def __init__(self):
        self.conf = ""
        self.nam = ""
        self.dep = []
        self.hel = ""

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
