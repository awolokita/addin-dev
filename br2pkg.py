# Python object representation of a buildroot package with JSON serialization
# (c) 2014 Andre Wolokita
import json

class br2pkg():
    def __init__(self):
        self.conf = ""
        self.nam = ""
        self.dep = []
        self.hel = ""

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
