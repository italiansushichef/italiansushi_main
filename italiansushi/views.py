from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from italiansushi.forms import *
from italiansushi.models import *
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as django_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core import serializers
import re, random
import json as jsonlib
import json
from operator import itemgetter

################################### Helper functions #############################
# helper func, returns champid if champname works, 0 if champname is empty, None otherwise
def getChampId(champname):
    BLANK_ID = 0
    if champname == '': return BLANK_ID
    with open('static/json-data/champls.json', 'r') as champfile:
        champdata = jsonlib.load(champfile)
    for champ in champdata["data"].itervalues():
        if champname.lower() == champ["name"].lower():
            return champ["id"]
    return None

# Helper function to check if lane is valid 
def checkValidLane(lane):
    valid_lanes = ['', 'M', 'T', 'J', 'B']
    return lane in valid_lanes

# Helper function to check if user can save new itemsets
def under_maxuploads(user):
    MAX_UPLOADS = 10
    savedcount = len(ItemSet.objects.filter(owner=user))
    return savedcount < MAX_UPLOADS

# Helper function to convert from unicode
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

# assumes a .json extension!
# Helper function to generate a valid name for filename to save, by checking user's itemsets
def get_validname(user,filename):
    # the -5 removes the .json extension. the 0:28 takes up to 28 chars of remaining for the name
    name28 = filename[:-5][0:28] 
    name32 = name28

    if name32 == '':
        name32 = 'noname'

    # make sure the file name is not taken -- generate a new filename if not taken 
    if ItemSet.objects.filter(owner=user, name=name32):
        startindex = 1
        foundname = False
        while not foundname:
            name32 = name28 + '(' + str(startindex) + ')' 
            if ItemSet.objects.filter(owner=user, name=name32):
                startindex += 1
            else:
                foundname = True
    return name32

def returnGamePart(ms):
    # in seconds
    startingitemscutoff = 2*60
    earlygameuppercutoff = 20*60
    midgameuppercutoff = 35*60
    sec = ms/1000
    if sec < startingitemscutoff:
        return "start"
    if sec < earlygameuppercutoff:
        return "early"
    if sec < midgameuppercutoff:
        return "mid"
    else:
        return "late"

def getItemBlockFromItemBlock(possible_block, title):
    sortedls = sorted(possible_block, key=itemgetter("weight"), reverse=True)
    block = {'type':title, 'items':[]}
    for itemid in sortedls[0]['items']:
        found = False
        for i in block['items']:
            if i['id'] == str(itemid):
                i['count'] += 1
                found = True
                break
        if not found and itemid:
            block['items'].append({'id': str(itemid), 'count': 1})
    return block


def getItemBlockFromItem(possible_items, title, n):
    sortedls = sorted(possible_items, key=itemgetter("weight"), reverse=True)
    block = {'type':title, 'items':[]}
    for i in range(0, min(n + 1, len(possible_items))):
        itemid = possible_items[i]['id']
        found = False
        for existingi in block['items']:
            if existingi['id'] == str(itemid):
                existingi['id'] += 1
                found = True
                break
        if not found and itemid:
            block['items'].append({'id': str(itemid), 'count': 1})
    return block


