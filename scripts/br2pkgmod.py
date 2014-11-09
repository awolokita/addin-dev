# This class represtents a buildroot configuration 'module'
# TODO Designator assignment - based on hash of pkg list, perhaps?
# TODO Actually use br2pck objects in the pkgs list?
# (c) 2014 Andre Wolokita
import json
from br2pkg import br2pkg

class br2pkgmod():
    def __init__(self):
        self.name = ""   # human readable name of module
        self.designator = 0    # a designator for the module
        self.pkgs = []
        self.msg = ""   # description of config/package module

    # Serialise to JSON #
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    # Pull data from JSON #
    def from_JSON(self,data):
	self.name = data["name"]
	self.designator = data["designator"]
	self.pkgs = data["pkgs"]
	self.msg = data["msg"]

