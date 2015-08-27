from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from italiansushi.forms import *
from italiansushi.models import *
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as django_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core import serializers
import re
import json as jsonlib

def about_page(request):
    if request.user.is_authenticated():
        logged_in = True
    else:
        logged_in = False
    context_dict = {'logged_in': logged_in}
    return render(request, 'italiansushi/about.html', context_dict)

# errorpage
def error_page(request):
    if request.user.is_authenticated():
        logged_in = True
    else:
        logged_in = False
    context_dict = {'logged_in': logged_in}
    return render(request, 'italiansushi/error.html', context_dict)

# homepage
def index(request):
    if request.user.is_authenticated():
        logged_in = True
    else:
        logged_in = False
    context_dict = {'logged_in': logged_in}
    return render(request, 'italiansushi/index.html', context_dict)

# receiving view for creating a new user acct
# redirects to main page upon success, error page if failure
def createuser(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            password = data['password']
            # repassword = data['repassword'] # TODO
            username = data['username']
            email = data['email']
            ## validate username is at most 32 characters, at least 3 characters
            if len(username) > 32 or len(username) < 3:
                return HttpResponseRedirect('/?createuser=badusername')
            ## validate password is at least 8 characters
            if len(password) < 8 or len(password) > 32:
                return HttpResponseRedirect('/?createuser=badpassword')

            # if there is already a user with that acct -- matching username or email. 
            # note: the username check is actually redundant 
            #       because the form.is_valid will have already checked it
            user_exists = User.objects.filter(username=username) | User.objects.filter(email=email)
            if user_exists:
                user = authenticate(username=username, password=password, email=email)
                # login user if information matches 
                if user is not None:
                    django_login(request, user)
                    return HttpResponseRedirect('/?login=success')
                # otherwise username or email is taken 
                else:
                    return HttpResponseRedirect('/?createuser=usernameoremailtaken')
            else:
                # Create user
                user = User(username=username, password=password, email=email)
                user.set_password(password)
                user.save()
                # Create profile
                profile = LoginProfile(user=user)
                profile.save()
                user = authenticate(username=username, password=password, email=email)
                django_login(request, user)
                return HttpResponseRedirect('/?createuser=success')
        else: # note, this checks if username is taken, also may check if email is valid already
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

# helper method to validate the input file as a jsonfile itemset minimally
# return None if not json, the inputfile otherwise
def validate_json(inputfile):
    name = inputfile.name
    content_type = inputfile.content_type
    size = inputfile.size
    # https://developer.riotgames.com/docs/item-sets
    valid_details = {
        "type": ["custom", "global"],
        "map": ["any", "SR", "HA", "TT", "CS"],
        "mode": ["any", "CLASSIC", "ARAM", "ODIN"],
        # also contains a blocks dict list
            # which contains a string "type"
            # and contains an items dict list 
                # which includes item id as a string  # TODO validate string ID
    }

    # this check isn't working on windows. TODO find out why
    # if inputfile.content_type != "application/json": return None

    # -5: gives the .json extension assuming it is there
    if len(name) < 5 or name[-5:] != '.json':
        print "Not a json extension"
        return None
    if size > 6000: 
        print "Input file size is too big"
        return None
    contents = inputfile.read()
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
            for item in block["items"]:
                if "id" not in item: # also validate item id
                    print "bad item id"
                    return None
        return contents

# receiving view for uploading a file
# redirects to main page if success, error page if failure
@login_required
def receive_upload(request):
    MAX_UPLOADS = 10
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            jsonfile = request.FILES['json']
            contents = validate_json(jsonfile)
            if not contents:
                return HttpResponseRedirect('/?upload=badjson')

            # Save contents of file
            json = contents
            user_loginprofile = LoginProfile.objects.filter(user=request.user)[0]
            savedcount = len(ItemSet.objects.filter(owner=user_loginprofile))
            if savedcount >= MAX_UPLOADS:
                return HttpResponseRedirect('/?upload=limitreached')

            # the -5 removes the .json extension. the 0:28 takes up to 28 chars of remaining for the name
            name28 = jsonfile.name[:-5][0:28] 
            name32 = name28

            # make sure the file name is not taken -- generate a new filename if not taken 
            if ItemSet.objects.filter(owner=user_loginprofile, name=name28):
                startindex = 1
                foundname = False
                while not foundname:
                    name32 = name28 + '(' + str(startindex) + ')' 
                    if ItemSet.objects.filter(owner=user_loginprofile, name=name32):
                        startindex += 1
                    else:
                        foundname = True

            new_itemset = ItemSet(json=json, owner=user_loginprofile, name=name32)
            new_itemset.save()
            # print "New json in database: (name, owner, json) "
            # print new_itemset.name
            # print new_itemset.owner
            # print new_itemset.json
            # print "User saved count " +  str(savedcount)
            return HttpResponseRedirect('/?upload=success')
        else: 
            print "invalid receive upload form"
            print form.errors
            return HttpResponseRedirect('/error/?upload=formfailure')
    return HttpResponseRedirect('/')

# for viewing an itemset
@login_required
def view_itemset(request):
    user_loginprofile = LoginProfile.objects.filter(user=request.user)[0]
    url = request.path
    user = url.split('/')[1]
    filename = url.split('/')[-1][:-5]
    if request.user.username == user:
        itemset = ItemSet.objects.filter(owner=user_loginprofile, name=filename)
        if itemset:
            json = itemset[0].json
            parsed = jsonlib.loads(json)
            return HttpResponse(json, content_type="application/json")
    return HttpResponse('The requested URL ' + str(request.path) + ' was not found on this server.')
    

# Helper non-view method to get a list of up to n items from the input json 
def preview_items(itemset, max_items):
    ls = []
    try:
        parsed = jsonlib.loads(itemset.json)
    except:
        return None
    else:
        blocks = parsed['blocks']
        for b in blocks:
            items = b['items']
            for i in items:
                if len(ls) >= max_items:
                    return ls
                elif 'id' in i:
                    ls.append(i['id'])
        return ls


# ajax backend for displaying items list
@login_required
def get_items(request):
    user_loginprofile = LoginProfile.objects.filter(user=request.user)[0]
    response_data = {}
    item_ls = ItemSet.objects.filter(owner=user_loginprofile)
    response_data["number"] = len(item_ls)
    for i in range(0, len(item_ls)):
        response_data[i] = {}
        response_data[i]["filename"] = str(item_ls[i].name)
        response_data[i]["item_ids"] = preview_items(item_ls[i], 15)
        # preview_ls = preview_items(item_ls[i], 15) # for debugging only
        # if not preview_ls:
        #     item_ls[i].delete()
        # else:
        #     response_data[i]["item_ids"] = preview_ls
    return JsonResponse(response_data)

# ajax backed for deleting an item set
@login_required
def delete_itemset(request):
    if request.method == "POST":
        user_loginprofile = LoginProfile.objects.filter(user=request.user)[0]
        form = DeleteItemSetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            name = data['name']
            user = data['user']
            itemToDelete = ItemSet.objects.filter(owner=user_loginprofile, name=name)
            if request.user.username == user and itemToDelete:
                itemToDelete[0].delete()
                return HttpResponse("deleted " + name + " successfully")
        else:
            print "invalid delete itemset form"
            print form.errors
            return HttpResponse('form error')
    return HttpResponse("/")

# ajax backend for autocompleting a champion name
def autocomplete_champ(request):
    data = None
    response = {"ac-match":[],}
    query = ""
    if request.method == "GET":
        query = request.GET['query']
    with open('static/json-data/champls.json', 'r') as champfile:
        data = jsonlib.load(champfile)
    if query == "":
        return response
    q = re.compile(query, re.IGNORECASE)
    # match is from first character, search is from entire string
    for champ in data["data"].itervalues():
        rematch = q.match(champ["name"])
        if rematch != None and rematch.group() != "":
            response["ac-match"].append(champ["name"])
    response["ac-match"].sort()
    return JsonResponse(response)

# logout view
@login_required
def site_logout(request):
    logout(request)
    return HttpResponseRedirect('/?logout=success')
