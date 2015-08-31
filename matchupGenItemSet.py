import urllib2, json, sys, os
from riotwatcher import RiotWatcher

if len(sys.argv) != 6:
    print "usage: python matchupGetItemSet.py [maxMatchesParsed] [champ1 id] [champ2 id] [lane] [API_KEY]"
    sys.exit(0)
maxMatchesParsed = int(sys.argv[1])
champ1 = int(sys.argv[2])
champ2 = int(sys.argv[3])
lane = sys.argv[4]
API_KEY = sys.argv[5]


matchesfile = 'static/json-data/matchidstest.json'
with open(matchesfile, 'r') as readfile:
    sumdata = json.load(readfile)
    for match in sumdata['matches']:
    	matchid = match['recentmatchId']
    	for player in match['champs']:
    		champid = player['id']
    		print champid

url = 'https://na.api.pvp.net/api/lol/na/v2.2/match/' + str(matchid) +  '?includeTimeline=true&api_key=' + API_KEY
readMatchDetailsFile = urllib2.urlopen(url)
matchDetailsData = json.load(readMatchDetailsFile)

for x in matchDetailsData[]: