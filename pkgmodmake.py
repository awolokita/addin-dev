# Create package ball
# (c) 2014 Andre Wolokita

from br2pkg import br2pkg
from br2pkgmod import br2pkgmod
from common import env_info
import json

json_data = open('net.modconfig')

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

data = json.load(json_data)
data2 = convert(data)

