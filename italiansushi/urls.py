from django.conf.urls import patterns, url
from italiansushi import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        )