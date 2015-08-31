import urllib2, json, sys, os
from riotwatcher import RiotWatcher

if len(sys.argv) != 4:
    print "usage: python parseMatchid.py [startIndex] [endIndex][API_KEY]"
    sys.exit(0)
startIndex = int(sys.argv[1])
endIndex = int(sys.argv[2])
API_KEY = sys.argv[3]
#w = RiotWatcher(API_KEY)

parsedIds = []

matchIdsBIG = 'static/json-data/matchids.json' #the file of match ids to be parsed
with open(matchIdsBIG, 'r') as readfile:
    idsData = json.load(readfile)['matches'][startIndex:endIndex]

#print idsData["match_count"]
#print idsData['matches'][endIndex]['recentmatchId']

for i in idsData:
    matchId = i['recentmatchId']
    isNew = True
    for p in parsedIds:
        if p["matchid"] == matchId:
            isNew = False
            break
    if isNew:
        parsedIds.append({"matchid": matchId, "champions":[]})

#print parsedIds
itemEvents = ["ITEM_PURCHASED", "ITEM_DESTROYED", "ITEM_SOLD"]
relevantStats = ["item0","item1","item2","item3","item4","item5","item6","sightWardsBoughtInGame","visionWardsBoughtInGame","wardsKilled","wardsPlaced", "winner"]
    
for parsedId in parsedIds:
    matchid = parsedId["matchid"]
    url = 'https://na.api.pvp.net/api/lol/na/v2.2/match/' + str(matchid) + '?includeTimeline=true&api_key=' + API_KEY
    readMatchDetails = urllib2.urlopen(url)
    matchDetailsData = json.load(readMatchDetails)
    parsedId["duration"] = matchDetailsData["matchDuration"]
    for player in matchDetailsData['participants']:
        champion = {"statistics":{}, "eventlist":[]}
        champion["id"] = player["championId"]
        champion["position"] = player["timeline"]["lane"]
        for stat in relevantStats:
            champion["statistics"][stat] = player["stats"][stat] 
        champParticId = player["participantId"]
        #print str(champParticId) + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        #eventNum = -1
        for frame in matchDetailsData['timeline']['frames']:
            if "events" in frame:            
                for event in frame['events']:
                    if event['eventType'] in itemEvents and event['participantId'] == champParticId:
                        champion["eventlist"].append({"eventType":event["eventType"], "itemId":event["itemId"],"timestamp":event["timestamp"]})
                        #eventNum+=1
                        #print str(eventNum) + "  " +str(champion["eventlist"][eventNum]["itemId"])
                    elif event['eventType'] == "ITEM_UNDO" and event['participantId'] == champParticId:
                        champion["eventlist"].append({"eventType":event["eventType"], "itemId":event["itemBefore"],"timestamp":event["timestamp"]})
                        #eventNum+=1
                        #print str(eventNum) + "  " +str(champion["eventlist"][eventNum]["itemId"])
        #print eventNum
        parsedId["champions"].append(champion)
total = len(parsedIds)
outputFilePath = 'static/json-data/processedmatches_' + str(startIndex) + '_' + str(endIndex) + '.json'
with open(outputFilePath, 'w') as outfile:
    json.dump(parsedIds, outfile, indent = 4)

print "success"
print str(total) + " unique matchids processed"

"""
print filedata['match_count']
#print "Calls: " + str(j)
print "done"""

            