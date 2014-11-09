# Python object representation of a buildroot package with JSON serialization
# (c) 2014 Andre Wolokita
import json

class br2pkg():
    def __init__(self):
        self.config = ""
        self.name = ""
        self.depends = []
        self.msg = ""
        self.tags = []
    
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    # Pull data from JSON #
    def from_JSON(self,data):
        self.config = data["config"]
        self.name = data["name"]
        self.depends = data["depends"]
        self.msg = data["msg"]
	self.tags = data["tags"]