# Helper func, uses a weighted algorithm to generate an itemset based on data that
# matches the input criteria
def generateItemSetForMatchup(champ1_id, champ2_id, lane):
    newjson = {}
    with open('static/json-data/champls.json', 'r') as champfile:
        champdata = jsonlib.load(champfile)
    champ1 = "ANY"
    champ2 = "ANY"
    for champ in champdata["data"].itervalues():
        if champ1_id == champ["id"]:
            champ1 = champ["key"]
        if champ2_id == champ["id"]:
            champ2 = champ["key"]
    raw_lane = "ANYLANE"
    if lane == 'M': 
        raw_lane = "MIDDLE"
    elif lane == 'B': 
        raw_lane = "BOTTOM"
    elif lane == 'T': 
        raw_lane = "TOP"
    elif lane == 'J': 
        raw_lane = "JUNGLE"
    title = champ1 + "_vs_" + champ2 + "_in_" + raw_lane
    name28 = title[0:28] 
    name32 = name28
    if ItemSet.objects.filter(owner=None, name=name28):
        startindex = 1
        foundname = False
        while not foundname:
            name32 = name28 + '(' + str(startindex) + ')' 
            if ItemSet.objects.filter(owner=None, name=name32):
                startindex += 1
            else:
                foundname = True
    title = name32
    newjson['title'] = title
    newjson['type'] = 'global'
    newjson['map'] = 'any'
    newjson['mode'] = 'any'
    newjson['blocks'] = []
    possible_startingitemsblock = []
    possible_earlygame = []
    possible_midgame = []
    possible_lategame = []
    possible_fullbuildblock = []

    matchfiles = [
                    'processedmatches_0_1000.json',
                    'processedmatches_1000_2000.json',
                    'processedmatches_2000_2500.json',
                    'processedmatches_2500_3000.json',
                    'processedmatches_3000_3500.json',
                    'processedmatches_3500_4000.json',
                    'processedmatches_4000_4500.json',
                    'processedmatches_4500_5000.json',
                    'processedmatches_5000_5500.json',
                    'processedmatches_5500_6000.json',
                 ]

    searched_matches = 0
    champion_matches = 0
    search_match_limit = 4000
    champion_match_limit = 150

    fullbuildcheckcutoff = 50*60

    normalWeight = 5
    laneMatchWeight = 15
    champ2Weight = 10
    victoryWeight = 5

    while searched_matches < search_match_limit and champion_matches < champion_match_limit:
        fileToSearch = random.choice(matchfiles)
        matchfiles.remove(fileToSearch)
        with open('static/json-data/' + fileToSearch, 'r') as matchfile:
            matchdata = jsonlib.load(matchfile)
        for match in matchdata:
            searched_matches += 1
            if searched_matches >= search_match_limit or champion_matches >= champion_match_limit:
                break
            duration = match['duration'] # in seconds
            weight = normalWeight
            matchChamp = None

            for champ in match['champions']:
                if champ['id'] == champ1_id:
                    if (raw_lane == "ANYLANE") or (champ['position'] == raw_lane):
                        weight += laneMatchWeight
                    if champ['statistics']['winner']:
                        weight += victoryWeight
                    matchChamp = champ
                    break
            if matchChamp:
                champion_matches += 1
                for otherchamp in match['champions']:
                    if otherchamp["id"] == champ2_id: #found second champ
                        if (otherchamp["statistics"]['winner'] != matchChamp['statistics']['winner']): #not on same team
                            if (raw_lane == "ANYLANE") or (raw_lane == otherchamp["position"]): # in same lane
                                weight += laneMatchWeight
                                break
                if duration > fullbuildcheckcutoff:
                    fullbuildblock = []
                    fullbuildblock.append(matchChamp["statistics"]["item0"])
                    fullbuildblock.append(matchChamp["statistics"]["item1"])
                    fullbuildblock.append(matchChamp["statistics"]["item2"])
                    fullbuildblock.append(matchChamp["statistics"]["item3"])
                    fullbuildblock.append(matchChamp["statistics"]["item4"])
                    fullbuildblock.append(matchChamp["statistics"]["item5"])
                    fullbuildblock.append(matchChamp["statistics"]["item6"])
                    fullbuildblock.sort()
                    found = False
                    for poss in possible_fullbuildblock:
                        if poss['items'] == fullbuildblock:
                            poss['weight'] += weight
                            found = True
                    if not found:
                        possible_fullbuildblock.append({'items': fullbuildblock, 'weight': weight})

                startingitemsblock = []
                destroyWeight = weight - 3
                for event in matchChamp["eventlist"]:
                    gamepart = returnGamePart(event["timestamp"])
                    if (gamepart == "start") and (event["eventType"] == "ITEM_PURCHASED"):
                        startingitemsblock.append(event["itemId"])

                    elif (gamepart == "early"):
                        if event["eventType"] == "ITEM_PURCHASED":
                            found = False
                            for item in possible_earlygame:
                                if item["id"] == event["itemId"]:
                                    found = True
                                    item["weight"] += weight
                            if not found:
                                possible_earlygame.append({"id": event["itemId"], "weight": weight})
                        elif event["eventType"] == "ITEM_DESTROYED":
                            found = False
                            for item in possible_earlygame:
                                if item["id"] == event["itemId"]:
                                    found = True
                                    item["weight"] -= destroyWeight

                    elif (gamepart == "mid"):
                        if event["eventType"] == "ITEM_PURCHASED":
                            found = False
                            for item in possible_midgame:
                                if item["id"] == event["itemId"]:
                                    found = True
                                    item["weight"] += weight
                            if not found:
                                possible_midgame.append({"id": event["itemId"], "weight": weight})
                        elif event["eventType"] == "ITEM_DESTROYED":
                            found = False
                            for item in possible_midgame:
                                if item["id"] == event["itemId"]:
                                    found = True
                                    item["weight"] -= destroyWeight

                    elif (gamepart == "late"):
                        if event["eventType"] == "ITEM_PURCHASED":
                            found = False
                            for item in possible_lategame: 
                                if item["id"] == event["itemId"]:
                                    found = True
                                    item["weight"] += weight
                            if not found:
                                possible_lategame.append({"id": event["itemId"], "weight": weight})
                        elif event["eventType"] == "ITEM_DESTROYED":
                            found = False
                            for item in possible_lategame:
                                if item["id"] == event["itemId"]:
                                    found = True
                                    item["weight"] -= destroyWeight
                startingitemsblock.sort()
                found = False
                for poss in possible_startingitemsblock:
                    if poss['items'] == startingitemsblock:
                        poss['weight'] += weight
                        found = True
                if not found:
                    possible_startingitemsblock.append({'items': startingitemsblock, 'weight': weight})

    if possible_startingitemsblock:
        newjson['blocks'].append(getItemBlockFromItemBlock(possible_startingitemsblock, 'Starting Items'))
    if possible_earlygame:
        newjson['blocks'].append(getItemBlockFromItem(possible_earlygame, "Early Game", 5))
    if possible_midgame:
        newjson['blocks'].append(getItemBlockFromItem(possible_midgame, "Mid Game", 5))
    if possible_lategame:
        newjson['blocks'].append(getItemBlockFromItem(possible_lategame, "Late Game", 5))
    if possible_fullbuildblock:
        newjson['blocks'].append(getItemBlockFromItemBlock(possible_fullbuildblock, 'Full Build'))

    print "Searched " + str(searched_matches)
    print "Where Champ Appeared " + str(champion_matches) 
    newitemset = ItemSet(json=newjson, owner=None, name=title, 
                        champ_for=champ1_id, champ_against=champ2_id, lane=lane)
    newitemset.save()
    return newitemset

