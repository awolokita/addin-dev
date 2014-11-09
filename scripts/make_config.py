# Make a .config file ready for buildroot make process
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

configsdir = env.configsPath
pkgmoddir = env.pkgmodPath

def getbase(base):
    base_config = configsdir + base
    # Check if base defconfig exists #
    if not os.path.isfile(base_config):
	print '\nNot a valid base defconfig file'
	return None
    # Check for no modules #
    if not len(pkgmodlist):
	print '\nNo package modules to add - run make now'
	return None
    return base_config

# @param base: base d
def getpkglist(pkgmodlist):
    pkglist = []

    # Loop through package modules #
    for pmod in pkgmodlist:
	pkgmodfile = pkgmoddir + pmod
        if not os.path.isfile(pkgmodfile):
            print '\nNot a valid package module file'
	    continue

	# Package module file exists! #
	json_data = open(pkgmodfile)
	data = json.load(json_data)
	pkgmod = br2pkgmod()
	pkgmod.from_JSON(data) # Fill the pkgmod from JSON
	
	# create a list of packages from pkdmod #
	for p in pkgmod.pkgs:
	    pkg = br2pkg()
	    pkg.from_JSON(p)
	    #print pkg.to_JSON()
	    pkglist.append(pkg)
    
    return pkglist



# use: make_config.py base_defconfig x-pkgmod.json y-pkgmod.json ...
if len(sys.argv) < 2:
    print 'Not enough args'
    sys.exit()

base = sys.argv[1]
pkgmodlist = sys.argv[2:]

b = getbase(base)
if not b:
    sys.exit()
print '\nBase defconfig:' + b + '\n'
l = getpkglist(pkgmodlist)
for x in l:
    print x.to_JSON()
