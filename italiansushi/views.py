from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from italiansushi.forms import CreateUserForm, LoginForm, FileForm
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as django_login
from django.contrib.auth.models import User
from italiansushi.models import LoginProfile, ItemSet
from django.contrib.auth.decorators import login_required
import re



# homepage
def index(request):
    if request.user.is_authenticated():
        logged_in = True
    else:
        logged_in = False
    context_dict = {'logged_in': logged_in}
    return render(request, 'italiansushi/index.html', context_dict)

def createuser(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            password = data['password']
            # repassword = data['repassword'] # TODO
            username = data['username']
            email = data['email']
            # if there is already a user with that acct -- matching username or email. 
            # note: the username check is actually redundant
            user_exists = User.objects.filter(username=username) | User.objects.filter(email=email)
            if user_exists:
                user = authenticate(username=username, password=password, email=email)
                if user is not None:
                    django_login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    print "Error, a user with that username or email already exists"
                    return HttpResponseRedirect('/#badlogin')
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
                return HttpResponseRedirect('/')
        else: # note: this will check if a user with that username already exists!!
            print 'invalid profile'
            print form.errors
            return HttpResponse('error creating user')
    return HttpResponseRedirect('/')

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
                        return HttpResponseRedirect('/#loginsuccess')
            return HttpResponse('error in login')
        else:
            print 'invalid data for login'
            return HttpResponse('error in login')
    return HttpResponseRedirect('/')

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
            # print data
            # print jsonfile
            # print json
            # print jsonfile.content_type
            # print jsonfile.size

            ## insert function: validate_json(jsonfile)
            ## jsonfile.name 
            ## jsonfile.content_type -- check if it is "application/json"
            ## jsonfile.size -- 
            ## jsonfile.read() -- content
            ## if it is not content_type json, return None
            ## if it is not appropriate size, return None
            ## if the content does not match a itemset, return None
            ## else return jsonfile

            if filetype == "application/json":
                user_loginprofile = LoginProfile.objects.filter(user=request.user)[0]
                
                if user_loginprofile.saved_count >= MAX_UPLOADS:
                    return HttpResponse('Received file, but cannot add more error because limit is 10')

                # the -5 removes the .json extension. the 0:28 takes up to 28 chars of remaining for the name
                name28 = jsonfile.name[:-5][0:28] 
                name32 = name28
                # make sure the file name is not taken 
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
                user_loginprofile.saved_count = len(ItemSet.objects.filter(owner=user_loginprofile))
                user_loginprofile.save()
                print "User saved count " +  str(user_loginprofile.saved_count)
                return HttpResponseRedirect('/#uploadsuccess')
            else:
                return HttpResponse('not a json...')
            
        else: 
            return HttpResponse('not a valid file...')
    return HttpResponse('not a valid file...')

@login_required
def site_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
