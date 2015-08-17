from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# homepage
def index(request):
	return render(request, 'italiansushi/index.html')