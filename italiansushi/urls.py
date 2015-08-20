from django.conf.urls import patterns, url
from italiansushi import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^createuser/$', views.createuser, name='createuser'),
        url(r'^login/$', views.login, name='login'),
        url(r'^logout/$', views.site_logout, name='logout'),
        # url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
        )