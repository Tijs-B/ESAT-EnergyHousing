from django.shortcuts import get_object_or_404, render
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.template import RequestContext, loader
from django.contrib import auth
from itertools import chain

# Security:
from django.core.context_processors import csrf
import cgi

from .models import *
import utilities
from demo import *


# GAMS
# import sqlite3 as sq
# import gams
# import os


# Create your views here.

# Prehomepage


def prehomepage(request):
    return render(request, 'smartgrid/prehomepage.html')


def resultaat(request):
    return render(request, 'smartgrid/info/resultaat.html')


def info_apparaten(request):
    return render(request, 'smartgrid/info/info_apparaten.html')


def vraagzijdesturing(request):
    return render(request, 'smartgrid/info/vraagzijdesturing.html')


def projectverdeling(request):
    return render(request, 'smartgrid/info/projectverdeling.html')


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


def rooms(request):
    rooms_list = Room.objects.all()
    return render(request, 'smartgrid/post_login/rooms.html',
                  {'rooms_list': rooms_list})


def room_detail(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    return render(request, 'smartgrid/post_login/room_detail.html',
                  {'room': room})


## Appliances
'''
def fixed(request, appliance_id):
    appliance = get_object_or_404(FixedDemand, pk=appliance_id)
    return render(request, 'smartgrid/post_login/appliances/Fixed.html',
                  {'appliance': appliance,
                   'consumption': appliance.consumption,
                   'currently_on':appliance.currently_on})
'''


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


def demo_encryptie(request):
    encryptie = ''

    if (request.GET.get('encryptbtn')):
        encryptie = demo((request.GET.get('mytextbox')))
    print encryptie
    return render(request, 'smartgrid/post_login/demo_encryptie.html', {'encryptie': encryptie})


# Apparaat toevoegen
def add_appliance(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    appliances = list(chain(HeatLoadInvariablePower.objects.all(),
                            HeatLoadVariablePower.objects.all(),
                            ShiftingLoadCycle.objects.all()))
    return render(request, 'smartgrid/post_login/appliances/add_appliance.html',
                  {'room': room, 'appliances': appliances})


def add(request, room_id):
    r = get_object_or_404(Room, pk=room_id)
    error_message = "Gelieve een apparaat te kiezen."
    appliances = list(chain(HeatLoadInvariablePower.objects.all(),
                            HeatLoadVariablePower.objects.all(),
                            ShiftingLoadCycle.objects.all()))
    try:
        selected_choice = request.POST['appliance']
    except KeyError:
        return render(request, 'smartgrid/post_login/appliances/add_appliance.html', {
            'room': r,
            'error_message': "Gelieve een apparaat te kiezen",
            'appliances': appliances})

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
            'appliances': appliances})


