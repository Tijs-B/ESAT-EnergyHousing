from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.template import RequestContext, loader

from .models import *

# Create your views here.

def testpage(request):
    template = loader.get_template('smartgrid/testpage.html')
    return HttpResponse(template.render())