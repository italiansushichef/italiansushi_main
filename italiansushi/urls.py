from django.conf.urls import patterns, url
from italiansushi import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^createuser/$', views.createuser, name='createuser'),
        url(r'^login/$', views.site_login, name='login'),
        url(r'^logout/$', views.site_logout, name='logout'),
        url(r'^upload/$', views.receive_upload, name='upload'),
        url(r'^view-items/$', views.get_items, name='get_items'),
        url(r'^load-item-info/$', views.load_item_info, name='load_item_info'),
        url(r'^load-champ-info/$', views.load_champ_info, name='load_champ_info'),
        url(r'^delete-itemset/$', views.delete_itemset, name='delete_itemset'),
        url(r'^error/$', views.error_page, name='error'),
        url(r'^ac-champ/$', views.autocomplete_champ, name='autocomplete_champ'),
        url(r'^matchup_generate_item/$', views.matchup_generate_item, name='matchup_generate_item'),
        url(r'^matchup-save-file/$', views.matchup_save_file, name='matchup_save_file'),
        url(r'^custom-save-file/$', views.custom_save_file, name='custom_save_file'),
        url(r'^createuser-and-save/$', views.createuser_save, name='createuser'),
        url(r'^login-and-save/$', views.site_login_save, name='login'),
        url(r'^.*\.json$', views.view_itemset, name='view_itemset'),
        url(r'^about/$', views.about_page, name = 'about'),
        url(r'^faq/$', views.faq_page, name = 'faq')
        )