# helper function to make of copy of itemToCopy and saves it to user
def save_itemset(itemToCopy, user):
    # Make a copy and save it to user
    filenameToSave = itemToCopy.name
    filenameToSave = get_validname(user, filenameToSave + '.json')
    itemToCopy.pk = None
    itemToCopy.owner = user
    itemToCopy.name = filenameToSave
    if itemToCopy.users_upvotes_count:
        itemToCopy.users_upvotes_count = 0
    itemToCopy.save()
    return filenameToSave

# helper function: takes in contents (a stringified json) and validates its format
def validate_jsoncontents(contents):
    # see https://developer.riotgames.com/docs/item-sets for more
    valid_details = {
        "type": ["custom", "global"],
        "map": ["any", "SR", "HA", "TT", "CS"],
        "mode": ["any", "CLASSIC", "ARAM", "ODIN"],
        # also contains a blocks dict list
            # which contains a string "type"
            # and contains an items dict list 
                # which includes item id as a string  # TODO validate string ID
    }

    with open('static/json-data/items_full.json') as data_file:    
        valid_items = jsonlib.load(data_file)

    try:
        parsed = jsonlib.loads(contents)
    except ValueError:
        print "No JSON object could be decoded"
        return None
    except:
        print "Other decoding error"
        return None
    else:
        if "type" not in parsed or parsed["type"] not in valid_details["type"]:
            print "Bad type field"
            return None
        if "map" not in parsed or parsed["map"] not in valid_details["map"]:
            print "Bad map field"
            return None
        if "mode" not in parsed or parsed["mode"] not in valid_details["mode"]:
            print "Bad mode field"
            return None
        if "blocks" not in parsed:
            print "Missing blocks field"
            return None
        for block in parsed["blocks"]:
            if "type" not in block or not isinstance(block["type"], basestring):
                print "Bad type in block field"
                return None
            if "items" not in block:
                print "Missing items in block field"
                return None
            if "id" in block:
                del block["id"]
            for item in block["items"]:
                if "id" not in item: # also validate item id
                    print "no item id read"
                    return None
                if item["id"] not in valid_items['data']:
                    print "invalid item id"
                    return None
        return parsed

