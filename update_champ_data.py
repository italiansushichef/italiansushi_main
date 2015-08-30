import urllib2, json, sys, os
from datetime import datetime

today = datetime.now()


if len(sys.argv) != 2:
	print "usage: python update_champ_data.py [API_KEY]"
	sys.exit()
API_KEY = sys.argv[1]
# get list of champions
response = urllib2.urlopen('https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion?api_key=' + API_KEY)
data = json.load(response)
response.close()
with open('static/json-data/champls.json', 'w') as outfile:
	json.dump(data, outfile, indent=4)

filepath = 'static/json-data/updatetime.json'

if os.path.isfile(filepath):
    with open(filepath, 'r') as readfile:
        filedata = json.load(readfile)
        filedata['Updates']['Update Champ Data'] = today.strftime('Updated on %m/%d/%Y %H:%M')

with open(filepath, 'w') as outfile:
    json.dump(filedata,outfile, indent = 4)