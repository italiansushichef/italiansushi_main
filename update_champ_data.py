import urllib2, json, sys

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

