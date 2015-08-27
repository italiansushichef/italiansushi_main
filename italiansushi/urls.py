from django.conf.urls import patterns, url
from italiansushi import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^createuser/$', views.createuser, name='createuser'),
        url(r'^login/$', views.site_login, name='login'),
        url(r'^logout/$', views.site_logout, name='logout'),
        url(r'^upload/$', views.receive_upload, name='upload'),
        url(r'^view-items/$', views.get_items, name='get_items'),
        url(r'^delete-itemset/$', views.delete_itemset, name='delete_itemset'),
        url(r'^error/$', views.error_page, name='error'),
        url(r'^ac-champ/$', views.autocomplete_champ, name='autocomplete_champ'),
        url(r'^matchup_generate_item/$', views.matchup_generate_item, name='matchup_generate_item'),
        url(r'^.*\.json$', views.view_itemset, name='view_itemset'),
        )