def scenario(request):
    scenario = Scenario.objects.all()[0]
    current_neighborhood_name = scenario.current_neighborhood
    current_neighborhood = Neighborhood.objects.get(neighborhood_name=current_neighborhood_name)

    energy_price_data = []
    for energy_price in current_neighborhood.energyprice_set.all():
        energy_price_data.append([(float(energy_price.time) - 1.0) / 4.0, float(energy_price.price)])

    available_energy_data = []
    for available_energy in current_neighborhood.availableenergy_set.all():
        available_energy_data.append([(float(available_energy.time) - 1.0) / 4.0, float(available_energy.amount)])

    consumption_list = []
    for house in current_neighborhood.house_set.all():
        name = house.house_name
        data = utilities.get_consumption(house)
        consumption_list.append({"name": name, "data": data})

    consumption_list.append({"name": "Volledige buurt", "data": utilities.get_consumption(), "linewidth": 5})

    neighborhood_list = Neighborhood.objects.all()

    return render(request, 'smartgrid/post_login/scenario.html',
                  {'current_neighborhood_name': current_neighborhood_name,
                   'energy_price_data': energy_price_data,
                   'available_energy_data': available_energy_data,
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
    # utilities.send_to_pi(i)
    return HttpResponse("OK")


def trigger_gams(request):
    house = House.objects.all()
    if request.POST:
        # gams workshop initialisatie
        ws = gams.GamsWorkspace(working_directory=os.getcwd())

        job = ws.add_job_from_file('SEH-frigo-huis-vriezer-database-communicatie (1).gms')

        opt = ws.add_options()

        db = ws.add_database()
        opt.defines["SupplyDataFileName"] = db.name
        # definieer de sets
        set_t = db.add_set('t', 1, 'time')

        for i in range(0, 97):
            set_t.add_record(i)

        set_cat1 = db.add_set('cat1', 1, 'appliances of category one')
        set_cat2 = db.add_set('cat2', 1, 'appliances of category two')
        set_cat3 = db.add_set('cat3', 1, 'appliances of category three, heatloadinvariablepower')
        set_cat4 = db.add_set('cat4', 1, 'appliances of category four, heatloadvariablepower')

        scenario = Scenario.objects.all()[0]
        # buitentemperatuur, prijs en renewables
        param_temp_amb = db.add_parameter_dc('TEMP_AMB', [set_t], 'Temperature of the environment (in K) -> time')
        param_price = db.add_parameter_dc('PRICE', [set_t], 'price of energy')
        param_resloc = db.add_parameter_dc('RESLOC', [set_t], 'local supply renewables')

        ambiant_temp = AmbientTemp.objects.filter(neighborhood=scenario.current_neighborhood)
        for i in ambiant_temp:
            param_temp_amb.add_record(i.time).value = i.temperature

        energy_price = EnergyPrice.objects.filter(neighborhood=scenario.current_neighborhood)
        for i in energy_price:
            param_price.add_record(i.time).value = i.price

        available_energy = AvailableEnergy.objects.filter(neighborhood=scenario.current_neighborhood)
        for i in available_energy:
            param_resloc.add_record(i.time).value = i.amount
        # fixed demand
        param_dcat1 = db.add_parameter_dc('DCAT1', [set_t], 'category 1 demand')

        fixed_demand = FixedDemandProfile.objects.all()
        # go by every time, add consumption to consumed when time equals fixed_demand.time, add consumption to dcat
        for time in range(0, 97):
            consumed = 0
            for i in fixed_demand:
                if i.room.house.neighbourhood == scenario.current_neighborhood:
                    if i.time == time:
                        consumed += i.consumption
                    param_dcat1.add_record(time).value = consumed

        param_cyc_cat2 = db.add_parameter_dc('CYC_CAT2', [set_cat2, set_t], 'demand of cat 2')
        # heatloadinvariablepower
        param_ua_cat3 = db.add_parameter_dc('UA_CAT3', [set_cat3], 'isolation constant')
        param_cop_cat3 = db.add_parameter_dc('COP_CAT3', [set_cat3], 'coefficient of performance ')
        param_pcool_cat3 = db.add_parameter_dc('PCOOL_CAT3', [set_cat3], 'power needed ')
        param_mass_cat3 = db.add_parameter_dc('MASS_CAT3', [set_cat3], 'mass of the cooled air inside ')

        category3 = HeatLoadInvariablePower.objects.all()
        for i in category3:
            if i.room.house.neighbourhood == scenario.current_neighborhood:
                set_cat3.add_record(i.appliance_name)

                param_cop_cat3.add_record(i.appliance_name).value = i.coefficient_of_performance
                param_mass_cat3.add_record(i.appliance_name).value = i.mass_of_air
                param_pcool_cat3.add_record(i.appliance_name).value = i.power_required
                param_ua_cat3.add_record(i.appliance_name).value = i.isolation_coefficient
        # heatloadvariablepower
        param_ua_cat4 = db.add_parameter_dc('UA_CAT4', [set_cat4], 'isolation constant of')
        param_cop_cat4 = db.add_parameter_dc('COP_CAT4', [set_cat4], 'coefficient of performance')
        param_pcool_cat4 = db.add_parameter_dc('PCOOL_CAT4', [set_cat4], 'power needed ')
        param_mass_cat4 = db.add_parameter_dc('MASS_CAT4', [set_cat4], 'mass of the cooled air inside')

        category4 = HeatLoadVariablePower.objects.all()
        for i in category4:
            if i.room.house.neighbourhood == scenario.current_neighborhood:
                set_cat4.add_record(i.appliance_name)

                param_cop_cat4.add_record(i.appliance_name).value = i.coefficient_of_performance
                param_mass_cat4.add_record(i.appliance_name).value = i.mass_of_air
                param_pcool_cat4.add_record(i.appliance_name).value = i.power_required
                param_ua_cat4.add_record(i.appliance_name).value = i.isolation_coefficient
