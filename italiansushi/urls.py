from django.conf.urls import patterns, url
from italiansushi import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^createuser/$', views.createuser, name='createuser'),
        url(r'^login/$', views.site_login, name='login'),
        url(r'^logout/$', views.site_logout, name='logout'),
        url(r'^upload/$', views.receive_upload, name='upload'),
        url(r'^view-items/', views.get_items, name='get_items'),
        url(r'^.*\.json$', views.view_itemset, name='view_itemset'),
        )