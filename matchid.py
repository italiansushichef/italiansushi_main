from riotwatcher import RiotWatcher, NORTH_AMERICA
import urllib2, json

w = RiotWatcher('cf473e24-e25e-4402-bdcc-9cb756e90161')
API_KEY = 'cf473e24-e25e-4402-bdcc-9cb756e90161'

if w.can_make_request() == True:
    yes = urllib2.urlopen('https://na.api.pvp.net/api/lol/na/v2.2/matchlist/by-summoner/21796238?rankedQueues=RANKED_SOLO_5x5,RANKED_TEAM_5x5&seasons=SEASON2015&api_key=' + API_KEY)
    data = json.load(yes)
    yes.close()
    with open('static/json-data/matchid.json','w') as outfile:
        json.dump(data, outfile, indent=4)
        
else:
    print "False"