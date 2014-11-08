# A script that walks through all directories in the buildroot ./package directory
# and creates JSON data structures of buildroot packages.
# TODO Handle multiple config tokens in one Config.in (nested)
# TODO Handle Config.*.in files
# TODO Handle menu items and selections
# TODO Handle "depend on"s with multiple OR (||) separated BR2_*
# TODO Handle multi line deps (with \ as next line token)
#      Right now the deps shouldn't be used for anything important
#
# (C) Andre Wolokita 2014
#
import os #for walk
import fnmatch #file name checking
import re #regex
from br2pkg import br2pkg

pkgdir = '/home/cxcn/blackfin-source/buildroot/blackfin-buildroot/package'

# some regex defs.
reg_conf = '^config'            #pkg config line for .config
reg_nam = '^\tbool'             #name of pkg in menuconfig
reg_dep = '^\tdepends on'       #pkg dependencies
reg_hel = '^\thelp'             #package description comes after this

reg_hel_end = '^\t  '           #end of help section

# some flags for Config.in parsing
f_help = 0      #flag set high on reg_hel match
f_conf = 0      #flag set high after first config
                #use to only grab top level config in Config.in
                #TODO: enable nested configs
f_conf_just_set = 0

for subdir, dirs, files in os.walk(pkgdir):
    for file in files:
        if fnmatch.fnmatch(file, '*.in'):
            # new instance of br2pkg - we're only going one deep for now #
            pkg = br2pkg();
            #print os.path.join(subdir, file)
            f = open(os.path.join(subdir, file))
            for line in f:
                #Parsing for bools
                if f_conf_just_set and re.match(reg_nam,line):
                    f_conf_just_set = 0
                    nam = line.strip('\tbool ')
                    nam = re.sub('"','',nam)
                    nam = nam.strip('\n')
                    pkg.nam = nam

                # Parsing the config symbol
                if re.match(reg_conf,line) and not f_conf:
                    #print 'foo'
                    f_conf = 1 #no more configs after this
                    f_conf_just_set = 1
                    conf = line.strip('config ') # get only the
                    conf = conf.strip('\n')      # BR2_* part
                    pkg.conf = conf              # assign it to our br2pkg class
                    #print pkg.conf
                    continue

                # Parsing the help block #
                if f_help and not re.match(reg_hel_end,line) and not re.match('\n',line):
                    #print 'help end'
                    f_help = 0                  #end of help section
                    continue
                if f_help:                      #in help section
                    #print line                 #adding more \n, need to trim
                    pkg.hel = pkg.hel + line
                    continue
                if re.match(reg_hel, line):
                    f_help = 1                  #start of help section
                    #print os.path.join(subdir,file) + "\n" + line
                    continue

                if re.match(reg_dep, line):
                    deps = line.strip('\tdepends on ')
                    deps = deps.strip(' *')
                    deps = re.sub('[a-z\W]*','',deps)
                    deps = deps.strip('\n')
                    pkg.dep.append(deps)
                    #print deps
                    continue

            f.close()
            f_help = 0
            f_conf = 0
            #print pkg.conf
            #print pkg.nam
            #print pkg.hel
            #print pkg.dep
            #print(pkg.to_JSON())
            fi = open(subdir+'/'+'pkg.json', 'w')
            fi.write(pkg.to_JSON())
            print subdir+'/'
