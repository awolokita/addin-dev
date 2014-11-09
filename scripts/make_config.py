# Make a .config file ready for buildroot make process
# TODO user supplied output config file name
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
#for testing #
testconfigfile = open(configsdir + '/test.config', 'a')

def getbase(base):
    base_config = configsdir + base
    # Check if base defconfig exists #
    if not os.path.isfile(base_config):
	print '\nNot a valid base defconfig file'
	return None

    return base_config

# Return a list of packages from a list of package modules
# TODO Maybe create a class: br2pkgmodlist ?
def getpkglist(pkgmodlist):
    # Check for no modules #
    if not len(pkgmodlist):
	print '\nNo package modules to add - run make now'
	return None
    
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

# Takes list of packages and returns a set of config tokens
# Unordered and no duplicates
def getconfigset(pkglist):
    configlist = []
    for pkg in pkglist:
        configlist.append(pkg.config)
    return set(configlist)

def checkconfigtoken(f,t):
    baseconfig = open(b)
    for line in baseconfig:
	if re.match('^'+t+'=.*',line):
	    print 'foo'
	    return None
    return 1

# Form the config file
# TODO Make this actually efficient
def formconfigfile(b,configset):
    baseconfig = open(b)
    # Copy base into new config #
    for line in baseconfig:
	testconfigfile.write(line)
    for c in configset:
        if not checkconfigtoken(b,c):
	    #print c +' already included in base config'
	    continue
	testconfigfile.write('\n'+ c + '=y')

# use: make_config.py base_defconfig x-pkgmod.json y-pkgmod.json ...
if len(sys.argv) < 2:
    print 'Not enough args'
    sys.exit()

base = sys.argv[1]
pkgmodlist = sys.argv[2:]

b = getbase(base) #Check and form path to base config
if not b:
    sys.exit()
print '\nBase defconfig:' + b + '\n'
pkglist = getpkglist(pkgmodlist) #Check and form list of br2pkgs
if not pkglist:
    sys.exit()
configset = getconfigset(pkglist) # Form non-duplicate set of config tokens
formconfigfile(b, configset)

#print configset
#for x in l:
#    print x.to_JSON()

