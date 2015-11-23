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
# import sqlite3 as sq
# import gams
# import os

# Create your views here.

# Prehomepage


def prehomepage(request):
    return render(request, 'smartgrid/prehomepage.html')


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
        template = loader.get_template('smartgrid/post_login/homepage.html')
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
    # scenario = Scenario.objects.all()[0]
    # current_neighborhood_name = scenario.neighbourhood_name
    # current_neighborhood = Neighborhood.objects.get(name=current_neighborhood_name)
    #
    # energy_price_data = []
    # for energy_price in current_neighborhood.energy_price_set:
    #     energy_price_data.append([(energy_price.time-1)/4, energy_price.price])
    #
    # return render(request, 'smartgrid/post_login/homepage.html',
    #                     {'full_name': request.user.username,
    #                      'energy_price_data': energy_price_data})
    return render(request, 'smartgrid/post_login/homepage.html', {'full_name': request.user.username})


def rooms(request):
    rooms_list = Room.objects.all()
    return render(request, 'smartgrid/post_login/rooms.html',
                  {'rooms_list': rooms_list})


def room_detail(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    return render(request, 'smartgrid/post_login/room_detail.html',
                  {'room': room})

## Appliances

def fixed(request, appliance_id):
    appliance = get_object_or_404(FixedDemand, pk=appliance_id)
    return render(request, 'smartgrid/post_login/appliances/Fixed.html',
                  {'appliance': appliance,
                   'consumption': appliance.consumption,
                   'currently_on':appliance.currently_on})


def shiftingloadcycle(request, appliance_id):
    appliance = get_object_or_404(ShiftingLoadCycle, pk=appliance_id)

    return render(request, 'smartgrid/post_login/appliances/Shiftingloadcycle.html',
                  {'appliance': appliance,
                   'flexstart': appliance.flexibility_start,
                   'flexend': appliance.flexibility_end,
                   'currently_on': appliance.currently_on})


def heatloadvariable(request, appliance_id):
    appliance = get_object_or_404(HeatLoadVariablePower, pk=appliance_id)
    return render(request, 'smartgrid/post_login/appliances/Heatloadvariable.html',
                  {'appliance': appliance,
                   'currently_on': appliance.currently_on,
                   'power_required': appliance.power_required,
                   'isolation_coefficient': appliance.isolation_coefficient,
                   'cop': appliance.coefficient_of_performance,
                   'mass_of_air': appliance.mass_of_air,
                   'power_consumed': appliance.power_consumed})

def heatloadinvariable(request, appliance_id):
    appliance = get_object_or_404(HeatLoadInvariablePower, pk=appliance_id)
    return render(request, 'smartgrid/post_login/appliances/Heatloadinvariable.html',
                  {'appliance': appliance,
                   'power_required': appliance.power_required,
                   'isolation_coefficient': appliance.isolation_coefficient,
                   'cop': appliance.coefficient_of_performance,
                   'mass_of_air': appliance.mass_of_air,
                   'power_consumed': appliance.power_consumed})

def scenario(request):
    scenario = Scenario.objects.all()[0]
    current_neighborhood_name = scenario.current_neighborhood
    current_neighborhood = Neighborhood.objects.get(neighborhood_name=current_neighborhood_name)

    energy_price_data = []
    for energy_price in current_neighborhood.energyprice_set.all():
        energy_price_data.append([(float(energy_price.time)-1.0)/4.0, float(energy_price.price)])

    available_energy_data = []
    for available_energy in current_neighborhood.availableenergy_set.all():
        available_energy_data.append([(float(available_energy.time)-1.0)/4.0, float(available_energy.amount)])

    neighborhood_list = Neighborhood.objects.all()

    return render(request, 'smartgrid/post_login/scenario.html',
                  {'current_neighborhood_name': current_neighborhood_name,
                   'energy_price_data': energy_price_data,
                   'available_energy_data': available_energy_data,
                   'neighborhood_list': neighborhood_list})


def change_scenario(request, neighborhood_id):
    neighborhood = get_object_or_404(neighborhood_id)
    scenario = Scenario.objects.all()[0]
    scenario.current_neighborhood = neighborhood.neighborhood_name


def trigger_gams(request):
    if request.POST:
        print 'gams'


def send_to_pi(request, time):
    onoffinfo = OnOffInfo.objects.filter(time=time)
    list_to_send = []
    scenario = Scenario.objects.all()[0]
    # om vaste id's te geven: bv: {diepvries_huis_A: 1, diepvries_huis_B: 2,...}
    fixed_appliance_dictionary = {}

    for onoff in onoffinfo:
        if onoff.house.neighbourhood.neighborhood_name == scenario.current_neighborhood:
            house = onoff.house.house_name

            status = onoff.Info
            #
            appliance_name = onoff.appliance_name
            # appliance_id = fixed_appliance_list[appliance_name]
            list_to_send += [[house, status, appliance_name]]
