# A script that walks through directories in the buildroot ./package directory,
# finds a specific pkg.json and adds tags from command line parameters
# (C) Andre Wolokita 2014
# TODO Add tag deletion
# TODO Handle duplicate tags
#

import os #for walk
import fnmatch #file name checking
import re #regex
from br2pkg import br2pkg
from common import env_info
import sys
import json

#path#
env = env_info()
#parameters#
if len(sys.argv) < 3:
    print 'Not enough arguments.'
    print 'Usage: python tags.py N CONFIG_LINE ... TAGS ...'
    print 'Example: python tags.py 2 BR2_PACKAGE_NGREP BR2_PACKAGE_LINPHONE foo bar baz'
    sys.exit()

# is the first param a number? #
try:
  n_config = int(sys.argv[1])
except ValueError:
   print("First parameter is non-integer")
   sys.exit()

config = sys.argv[2:2+n_config]
print config
tags = sys.argv[2+n_config:]
print tags

pkgdir = '/home/cxcn/blackfin-source/buildroot/blackfin-buildroot/package'
pkgdir = env.packagePath

def config_check(pats,line):
    for pat in pats:
        if re.match(pat,line):
	    return 1
    return 0

for subdir, dirs, files in os.walk(pkgdir):
    for file in files:
        if fnmatch.fnmatch(file, 'pkg.json'):
            pkg = br2pkg();
            json_data = open(os.path.join(subdir, file))
	    data = json.load(json_data)
	    #for pat in config
	    #    if not re.match(config,data["config"]):
	    #	    continue
	    if not config_check(config,data["config"]):
		continue
	    # pull json into br2pkg #
	    pkg.config = data["config"]
	    pkg.name = data["name"]
	    pkg.msg = data["msg"]
	    pkg.tags = data["tags"]
	    pkg.depends = data["depends"]

	    # append tags #
	    pkg.tags.extend(tags)
	    #json_data.write(pkg.to_JSON)
            fi = open(subdir+'/'+'pkg.json', 'w')
            fi.write(pkg.to_JSON())
	    fi.close()
	    print "done"
            json_data.close()