# helper method to validate the input file as a jsonfile itemset
# return None if not json, the inputfile otherwise
def validate_json(inputfile):
    name = inputfile.name
    content_type = inputfile.content_type
    size = inputfile.size

    # -5: gives the .json extension assuming it is there
    if len(name) < 5 or name[-5:] != '.json':
        print "Not a json extension"
        return None
    if size > 6000: 
        print "Input file size is too big"
        return None
    contents = inputfile.read()
    return validate_jsoncontents(contents)

# helper function: validates contents of itemset_json, then gets champ1 and champ2 id
# checks lane, and saves the itemset to user then if all checks passed
def checkAndSaveCustomFile(itemset_json, champ1, champ2, lane, user):
    jsonToSave = validate_jsoncontents(itemset_json)
    if not jsonToSave:
        return {'success':False}
    champ1_id = getChampId(champ1)
    champ2_id = getChampId(champ2)
    valid_lane = checkValidLane(lane)
    if (not champ1_id and champ1 != "") or (not champ2_id and champ2 != "") or not valid_lane:
        return {'success':False}
    jsonToSave = byteify(jsonToSave)
    filename = jsonToSave['title']
    name32 = get_validname(user, filename + '.json')
    new_itemset = ItemSet(json=jsonToSave, owner=user, name=name32, 
                        champ_for=champ1_id, champ_against=champ2_id, lane=lane)
    new_itemset.save()
    return {'success':True, 'filename': name32}

################################### End Helper functions #############################


################################### Views ##########################################
def faq_page(request):
    context_dict = {'logged_in': request.user.is_authenticated()}
    return render(request, 'italiansushi/faq.html', context_dict)

def about_page(request):
    with open('static/json-data/updatetime.json', 'r') as readfile:
        data = jsonlib.load(readfile)

    context_dict = {
        'logged_in': request.user.is_authenticated(),
        'summoner_data_update': data["Updates"]["Update Summoner Data"],
        'item_data_update': data["Updates"]["Update Item Data"],
        'match_data_update': data["Updates"]["Update Match Data"],
        'champ_data_update': data["Updates"]["Update Champ Data"],
    }
    return render(request, 'italiansushi/about.html', context_dict)

# errorpage
def error_page(request):
    context_dict = {'logged_in': request.user.is_authenticated()}
    return render(request, 'italiansushi/error.html', context_dict)

# homepage
def index(request):
    context_dict = {'logged_in': request.user.is_authenticated()}
    return render(request, 'italiansushi/index.html', context_dict)

