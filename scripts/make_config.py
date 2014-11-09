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

def makeconfig(base, pkgmodlist):
    if not len(pkgmodlist):
	print "foo"

# use: make_config.py base_defconfig x-pkgmod.json y-pkgmod.json ...
if len(sys.argv) < 2:
    print 'Not enough args'
    sys.exit()

base = sys.argv[1]
pkgmodlist = sys.argv[2:]

makeconfig(base, pkgmodlist)
