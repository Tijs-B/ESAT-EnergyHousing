from django.shortcuts import get_object_or_404, render
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.template import RequestContext, loader
from django.contrib import auth
from itertools import chain
from django.contrib.auth.decorators import login_required
import os

# Security:
from django.core.context_processors import csrf
import cgi

from .models import *

import utilities
from demo import *
from demo2 import *


# GAMS
# import sqlite3 as sq
import gams


# import os


# Create your views here.

# Prehomepage


def prehomepage(request):
    return render(request, 'smartgrid/prehomepage.html')


def resultaat(request):
    consumption_list_1 = []
    consumption_list_1.append({"name": "Met vraagzijdesturing",
                               "data": utilities.get_consumption(neighborhood=Neighborhood.objects.get(neighborhood_name="Buurt 1"))})
    consumption_list_1.append({"name": "Zonder vraagzijdesturing",
                               "data": utilities.get_consumption(neighborhood=Neighborhood.objects.get(neighborhood_name="Buurt 1 zonder vraagzijdesturing"))})

    consumption_list_2 = []
    consumption_list_2.append({"name": "Met vraagzijdesturing",
                               "data": utilities.get_consumption(neighborhood=Neighborhood.objects.get(neighborhood_name="Buurt 2"))})
    consumption_list_2.append({"name": "Zonder vraagzijdesturing",
                               "data": utilities.get_consumption(neighborhood=Neighborhood.objects.get(neighborhood_name="Buurt 2 zonder vraagzijdesturing"))})


    return render(request, 'smartgrid/info/resultaat.html',
                  {'consumption_list_1': consumption_list_1,
                   'consumption_list_2': consumption_list_2})


def info_apparaten(request):
    return render(request, 'smartgrid/info/info_apparaten.html')


def vraagzijdesturing(request):
    return render(request, 'smartgrid/info/vraagzijdesturing.html')


def projectverdeling(request):
    return render(request, 'smartgrid/info/projectverdeling.html')


def demo_encryptie(request):
    gecodeerd = ''
    tag1 = ''
    hexa = ''
    tag2 = ''
    oorspronkelijk = ''
    nonce = ''
    if (request.GET.get('dencryptbtn')):
        hexa = request.GET.get("hexa")
        tag2 = request.GET.get("tag2")
        nonce = request.GET.get("nonce")
        oorspronkelijk = decrypt(hexa, tag2, nonce)

    if (request.GET.get('encryptbtn')):
        gecodeerd, tag1, nonce = demo((request.GET.get('mytextbox')))

    return render(request, 'smartgrid/post_login/demo_encryptie.html', {'gecodeerd': gecodeerd,
                                                                        'tag1': tag1, 'nonce': nonce,
                                                                        'oorspronkelijk': oorspronkelijk})


# Login


def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('smartgrid/login.html', c)


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return redirect('smartgrid:home')
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



@login_required(redirect_field_name='next')
def home(request):
    scenario = Scenario.objects.all()[0]
    current_neighborhood_name = scenario.current_neighborhood
    current_neighborhood = Neighborhood.objects.get(neighborhood_name=current_neighborhood_name)

    energy_price_data = []
    for energy_price in current_neighborhood.energyprice_set.all():
        energy_price_data.append([(float(energy_price.time) - 1.0) / 4.0, float(energy_price.price)])

    return render(request, 'smartgrid/post_login/homepage.html',
                  {'full_name': request.user.username,
                   'energy_price_data': energy_price_data})


@login_required(redirect_field_name='next')
def rooms(request):
    rooms_list = Room.objects.all()
    return render(request, 'smartgrid/post_login/rooms.html',
                  {'rooms_list': rooms_list})