# receiving view for creating a new user acct
# redirects to main page upon success, error page if failure
def createuser(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            password = data['password']
            username = data['username']
            email = data['email']
            ## validate username is at most 32 characters, at least 3 characters
            if len(username) > 32 or len(username) < 3 or username=="tmp":
                return HttpResponseRedirect('/?createuser=badusername')
            ## validate password is at least 8 characters
            if len(password) < 8 or len(password) > 32:
                return HttpResponseRedirect('/?createuser=badpassword')

            # if there is already a user with that acct -- matching username or email. 
            # note: the username check is actually redundant 
            #       because the form.is_valid will have already checked it
            user_exists = User.objects.filter(username=username) | User.objects.filter(email=email)
            if user_exists:
                return HttpResponseRedirect('/?createuser=usernameoremailtaken')
            else:
                # Create user
                user = User(username=username, password=password, email=email)
                user.set_password(password)
                user.save()
                user = authenticate(username=username, password=password, email=email)
                django_login(request, user)
                return HttpResponseRedirect('/?createuser=success')
        else: # note, this checks if username is taken, also doesn't check if email is valid already
            print 'invalid createuser form'
            print form.errors 
            user_exists = User.objects.filter(username=request.POST['username'])
            if user_exists:
                return HttpResponseRedirect('/?createuser=usernameoremailtaken')
            # validate email is probably an email address -- not thorough 
            if not re.match(r'[^@]+@[^@]+\.[^@]+', request.POST['email']):
                return HttpResponseRedirect('/?createuser=bademail')
            ## some other type of error
            return HttpResponseRedirect('/error/?createuser=formfailure')
    return HttpResponseRedirect('/')

# receiving view for creating a new user acct, and then saving the file
# redirects to main page upon success, error page if failure
def createuser_save(request):
    if request.method == "POST":
        form = CreateUserSaveForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            password = data['password']
            username = data['username']
            email = data['email']
            ## validate username is at most 32 characters, at least 3 characters
            if len(username) > 32 or len(username) < 3 or username=="tmp":
                return HttpResponseRedirect('/?createuser=badusername&save=failure')
            ## validate password is at least 8 characters
            if len(password) < 8 or len(password) > 32:
                return HttpResponseRedirect('/?createuser=badpassword&save=failure')

            # if there is already a user with that acct -- matching username or email. 
            # note: the username check is actually redundant 
            #       because the form.is_valid will have already checked it
            user_exists = User.objects.filter(username=username) | User.objects.filter(email=email)
            if user_exists:
                return HttpResponseRedirect('/?createuser=usernameoremailtaken&save=failure')
            else:
                # Create user
                user = User(username=username, password=password, email=email)
                user.set_password(password)
                user.save()
                user = authenticate(username=username, password=password, email=email)
                django_login(request, user)
                idToSave = data['idToSave']
                # Save ItemSet to the User 
                if not under_maxuploads(user):
                    return HttpResponseRedirect('/?createuser=success&save=limitreached')

                if idToSave != 0:
                    itemToCopy = ItemSet.objects.filter(id=idToSave,owner=None)
                    # validate id exists
                    if not itemToCopy:
                        return HttpResponseRedirect('/?createuser=success&save=badItemSet')
                    else:
                        itemToCopy = itemToCopy[0]
                    # Make a copy
                    save_itemset(itemToCopy, user)
                    return HttpResponseRedirect('/?createuser=success&save=success')
                else:
                    itemset_json = request.POST['itemset_json'] 
                    champ1 = request.POST['champ1']
                    champ2 = request.POST['champ2']
                    lane = request.POST['lane']
                    result = checkAndSaveCustomFile(itemset_json, champ1, champ2, lane, user)
                    return JsonResponse(result) 
        else: # note, this checks if username is taken, also may check if email is valid already
            print 'invalid createuser form'
            print form.errors 
            user_exists = User.objects.filter(username=request.POST['username'])
            if user_exists:
                return HttpResponseRedirect('/?createuser=usernameoremailtaken&save=failure')
            # validate email is probably an email address -- not thorough 
            if not re.match(r'[^@]+@[^@]+\.[^@]+', request.POST['email']):
                return HttpResponseRedirect('/?createuser=bademail&save=failure')
            ## some other type of error
            return HttpResponseRedirect('/error/?createuser=formfailure&save=failure')
    return HttpResponseRedirect('/')

# receiving view for logging into the website
# redirects to index page upon success, error page if failure
def site_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            password = data['password']
            usernameoremail = data['usernameoremail']
            found_user = User.objects.filter(username=usernameoremail) | User.objects.filter(email=usernameoremail)
            # from list of possible users, try to authenticate
            if found_user:
                for possible_user in found_user:
                    user = authenticate(username=possible_user, password=password)
                    if user is not None:
                        django_login(request, user)
                        return HttpResponseRedirect('/?login=success')
            return HttpResponseRedirect('/?login=nouser')
        else:
            print 'invalid login form'
            print form.errors
            return HttpResponseRedirect('/error/?login=formfailure')
    return HttpResponseRedirect('/')

# receiving view for logging into the website
# redirects to index page upon success, error page if failure
def site_login_save(request):
    if request.method == "POST":
        
        form = LoginSaveForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            password = data['password']
            usernameoremail = data['usernameoremail']
            found_user = User.objects.filter(username=usernameoremail) | User.objects.filter(email=usernameoremail)
            # from list of possible users, try to authenticate
            if found_user:
                for possible_user in found_user:
                    user = authenticate(username=possible_user, password=password)
                    if user is not None:
                        django_login(request, user)
                        idToSave = data['idToSave']
                        # Save ItemSet to the User 

                        if not under_maxuploads(user):
                            return HttpResponseRedirect('/?login=success&save=limitreached')
                        if idToSave != 0:
                            itemToCopy = ItemSet.objects.filter(id=idToSave,owner=None)
                            # validate id exists
                            if not itemToCopy:
                                return HttpResponseRedirect('/?login=success&save=badItemSet')
                            else:
                                itemToCopy = itemToCopy[0]

                            # Make a copy
                            save_itemset(itemToCopy, request.user)
                            return HttpResponseRedirect('/?login=success&save=success')
                        else:
                            itemset_json = request.POST['itemset_json'] 
                            champ1 = request.POST['champ1']
                            champ2 = request.POST['champ2']
                            lane = request.POST['lane']
                            result = checkAndSaveCustomFile(itemset_json, champ1, champ2, lane, user)
                            return JsonResponse(result)
            return HttpResponseRedirect('/?login=nouser&save=failure')
        else:
            print 'invalid login form'
            print form.errors
            return HttpResponseRedirect('/error/?login=formfailure&save=failure')
    return HttpResponseRedirect('/')

# receiving view for uploading a file
# redirects to main page if success, error page if failure
@login_required
def receive_upload(request):
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            champ1 = request.POST['champ1']
            champ2 = request.POST['champ2']
            lane = request.POST['lane']
            champ1_id = getChampId(champ1)
            champ2_id = getChampId(champ2)
            valid_lane = checkValidLane(lane)
            if (not champ1_id and champ1 != "") or (not champ2_id and champ2 != "") or not valid_lane:
                return HttpResponseRedirect('/?upload=formfailure')
            jsonfile = request.FILES['json']
            contents = validate_json(jsonfile)
            if not contents:
                return HttpResponseRedirect('/?upload=badjson')

            # Save contents of file
            json = contents
            savedcount = len(ItemSet.objects.filter(owner=request.user))
            if not under_maxuploads(request.user):
                return HttpResponseRedirect('/?upload=limitreached')

            name32 = get_validname(request.user,jsonfile.name)

            new_itemset = ItemSet(json=json, owner=request.user, name=name32, champ_for=champ1_id, 
                                    champ_against=champ2_id, lane=lane)
            new_itemset.save()
            return HttpResponseRedirect('/?upload=success')
        else: 
            print "invalid receive upload form"
            print form.errors
            return HttpResponseRedirect('/error/?upload=formfailure')
    return HttpResponseRedirect('/')

# backend for viewing an itemset -- displays the itemset formatted 
def view_itemset(request):
    url = request.path
    user = url.split('/')[1]
    filename = url.split('/')[-1][:-5]
    itemset = None
    if user == 'tmp': # special case, tmp is a reserved name
        itemset = ItemSet.objects.filter(owner=None, name=filename)
    else:
        userobject = User.objects.filter(username=user)
        if userobject:
            itemset = ItemSet.objects.filter(owner=userobject[0], name=filename)
    if itemset:
        json = itemset[0].json
        output = jsonlib.dumps(json, indent=4)
        return HttpResponse(output, content_type="application/json")
    return HttpResponse('The requested URL ' + str(request.path) + ' was not found on this server.')
    

# Helper: non-view method to get a list of up to n items from the input json ## DEPRECATED 
# def preview_items(itemset, max_items):
#     ls = []
#     try:
#         parsed = jsonlib.loads(itemset.json)
#     except:
#         return None
#     else:
#         blocks = parsed['blocks']
#         for b in blocks:
#             items = b['items']
#             for i in items:
#                 if len(ls) >= max_items:
#                     return ls
#                 elif 'id' in i:
#                     ls.append(i['id'])
#         return ls

# ajax backend for displaying items list for the item manager
@login_required
def get_items(request):
    response_data = {}
    item_ls = ItemSet.objects.filter(owner=request.user)
    response_data["number"] = len(item_ls)
    for i in range(0, len(item_ls)):
        response_data[i] = {}
        response_data[i]["filename"] = str(item_ls[i].name)
        response_data[i]["jsonfile"] = item_ls[i].json
    return JsonResponse(response_data)

# ajax backed for deleting an item set from the item manager
@login_required
def delete_itemset(request):
    if request.method == "POST":
        form = DeleteItemSetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            name = data['name']
            user = data['user']
            itemToDelete = ItemSet.objects.filter(owner=request.user, name=name)
            if request.user.username == user and itemToDelete:
                itemToDelete[0].delete()
                return HttpResponse("success")
        else:
            print "invalid delete itemset form"
            print form.errors
            return HttpResponse('form error')
    return HttpResponse("/")

# ajax backend for autocompleting a champion name ## DEPRECATED 
# def autocomplete_champ(request):
#     data = None
#     response = {"ac-match":[],}
#     query = ""
#     if request.method == "GET":
#         query = request.GET['query']
#     with open('static/json-data/champls.json', 'r') as champfile:
#         data = jsonlib.load(champfile)
#     if query == "" or query == None:
#         return JsonResponse(response)
#     q = re.compile(query, re.IGNORECASE)
#     # match is from first character, search is from entire string
#     for champ in data["data"].itervalues():
#         rematch = q.match(champ["name"])
#         if rematch != None and rematch.group() != "":
#             response["ac-match"].append(champ["name"])
#     response["ac-match"].sort()
#     return JsonResponse(response)

# Ajax backend for returning the champion list, for autocomplete
def load_champ_info(request):
    if request.method == "GET":
        data = None
        with open('static/json-data/champls.json', 'r') as itemfile:
            data = jsonlib.load(itemfile)
        if data:
            return JsonResponse(data)
    return JsonResponse({})

# ajax backend for generating an itemset using matchup generater
def matchup_generate_item(request):
    if request.method == "POST":
        form = GenerateItemSetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            response = {'jsonfile':None}
            champdata = None
            with open('static/json-data/champls.json', 'r') as champfile:
                champdata = jsonlib.load(champfile)
            valid_lanes = ['', 'M', 'T', 'J', 'B']
            champ1 = str(data['champ1'])
            champ2 = str(data['champ2'])
            lane = str(data['lane'])

            # validate all data
            champ1_id = getChampId(champ1)
            champ2_id = getChampId(champ2)
            valid_lane = checkValidLane(lane)
            
            response['champ1_id'] = champ1_id
            response['champ2_id'] = champ2_id
            response['valid_lane'] = valid_lane
            if not champ1_id or (not champ2_id and champ2 != "") or not valid_lane:
                return JsonResponse(response)
            possibleitem = ItemSet.objects.filter(owner=None, champ_for=champ1_id, champ_against=champ2_id, lane=lane)
            if possibleitem and possibleitem.count() >= 5:
                randomindex = random.randint(0, possibleitem.count())
                item = possibleitem[randomindex]
            else:
                item = generateItemSetForMatchup(champ1_id, champ2_id, lane)
            response['jsonfile'] = item.json
            response['jsonfile_id'] = item.id
            response['jsonfile_name'] = item.name
            return JsonResponse(response)
        else:
            print form.errors
            return JsonResponse({'jsonfile':None})
    return HttpResponseRedirect('/')

# ajax backend for saving the matchup generated file, given the item set id
@login_required
def matchup_save_file(request):
    if request.method == "POST":
        form = SaveItemSetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            idToSave = data['idToSave']
            # Save ItemSet to the User 

            if not under_maxuploads(request.user):
                return JsonResponse({'max_uploads_reached':True})

            itemToCopy = ItemSet.objects.filter(id=idToSave,owner=None)
            # validate id exists
            if not itemToCopy:
                return JsonResponse({'success':False})
            else:
                itemToCopy = itemToCopy[0]

            # Make a copy
            title = save_itemset(itemToCopy, request.user)
            return JsonResponse({'success':True, 'savetitle': title})
        else:
            print form.errors
            return JsonResponse({'success':False})
    return HttpResponseRedirect('/')

# ajax backend for a file found in search, given the item set id
@login_required
def search_save_file(request):
    if request.method == "POST":
        idToSave = request.POST['idToSave']
        owner_username = request.POST['owner']
        # Save ItemSet to the User 
        if not under_maxuploads(request.user):
            return JsonResponse({'max_uploads_reached':True})
        if owner_username == 'tmp':
            owner = None
        else:
            owner = User.objects.filter(username=owner_username)
        itemToCopy = ItemSet.objects.filter(id=idToSave,owner=owner)
        # validate id exists
        if not itemToCopy:
            return JsonResponse({'success':False})
        else:
            itemToCopy = itemToCopy[0]

        # Make a copy
        title = save_itemset(itemToCopy, request.user)
        return JsonResponse({'success':True, 'savetitle': title})
    return HttpResponseRedirect('/')

# ajax backend for up/downvoting a file found in search, given the item set id and the upordown vote
@login_required
def search_upvote_file(request):
    if request.method == "POST":
        idToSave = request.POST['idToSave']
        owner_username = request.POST['owner']
        upordown = request.POST['upordown']
        if owner_username == 'tmp':
            owner = None
        else:
            owner = User.objects.filter(username=owner_username)
        itemToUpvote = ItemSet.objects.filter(id=idToSave,owner=owner)
        # validate id exists
        if not itemToUpvote:
            return JsonResponse({'success':False})
        else:
            itemToUpvote = itemToUpvote[0]
        if upordown == "up":
            itemToUpvote.users_upvotes.add(request.user)
            itemToUpvote.users_upvotes_count = itemToUpvote.users_upvotes.count()
            itemToUpvote.save()
            return JsonResponse({'success':True, 'upvotes': itemToUpvote.users_upvotes_count, 'upvotesuccess': True})
        elif upordown == "down":
            itemToUpvote.users_upvotes.remove(request.user)
            itemToUpvote.users_upvotes_count = itemToUpvote.users_upvotes.count()
            itemToUpvote.save()
            return JsonResponse({'success':True, 'upvotes': itemToUpvote.users_upvotes_count, 'downvotesuccess': True})
        else:
            return JsonResponse({'success':False})
        
    return HttpResponseRedirect('/')

# ajax backend for saving the file made in the custom file editor
@login_required
def custom_save_file(request):
    if request.method == "POST":
        if not under_maxuploads(request.user):
            return JsonResponse({'max_uploads_reached':True})

        contents = request.POST['itemset_json']

        # validate other fields
        champ1 = str(request.POST['champ1'])
        champ2 = str(request.POST['champ2'])
        lane = str(request.POST['lane'])

        champ1_id = getChampId(champ1)
        champ2_id = getChampId(champ2)
        valid_lane = checkValidLane(lane)
        response = checkAndSaveCustomFile(contents, champ1, champ2, lane, request.user)
        return JsonResponse(response)
    return HttpResponseRedirect('/')

# ajax backend for sending the itemset data to frontend
def load_item_info(request):
    if request.method == "GET":
        data = None
        with open('static/json-data/items_full.json', 'r') as itemfile:
            data = jsonlib.load(itemfile)
        if data:
            return JsonResponse(data)
    return JsonResponse({})

# ajax backend for searching item sets
def search_itemsets(request):
    PAGE_SIZE = 20
    response = {}
    if request.method == "GET":
        champ1 = str(request.GET['champ1'])
        champ2 = str(request.GET['champ2'])
        lane = str(request.GET['lane'])
        searchpage = int(request.GET['searchpage'])
        response['champ1_id'] = getChampId(champ1)
        response['champ2_id'] = getChampId(champ2)
        response['valid_lane'] = checkValidLane(lane)
        response['lane'] = lane
        if (not response['champ1_id'] and champ1 != "") or (not response['champ2_id'] and champ2 != "") or not response['valid_lane']:
            response['results'] = []
            return JsonResponse(response)
        else:
            possible_matches = ItemSet.objects.all().exclude(owner=None)
            # filter as appropriate
            if (response['champ1_id'] != 0): # not 0 (any)
                possible_matches = possible_matches.filter(champ_for=response['champ1_id'])
            if (response['champ2_id'] != 0): # not 0 (any)
                possible_matches = possible_matches.filter(champ_against=response['champ2_id'])
            if (response['lane'] != ''):      # not blank (any)
                possible_matches = possible_matches.filter(lane=response['lane'])
            possible_matches = possible_matches.order_by('-users_upvotes_count')
            
            startindex = searchpage * PAGE_SIZE
            endindex = (searchpage + 1) * PAGE_SIZE
            return_ls = possible_matches[startindex:endindex]
            if len(return_ls) == 0: 
                response["nextpage"] = -1
            else:
                response["nextpage"] = searchpage + 1
            response["count"] = len(return_ls)
            response["results"] = []
            for i in range(0, len(return_ls)):
                can_upvote = True
                # check if already upvoted
                if not request.user.is_authenticated() or return_ls[i].users_upvotes.filter(id=request.user.id):
                    can_upvote = False
                if return_ls[i].owner:
                    owner = return_ls[i].owner.username
                else:
                    owner = 'tmp'
                can_save = True
                if not request.user.is_authenticated() or (return_ls[i].owner and return_ls[i].owner == request.user):
                    can_save = False
                result = {
                    'json': return_ls[i].json, 'upvotes': return_ls[i].users_upvotes_count, 
                    'filename': return_ls[i].name, 'can_upvote': can_upvote, 'id': return_ls[i].id,
                    'owner': owner, 'can_save': can_save
                }
                response["results"].append(result)
            return JsonResponse(response)
    return JsonResponse({})

# logout view
@login_required
def site_logout(request):
    logout(request)
    return HttpResponseRedirect('/?logout=success')
