from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.testpage, name='prehomepage'),
    url(r'^$', views.login, name='login')

]