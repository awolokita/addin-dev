# Create buildroot package module from tag
# TODO Multi-tag?
# (c) 2014 Andre Wolokita

from br2pkg import br2pkg
from br2pkgmod import br2pkgmod
from common import env_info
import json
import sys
import os
import fnmatch
import re
env = env_info()

if len(sys.argv) < 2:
    print 'Not enough args'
    sys.exit()

tag = sys.argv[1]
pkgdir = env.brPath + '/../package'

# Convert JSON to strings from unicode or whatever
def convert(input): 
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

# match tag in given data.tags #
def tag_check(pat,line):
    for tags in line:
        if re.match(pat,tags):
            return 1
    return 0

pkgmod = br2pkgmod()
pkgmod.name = tag
pkgmod.msg = 'Test buildroot package module\n'

for subdir, dirs, files in os.walk(pkgdir):
    for file in files:
        if fnmatch.fnmatch(file, 'pkg.json'):
            pkg = br2pkg();
            json_data = open(os.path.join(subdir, file))
            data = json.load(json_data)
            if not tag_check(tag,data["tags"]):
                continue
	    print 'found: ' + data["config"]
            # pull json into br2pkg #
            pkg.config = data["config"]
            pkg.name = data["name"]
            pkg.msg = data["msg"]
            pkg.tags = data["tags"]
            pkg.depends = data["depends"]

	    pkgmod.pkgs.append(pkg) # add the pkg.json to the module
print pkgmod.to_JSON()
fi = open(env.brPath + '/' + tag + '-pkgmod.json','w')
fi.write(pkgmod.to_JSON())
#data = json.load(json_data)
#data2 = convert(data)


