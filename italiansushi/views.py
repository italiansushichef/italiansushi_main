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
            json = jsonfile.read()
            filetype = jsonfile.content_type

            ## insert function: validate_json(jsonfile)
            ## jsonfile.name 
            ## jsonfile.content_type -- check if it is "application/json"
            ## jsonfile.size -- 
            ## jsonfile.read() -- content
            ## if it is not content_type json, return None
            ## if it is not appropriate size, return None
            ## if the content does not match a itemset, return None
            ## else return jsonfile

            # if filetype == "application/json":
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
            print new_itemset.name
            print new_itemset.owner
            print new_itemset.json
            print "User saved count " +  str(savedcount)
            return HttpResponseRedirect('/?upload=success')
            # else:
            #     return HttpResponseRedirect('/?upload=notjson')
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
    parsed = jsonlib.loads(itemset.json)
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

# logout view
@login_required
def site_logout(request):
    logout(request)
    return HttpResponseRedirect('/?logout=success')
