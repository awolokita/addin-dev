# A script that walks through directories in the buildroot ./package directory,
# finds a specific pkg.json and adds tags from command line parameters
# (C) Andre Wolokita 2014
# TODO Add tag deletion
# TODO Handle duplicate tags
# TODO Handle multiple pkg.json configs

import os #for walk
import fnmatch #file name checking
import re #regex
from br2pkg import br2pkg
from common import env_info
import sys
import json
from collections import namedtuple
#path#
env = env_info()
#parameters#
if len(sys.argv) < 2:
    print 'not enough args'
    sys.exit()

config = sys.argv[1]
tags = sys.argv[2:]

pkgdir = '/home/cxcn/blackfin-source/buildroot/blackfin-buildroot/package'
pkgdir = env.brPath + '/../package'


for subdir, dirs, files in os.walk(pkgdir):
    for file in files:
        if fnmatch.fnmatch(file, 'pkg.json'):
            pkg = br2pkg();
            json_data = open(os.path.join(subdir, file))
	    data = json.load(json_data)
	    if not re.match(config,data["config"]):
		continue
	    # pull json into br2pkg #
	    pkg.config = data["config"]
	    pkg.name = data["name"]
	    pkg.msg = data["msg"]
	    pkg.tags = data["tags"]
	    pkg.depends = data["depends"]

	    # append tags #
	    pkg.tags.append(tags)
	    print pkg.config
	    #json_data.write(pkg.to_JSON)
            json_data.close()
