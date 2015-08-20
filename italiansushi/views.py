from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from italiansushi.forms import CreateUserForm, LoginForm
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as django_login
from django.contrib.auth.models import User
from italiansushi.models import LoginProfile, ItemSet
from django.contrib.auth.decorators import login_required

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
            # repassword = data['repassword']
            username = data['username']
            email = data['email']
            # if there is already a user with that acct 
            user_exists = User.objects.filter(username=username)
            if user_exists:
                user = authenticate(username=username, password=password)
                if user:
                    django_login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    print "Error, a user with that username already exists"
            else:
                user = User(username=username, password=password, email=email)
                user.set_password(password)
                user.save()
                profile = LoginProfile(user=user)
                profile.save()
                user = authenticate(username=username, password=password, email=email)
                django_login(request, user)
                return HttpResponseRedirect('/')
        else:
            print 'invalid profile'
    return HttpResponseRedirect('/')

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            password = data['password']
            usernameoremail = data['usernameoremail']
            user = authenticate(username=usernameoremail, password=password)
            django_login(request, user)
            return HttpResponseRedirect('/')
        else:
            print 'invalid'
    return HttpResponseRedirect('/')

@login_required
def site_logout(request):
    logout(request)
    print 'hm?'
    return HttpResponseRedirect('/')