@login_required(redirect_field_name='next')
def room_detail(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    return render(request, 'smartgrid/post_login/room_detail.html',
                  {'room': room})


## Appliances

@login_required(redirect_field_name='next')
def shiftingloadcycle(request, appliance_id):
    appliance = get_object_or_404(ShiftingLoadCycle, pk=appliance_id)
    latest_end = appliance.latest_end_time * 15
    hours = latest_end / 60
    minutes = latest_end % 60
    latest_end_time = "%02d" % hours + ':' + "%02d" % minutes
    return render(request, 'smartgrid/post_login/appliances/Shiftingloadcycle.html',
                  {'appliance': appliance,
                   'latest_end_time': latest_end_time})


@login_required(redirect_field_name='next')
def heatloadvariable(request, appliance_id):
    appliance = get_object_or_404(HeatLoadVariablePower, pk=appliance_id)
    return render(request, 'smartgrid/post_login/appliances/Heatloadvariable.html',
                  {'appliance': appliance,
                   'power_required': appliance.power_required,
                   'isolation_coefficient': appliance.isolation_coefficient,
                   'cop': appliance.coefficient_of_performance,
                   'mass_of_air': appliance.mass_of_air})


@login_required(redirect_field_name='next')
def heatloadinvariable(request, appliance_id):
    appliance = get_object_or_404(HeatLoadInvariablePower, pk=appliance_id)
    temperature_min = appliance.temperature_min_inside - 273
    temperature_max = appliance.temperature_max_inside - 273
    return render(request, 'smartgrid/post_login/appliances/Heatloadinvariable.html',
                  {'appliance': appliance,
                   'power_required': appliance.power_required,
                   'isolation_coefficient': appliance.isolation_coefficient,
                   'cop': appliance.coefficient_of_performance,
                   'mass_of_air': appliance.mass_of_air,
                   'temperature_min': temperature_min,
                   'temperature_max': temperature_max})


@login_required(redirect_field_name='next')
# Apparaat toevoegen
def add_appliance(request, room_id):
    room = get_object_or_404(Room, pk=room_id)

    store = get_object_or_404(Room, room_name='Store')
    all_appliances = list(chain(HeatLoadInvariablePower.objects.filter(room_id=store.id),
                                HeatLoadVariablePower.objects.filter(room_id=store.id),
                                ShiftingLoadCycle.objects.filter(room_id=store.id)))

    wanted_appliances = all_appliances
    return render(request, 'smartgrid/post_login/appliances/add_appliance.html',
                  {'room': room, 'appliances': wanted_appliances})


@login_required(redirect_field_name='next')
def add(request, room_id):
    r = get_object_or_404(Room, pk=room_id)
    error_message = "Gelieve een apparaat te kiezen."
    store = get_object_or_404(Room, room_name='Store')
    print store
    all_appliances = list(chain(HeatLoadInvariablePower.objects.filter(room_id=store.id),
                                HeatLoadVariablePower.objects.filter(room_id=store.id),
                                ShiftingLoadCycle.objects.filter(room_id=store.id)))
    
    wanted_appliances = all_appliances

    try:
        selected_choice = request.POST['appliance']
    except KeyError:
        return render(request, 'smartgrid/post_login/appliances/add_appliance.html', {
            'room': r,
            'error_message': "Gelieve een apparaat te kiezen",
            'appliances': wanted_appliances})

    appliance = list(chain(ShiftingLoadCycle.objects.all().filter(appliance_name=selected_choice),
                           HeatLoadInvariablePower.objects.all().filter(appliance_name=selected_choice),
                           HeatLoadVariablePower.objects.all().filter(appliance_name=selected_choice)))

    if isinstance(appliance[0], HeatLoadVariablePower):
        r.heatloadvariablepower_set.add(appliance[0])
        r.save()
        return HttpResponseRedirect(reverse('smartgrid:room_detail', args=(r.id,)))
    elif isinstance(appliance[0], HeatLoadInvariablePower):
        r.heatloadinvariablepower_set.add(appliance[0])
        r.save()
        return HttpResponseRedirect(reverse('smartgrid:room_detail', args=(r.id,)))
    elif isinstance(appliance[0], ShiftingLoadCycle):
        r.shiftingloadcycle_set.add(appliance[0])
        r.save()
        return HttpResponseRedirect(reverse('smartgrid:room_detail', args=(r.id,)))
    else:
        return render(request, 'smartgrid/post_login/appliance/add_appliance.html', {
            'room': r,
            'error_message': "Het lijkt erop dat er iets is misgegaan, probeer opnieuw a.u.b.",
            'appliances': wanted_appliances})


def delete_appliance(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    appliances = list(chain(HeatLoadInvariablePower.objects.filter(room_id=room_id),
                            HeatLoadVariablePower.objects.filter(room_id=room_id),
                            ShiftingLoadCycle.objects.filter(room_id=room_id)))
    return render(request, 'smartgrid/post_login/appliances/delete_appliance.html',
                  {'room': room, 'appliances': appliances})


def delete(request, room_id):
    r = Room.objects.get(room_name='Store')
    orig_room = get_object_or_404(Room, pk=room_id)
    error_message = "Gelieve een apparaat te kiezen."

    appliances = list(chain(HeatLoadInvariablePower.objects.filter(room_id=room_id),
                            HeatLoadVariablePower.objects.filter(room_id=room_id),
                            ShiftingLoadCycle.objects.filter(room_id=room_id)))

    try:
        selected_choice = request.POST['appliance']
    except KeyError:
        return render(request, 'smartgrid/post_login/appliances/delete_appliance.html', {
            'room': orig_room,
            'error_message': "Gelieve een apparaat te kiezen",
            'appliances': appliances})

    appliance = list(chain(ShiftingLoadCycle.objects.all().filter(appliance_name=selected_choice),
                           HeatLoadInvariablePower.objects.all().filter(appliance_name=selected_choice),
                           HeatLoadVariablePower.objects.all().filter(appliance_name=selected_choice)))

    if isinstance(appliance[0], HeatLoadVariablePower):
        r.heatloadvariablepower_set.add(appliance[0])
        r.save()
        return HttpResponseRedirect(reverse('smartgrid:room_detail', args=(room_id,)))
    elif isinstance(appliance[0], HeatLoadInvariablePower):
        r.heatloadinvariablepower_set.add(appliance[0])
        r.save()
        return HttpResponseRedirect(reverse('smartgrid:room_detail', args=(room_id,)))
    elif isinstance(appliance[0], ShiftingLoadCycle):
        r.shiftingloadcycle_set.add(appliance[0])
        r.save()
        return HttpResponseRedirect(reverse('smartgrid:room_detail', args=(room_id,)))
    else:
        return render(request, 'smartgrid/post_login/appliance/delete_appliance.html', {
            'room': orig_room,
            'error_message': "Het lijkt erop dat er iets is misgegaan, probeer opnieuw a.u.b.",
            'appliances': appliances})


@login_required(redirect_field_name='next')
def scenario(request):
    scenario = Scenario.objects.all()[0]
    current_neighborhood_name = scenario.current_neighborhood
    current_neighborhood = Neighborhood.objects.get(neighborhood_name=current_neighborhood_name)

    energy_price_data = []
    for energy_price in current_neighborhood.energyprice_set.all():
        energy_price_data.append([(float(energy_price.time) - 1.0) / 4.0, float(energy_price.price)])

    solar_data = []
    wind_data = []
    for available_energy in current_neighborhood.availableenergy_set.all():
        solar_data.append([(float(available_energy.time) - 1.0) / 4.0, float(available_energy.amount)])
        wind_data.append([(float(available_energy.time) - 1.0) / 4.0, float(available_energy.wind)])
    available_energy_list = [{"name": "Verwachte zonne-energie", "data": solar_data},
                             {"name": "Verwachte windenergie", "data": wind_data}]

    consumption_list = []
    for house in current_neighborhood.house_set.all():
        name = house.house_name
        data = utilities.get_consumption(house)
        consumption_list.append({"name": name, "data": data})

    # consumption_list.append({"name": "Volledige buurt", "data": utilities.get_consumption(), "linewidth": 5})


    if not current_neighborhood_name.endswith("zonder vraagzijdesturing"):
        neighborhood_geen_sturing = Neighborhood.objects.get(neighborhood_name=current_neighborhood_name + " zonder vraagzijdesturing")
        consumption_list.append({"name": "Zonder vraagzijdesturing",
                                 "data": utilities.get_consumption(neighborhood=neighborhood_geen_sturing)})
    else:
        neighborhood_met_sturing = Neighborhood.objects.get(neighborhood_name=current_neighborhood_name[0:7])
        consumption_list.append({"name": "Met vraagzijdesturing",
                                 "data": utilities.get_consumption(neighborhood=neighborhood_met_sturing)})


    neighborhood_list = Neighborhood.objects.all()
    neighborhood_list.filter(neighborhood_name='Store').delete()

    return render(request, 'smartgrid/post_login/scenario.html',
                  {'current_neighborhood_name': current_neighborhood_name,
                   'energy_price_data': energy_price_data,
                   'available_energy_list': available_energy_list,
                   'consumption_list': consumption_list,
                   'neighborhood_list': neighborhood_list})


def change_scenario(request, neighborhood_id):
    neighborhood = get_object_or_404(Neighborhood, pk=neighborhood_id)
    scenario = Scenario.objects.all()[0]
    scenario.current_neighborhood = neighborhood.neighborhood_name
    scenario.save()
    return redirect('smartgrid:scenario')


def set_scenario_time(request, i):
    scenario = Scenario.objects.all()[0]
    scenario.time = i
    utilities.send_to_pi(i)
    return HttpResponse("OK")
