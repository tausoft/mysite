from django.urls import path, include
from django.views.generic import TemplateView, DeleteView
from . import views
from django.conf.urls import *
from register import views as v

urlpatterns = [
    url(r'^$', views.index, name ='index'),
    path("register/", v.register, name="register"),
    path('', include('django.contrib.auth.urls')),
    url(r'^o_nama/$', views.about, name ='about'),
    url(r'^dekodiranjeinput/$', views.dekodiranjeinput, name ='dekodiranjeinput'),
    url(r'^dekodiranjeinput_search/$', views.dekodiranjeinput_search, name ='dekodiranjeinput_search'),
    url(r'^dekodiranjetabela/$', views.dekodiranjetabela, name ='dekodiranjetabela'),
    url(r'^dekodiranjeobradjeni/$', views.dekodiranjeobradjeni, name ='dekodiranjeobradjeni'),
    url(r'^dekodiranjeadmin/$', views.dekodiranjeadmin, name ='dekodiranjeadmin'),
    url(r'^dekodiranjeadminvendorlist/$', views.dekodiranjeadminvendorlist, name ='dekodiranjeadminvendorlist'),
    url(r'^dekodiranjeadminnokialist/$', views.dekodiranjeadminnokialist, name ='dekodiranjeadminnokialist'),
    url(r'^dekodiranjepretraga/$', views.dekodiranjepretraga, name ='dekodiranjepretraga'),
    url(r'^confirm_new/$', views.confirm_new, name ='confirm_new'),
    url(r'^csvupload/$', views.csvupload, name ='csvupload'),
    url(r'^add_new/$', views.add_new, name ='add_new'),
    url(r'^add_new_confirm/$', views.add_new_confirm, name ='add_new_confirm'),
    url(r'^search_unc/$', views.search_unc, name ='search_unc'),
    url(r'^edit_new/(?P<item_id>\d+)/$', views.edit_new, name='edit_new'),
    url(r'^delete_new/(?P<item_id>\d+)/$', views.delete_new, name='delete_new'),
    url(r'^download_list/$', views.download_list, name ='download_list'),
    url(r'^nokia_list/$', views.nokia_list, name ='nokia_list'),
    url(r'^upload_csv/$', views.upload_csv, name ='upload_csv'),
    url(r'^reset_csv/$', views.reset_csv, name ='reset_csv'),
    url(r'^validate_csv/$', views.validate_csv, name ='validate_csv'),
    url(r'^ace_list/$', views.ace_list, name ='ace_list'),
    url(r'^ace_table/$', views.ace_table, name ='ace_table'),
    url(r'^test/$', views.test, name ='test'),
    url(r'^lista/$', views.lista, name ='lista'),
    url(r'^dashboard/$', views.dashboard, name ='dashboard'),
    url(r'^ajax/search_unc_ajax/$', views.search_unc_ajax, name='search_unc_ajax'),
    url(r'^isie/$', views.isie, name='isie'),
]