# This class represtents a buildroot configuration 'module'
# TODO Designator assignment - based on hash of pkg list, perhaps?
# TODO
#(C) Andre Wolokita 2014
import json

class br2pkgmod():
    def __init__(self):
        self.nam = ""   # human readable name of module
        self.des = 0    # a designator for the module
        self.pkgs = []
        self.hel = ""   # description of config/package module

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
