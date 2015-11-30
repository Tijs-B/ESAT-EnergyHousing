from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.prehomepage, name='prehomepage'),
    url(r'^resultaat/$', views.resultaat, name='resultaat'),
    url(r'^info_apparaten/$', views.info_apparaten, name='info_apparaten'),
    url(r'^vraagzijdesturing/$', views.vraagzijdesturing, name='vraagzijdesturing'),
    url(r'^projectverdeling/$', views.projectverdeling, name='projectverdeling'),
    # Login-urls
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^accounts/auth/$', views.auth_view, name='auth'),
    url(r'^accounts/logout/$', views.logout, name='logout'),
    url(r'^accounts/invalid/$', views.invalid_login, name='invalid_login'),
    # After login
    url(r'^home/$', views.home, name='home'),

    url(r'^rooms/$', views.rooms, name='rooms'),
    url(r'^room/(?P<room_id>[0-9]+)/$', views.room_detail, name='room_detail'),
    url(r'^room/heatloadinvariable/(?P<appliance_id>[0-9]+)/$', views.heatloadinvariable, name='heatloadinvariable'),
    url(r'^room/heatloadvariable/(?P<appliance_id>[0-9]+)/$', views.heatloadvariable, name='heatloadvariable'),
    #url(r'^room/fixed/(?P<appliance_id>[0-9]+)/$', views.fixed, name='fixed'),
    url(r'^room/shiftingloadcycle/(?P<appliance_id>[0-9]+)/$', views.shiftingloadcycle, name='shiftingloadcycle'),
    url(r'^room/(?P<room_id>[0-9]+)/add_appliance/$', views.add_appliance, name='add_appliance'),
    url(r'^room/(?P<room_id>[0-9]+)/add/$', views.add, name='add'),

    url(r'^demo_encryptie/$', views.demo_encryptie, name='demo_encryptie'),
    url(r'^scenario/$', views.scenario, name='scenario'),
    url(r'^scenario/change_scenario/(?P<neighborhood_id>[0-9]+)/$', views.change_scenario, name='change_scenario'),
    url(r'^scenario/settime/(?P<i>[0-9]+)/$', views.set_scenario_time, name='set_scenario_time'),
]
