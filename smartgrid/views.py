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

    consumption_data = []

    neighborhood_list = Neighborhood.objects.all()

    return render(request, 'smartgrid/post_login/scenario.html',
                  {'scenario_started': scenario.started,
                   'current_neighborhood_name': current_neighborhood_name,
                   'energy_price_data': energy_price_data,
                   'available_energy_data': available_energy_data,
                   'consumption_data': consumption_data,
                   'neighborhood_list': neighborhood_list})


def change_scenario(request, neighborhood_id):
    neighborhood = get_object_or_404(neighborhood_id)
    scenario = Scenario.objects.all()[0]
    scenario.current_neighborhood = neighborhood.neighborhood_name
    return scenario(request)


def set_scenario_time(request, i):
    scenario = Scenario.objects.all()[0]
    scenario.time = i
    # send_to_pi(i)
    return HttpResponse("OK")

def trigger_gams(request):
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

        ambiant_temp = AmbientTemp.objects.filter(Neighborhood=scenario.current_neighborhood)
        for i in ambiant_temp:
            param_temp_amb.add_record(i.time).value = i.temperature

        energy_price = EnergyPrice.objects.filter(Neighborhood=scenario.current_neighborhood)
        for i in energy_price:
            param_price.add_record(i.time).value = i.price

        available_energy = AvailableEnergy.objects.filter(Neighborhood=scenario.current_neighborhood)
        for i in available_energy:
            param_resloc.add_record(i.time).value = i.amount
        # fixed demand
        param_dcat1 = db.add_parameter_dc('DCAT1', [set_t], 'category 1 demand')

        fixed_demand = FixedDemandProfile.objects.filter(Neighborhood=scenario.current_neighborhood)
        total_consumption = [list() for _ in xrange(97)]
        # go by every time, add consumption to consumed when time equals fixed_demand.time, add consumption to dcat
        for time in range(0, 97):
            consumed = 0
            for i in fixed_demand:
                if i.time == time:
                    consumed += i.consumption
                param_dcat1.add_record(time).value = consumed

        param_cyc_cat2 = db.add_parameter_dc('CYC_CAT2', [set_cat2, set_t], 'demand of cat 2')
        # heatloadinvariablepower
        param_ua_cat3 = db.add_parameter_dc('UA_CAT3', [set_cat3], 'isolation constant')
        param_cop_cat3 = db.add_parameter_dc('COP_CAT3', [set_cat3], 'coefficient of performance ')
        param_pcool_cat3 = db.add_parameter_dc('PCOOL_CAT3', [set_cat3], 'power needed ')
        param_mass_cat3 = db.add_parameter_dc('MASS_CAT3', [set_cat3], 'mass of the cooled air inside ')

        category3 = HeatLoadInvariablePower.objects.filter(Neighborhood=scenario.current_neighborhood)
        for i in category3:
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

        category4 = HeatLoadInvariablePower.objects.filter(Neighborhood=scenario.current_neighborhood)
        for i in category4:
            set_cat4.add_record(i.appliance_name)

            param_cop_cat4.add_record(i.appliance_name).value = i.coefficient_of_performance
            param_mass_cat4.add_record(i.appliance_name).value = i.mass_of_air
            param_pcool_cat4.add_record(i.appliance_name).value = i.power_required
            param_ua_cat4.add_record(i.appliance_name).value = i.isolation_coefficient


def send_to_pi(request, time):
    scenario = Scenario.objects.all()[0]
    onoffinfo = OnOffInfo.objects.filter(time=time, Neighborhood=scenario.current_neighborhood)
    list_to_send = []
    # om vaste id's te geven: bv: {diepvries_huis_A: 1, diepvries_huis_B: 2,...}
    fixed_appliance_dictionary = {}

    for onoff in onoffinfo:
        house = onoff.house.house_name

        status = onoff.Info
        #
        appliance_name = onoff.appliance_name
        # appliance_id = fixed_appliance_list[appliance_name]
        list_to_send += [[house, status, appliance_name]]