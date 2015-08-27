import urllib2, json, sys, osfrom riotwatcher import RiotWatcherif len(sys.argv) != 4:    print "usage: python matchid.py [champid] [max_matches] [API_KEY]"    sys.exit(0)champid = int(sys.argv[1])max_matches = int(sys.argv[2])d = []API_KEY = sys.argv[3]w = RiotWatcher(API_KEY)sumfile = 'static/json-data/summonerids.json'with open(sumfile, 'r') as readfile:    sumdata = json.load(readfile)    summid = sumdata['summonerids'] i = 1j = 1while len(d) < max_matches:    if w.can_make_request() == True and j < 200:        readfile = urllib2.urlopen('https://na.api.pvp.net/api/lol/na/v2.2/matchlist/by-summoner/' + str(summid[i]) +  '?championIds=' + str(champid) + '&rankedQueues=RANKED_SOLO_5x5&seasons=SEASON2015&api_key=' + API_KEY)        data = json.load(readfile)        if data["totalGames"] != 0:            for match in data["matches"]:                if match["matchId"] not in d:                    d.append(match["matchId"])        i += 1        j += 1            filepath = 'static/json-data/matchids.json'output={'count':max_matches, 'matchids':d[:max_matches], 'champid':champid}if os.path.isfile(filepath):    with open(filepath, 'r') as readfile:        filedata = json.load(readfile)        if filedata and filedata['count'] and filedata['matchids']:            for mid in filedata['matchids']:                if mid not in output['matchids']:                    output['matchids'].append(mid)                    output['count'] += 1                    with open(filepath, 'w') as outfile:    json.dump(output, outfile, indent = 4)    print output['count']print "done"            