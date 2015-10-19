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

# Create your views here.


def testpage(request):
    template = loader.get_template('smartgrid/testpage.html')
    return HttpResponse(template.render())


def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c)


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/accounts/loggedin')
    else:
        return HttpResponseRedirect('/accounts/invalid')


def loggedin(request):
    return render_to_response('loggedin.html',
                              {'full_name': request.user.username})


def invalid_login(request):
    return render_to_response('invalid_login.html')


def logout(request):
    auth.logout(request)
    return render_to_response('logout.html')


















