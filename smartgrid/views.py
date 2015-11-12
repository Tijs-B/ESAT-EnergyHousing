from django.shortcuts import get_object_or_404, render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.template import RequestContext, loader
from django.contrib import auth
# Security:
from django.core.context_processors import csrf

from .models import *

#GAMS
import sqlite3 as sq
import gams
import os

# Create your views here.

# Prehomepage


def testpage(request):
    # template = loader.get_template('smartgrid/prehomepage.html')
    print 'testpage'
    context = {}
    return render(request, 'smartgrid/prehomepage.html', context)


def resultaat(request):
    return render(request,'smartgrid/info/resultaat.html')


def info_apparaten(request):
    return render(request,'smartgrid/info/info_apparaten.html')


def vraagzijdesturing(request):
    return render(request,'smartgrid/info/vraagzijdesturing.html')


def projectverdeling(request):
    return render(request,'smartgrid/info/projectverdeling.html')

# Login


def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('smartgrid/login.html', c)


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    print user

    if user is not None:
        auth.login(request, user)
        template = loader.get_template('smartgrid/homepage.html')
        return HttpResponse(template.render())
    else:
        template = loader.get_template('smartgrid/invalid_login.html')
        return HttpResponse(template.render())


def invalid_login(request):
    return render_to_response('smartgrid/invalid_login.html')


def logout(request):
    auth.logout(request)
    template = loader.get_template('smartgrid/logout.html')
    return HttpResponse(template.render())

# Na login

def home(request):
    # template = loader.get_template('smartgrid/homepage.html')
    # print request.user.username
    return render(request, 'smartgrid/post_login/homepage.html',
                        {'full_name': request.user.username})


def rooms(request):
    rooms_list = Room.objects.all()
    return render(request, 'smartgrid/post_login/rooms.html', {'rooms_list': rooms_list})


def room_detail(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    return render(request, 'smartgrid/post_login/room_detail.html', {'room': room})

def trigger_gams(request):
    if request.POST:
        print 'trigger gams'
        x = Appliance()




