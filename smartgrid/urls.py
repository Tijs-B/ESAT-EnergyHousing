from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.testpage, name='prehomepage'),
    # Login-urls
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^accounts/auth/$', views.auth_view, name='auth'),
    url(r'^accounts/logout/$', views.logout, name='logout'),
    url(r'^accounts/invalid/$', views.invalid_login, name='invalid_login'),
    # After login
    url(r'^home/$', views.home, name='home'),

    url(r'^rooms/$', views.rooms, name='rooms'),
    url(r'^room/(?P<room_id>[0-9]+)/$', views.room_detail, name='room_detail')
]