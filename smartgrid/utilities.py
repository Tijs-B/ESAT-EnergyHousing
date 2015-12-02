from models import *
from planning_verstuurder import *
import gams
import os
from models import *


def send_to_pi(time):
    scenario = Scenario.objects.all()[0]
    onoffinfo = OnOffInfo.objects.filter(time=time)
    # om vaste id's te geven: bv: {diepvries_huis_A: 1, diepvries_huis_B: 2,...}
    fixed_appliance_dictionary = {}
    list_to_send = []
    for onoff in onoffinfo:
        if onoff.house.neighbourhood_name == scenario.current_neighborhood:
            house = onoff.house.house_name
            status = onoff.Info
            appliance_name = onoff.appliance_name
            # appliance_id = fixed_appliance_list[appliance_name]
            list_to_send += [[house, status, appliance_name]]
    verstuur(list_to_send)


def trigger_gams():
    scenario = Scenario.objects.all()[0]
    house_all = House.objects.all()
    print 'test'
    for house in house_all:
        print 'test'
        if house.neighbourhood.neighborhood_name == scenario.current_neighborhood:
            # gams workshop initialisatie
            ws = gams.GamsWorkspace(working_directory=os.getcwd(), debug=gams.DebugLevel.ShowLog)

            job = ws.add_job_from_file('SEH_volledige_code_met_database1.gms')

            opt = ws.add_options()

            db = ws.add_database()
            opt.defines["SupplyDataFileName"] = db.name
            # definieer de sets
            set_t = db.add_set('t', 1, 'time')
            # time
            for i in range(1, 97):
                set_t.add_record(str(i))

            set_cat2 = db.add_set('cat2', 1, 'appliances of category two')
            set_cat3 = db.add_set('cat3', 1, 'appliances of category three')

            # buitentemperatuur, prijs en renewables
            param_temp_amb = db.add_parameter_dc('TEMP_AMB', [set_t], 'Temperature of the environment (in K) -> time')
            param_price = db.add_parameter_dc('PRICE', [set_t], 'price of energy')
            param_resloc = db.add_parameter_dc('RESLOC', [set_t], 'local supply renewables')

            param_dcat1 = db.add_parameter_dc('D_TOT_CAT1', [set_t], 'category 1 demand')

            param_d_cycle_cat2 = db.add_parameter_dc('D_CYCLE_CAT2', [set_cat2, set_t], 'demand cycle')
            param_n_cycles_cat2 = db.add_parameter_dc('N_CYCLES_CAT2', [set_cat2], 'number of cycles')
            param_dur_cat2 = db.add_parameter_dc('DUR_CAT2', [set_cat2], 'duration of cycle')

            param_ua_cat3 = db.add_parameter_dc('UA_CAT3', [set_cat3], 'isolation constant')
            param_cop_cat3 = db.add_parameter_dc('COP_CAT3', [set_cat3], 'coefficient of performance ')
            param_pcool_cat3 = db.add_parameter_dc('PCOOL_CAT3', [set_cat3], 'power needed ')
            param_mass_cat3 = db.add_parameter_dc('MASS_CAT3', [set_cat3], 'mass of the cooled air inside ')
            param_t_min_cat3 = db.add_parameter_dc('T_MIN_CAT3', [set_cat3], 'minimal temp inside device')
            param_t_max_cat3 = db.add_parameter_dc('T_MAX_CAT3', [set_cat3], 'max temp inside device')

            param_t_min_cat4 = db.add_parameter_dc('T_MIN_CAT4', [set_t], 'min temp inside')
            param_t_max_cat4 = db.add_parameter_dc('T_MAX_CAT4', [set_t], 'max temp inside')

            ambiant_temp = AmbientTemp.objects.filter(neighborhood__neighborhood_name=scenario.current_neighborhood)
            for i in ambiant_temp:
                param_temp_amb.add_record(str(i.time)).value = i.temperature

            energy_price = EnergyPrice.objects.filter(neighborhood__neighborhood_name=scenario.current_neighborhood)
            for i in energy_price:
                param_price.add_record(str(i.time)).value = i.price

            available_energy = AvailableEnergy.objects.filter(neighborhood__neighborhood_name=scenario.current_neighborhood)
            for i in available_energy:
                param_resloc.add_record(str(i.time)).value = i.amount
            # fixed demand

            fixed_demand = FixedDemandProfile.objects.filter(house__neighbourhood__neighborhood_name=scenario.current_neighborhood, house=house)
            for i in fixed_demand:
                param_dcat1.add_record(str(i.time)).value = i.consumption

            # shifting load

            shiftingloadcycle = ShiftingLoadCycle.objects.filter(room__house__neighbourhood__neighborhood_name=scenario.current_neighborhood, room__house=house)
            for i in shiftingloadcycle:
                set_cat2.add_record(str(i.appliance_name))

                param_n_cycles_cat2.add_record(str(i.appliance_name)).value = 1
                total_duration = 0
                shiftingloadprofile = ShiftingLoadProfile.objects.filter(shiftingloadcycle=i)
                for profile in shiftingloadprofile:
                    total_duration += 1
                    param_d_cycle_cat2.add_record([str(i.appliance_name), str(profile.time)]).value = profile.consumption
                param_dur_cat2.add_record(str(i.appliance_name)).value = total_duration


            # heatloadinvariablepower
            category3 = HeatLoadInvariablePower.objects.filter(room__house__neighbourhood__neighborhood_name=scenario.current_neighborhood, room__house=house)
            for i in category3:
                set_cat3.add_record(str(i.appliance_name))
                param_cop_cat3.add_record(str(i.appliance_name)).value = i.coefficient_of_performance
                param_mass_cat3.add_record(str(i.appliance_name)).value = i.mass_of_air
                param_pcool_cat3.add_record(str(i.appliance_name)).value = i.power_required
                param_ua_cat3.add_record(str(i.appliance_name)).value = i.isolation_coefficient
                param_t_min_cat3.add_record(str(i.appliance_name)).value = i.temperature_min_inside
                param_t_max_cat3.add_record(str(i.appliance_name)).value = i.temperature_max_inside
            # house

            """
            param_ua_cat4 = db.add_parameter_dc('UA_HOUSE', ['1'], 'isolation constant of')
            param_cop_cat4 = db.add_parameter_dc('COP_HOUSE', ['1'], 'coefficient of performance')
            param_pcool_cat4 = db.add_parameter_dc('PCOOL_HOUSE', ['1'], 'power needed ')
            param_mass_cat4 = db.add_parameter_dc('MASS_HOUSE', ['1'], 'mass of the cooled air inside')
            """
            category4 = HeatLoadVariablePower.objects.filter(room__house__neighbourhood__neighborhood_name=scenario.current_neighborhood, room__house=house)[0]
            """
            param_cop_cat4.add_record(['1']).value = category4.coefficient_of_performance
            param_mass_cat4.add_record(['1']).value = category4.mass_of_air
            param_pcool_cat4.add_record(['1']).value = category4.power_required
            param_ua_cat4.add_record(['1']).value = category4.isolation_coefficient
            """
            opt.defines["UA"] = str(category4.isolation_coefficient)
            opt.defines["COP"] = str(category4.coefficient_of_performance)
            opt.defines["PHEAT"] = str(category4.power_required)
            opt.defines["MASS"] = str(category4.mass_of_air)
            for time in range(1, 25):
                param_t_min_cat4.add_record(str(time)).value = 284
                param_t_max_cat4.add_record(str(time)).value = 290
            for time in range(25, 41):
                param_t_min_cat4.add_record(str(time)).value = 290
                param_t_max_cat4.add_record(str(time)).value = 296
            for time in range(41, 73):
                param_t_min_cat4.add_record(str(time)).value = 284
                param_t_max_cat4.add_record(str(time)).value = 290
            for time in range(73, 97):
                param_t_min_cat4.add_record(str(time)).value = 290
                param_t_max_cat4.add_record(str(time)).value = 296
            """
            for time in range(1, 96):
                param_t_min_cat4.add_record(str(time)).value = category4.temperature_min_inside
                param_t_max_cat4.add_record(str(time)).value = category4.temperature_max_inside
            """
            """
            param_pload_battery = db.add_parameter_dc('Pload_battery', ['1'], 'laadvermogen')
            param_capacity_battery = db.add_parameter_dc('Capacity_battery', ['1'], 'capaciteit')
            """
            car = Car.objects.filter(house__neighbourhood__neighborhood_name=scenario.current_neighborhood, house=house)
            """
            param_pload_battery.add_record(['1']).value = car[0].load_capacity
            param_capacity_battery.add_record(['1']).value = car[0].power_capacity
            """
            opt.defines["PLOAD"] = str(car[0].load_capacity)
            opt.defines["CAP"] = str(car[0].power_capacity)
            print 'test last'

            print 'job run?'
            print db
            job.run(gams_options=opt, databases=db)
            print 'job run'
            print 'test'
            # x = job.out_db.get_variable('zcost')
            # print x.level
            print 'test'


def get_consumption(house=None):
    """
    Returns a list of consumption data for the given house, or for all the houses in the current neighborhood together.
    e.g. [[1, 25.4], [2, 27.3], ..., [96, 12.5]]
    """
    scenario = Scenario.objects.all()[0]
    current_neighborhood_name = scenario.current_neighborhood
    current_neighborhood = Neighborhood.objects.get(neighborhood_name=current_neighborhood_name)

    consumption = [[i, 0] for i in range(1, 97)]

    if house is not None:
        for fixed_demand_profile in house.fixeddemandprofile_set.all():
            print fixed_demand_profile.time
            consumption[fixed_demand_profile.time - 1][1] += fixed_demand_profile.consumption

        for onoff_info in OnOffInfo.objects.all():
            if onoff_info.house == house:
                consumption[onoff_info.time - 1][1] += onoff_info.OnOff * onoff_info.Info

    else:
        for fixed_demand_profile in FixedDemandProfile.objects.all():
            if fixed_demand_profile.house.neighborhood == current_neighborhood:
                consumption[fixed_demand_profile.time - 1][1] += fixed_demand_profile.consumption

        for onoff_info in OnOffInfo.objects.all():
            if onoff_info.house.neighborhood == current_neighborhood:
                consumption[onoff_info.time - 1][1] += onoff_info.OnOff * onoff_info.Info

    return consumption


def create_test_database():
    n = Neighborhood(neighborhood_name="Goede buurt")
    n.save()
    print "created neighborhood!"

    for i in range(1, 97):
        n.ambienttemp_set.create(time=i, temperature=2*i)
        print "   created ambienttemp! i=" + str(i)
        n.energyprice_set.create(time=i, price=i**2-3*i)
        print "   created energyprice! i=" + str(i)
        n.availableenergy_set.create(time=i, amount=100*i**2 - 50*i)
        print "   created availableenergy! i=" + str(i)

    s = Scenario(scenario_name="Default scenario", current_neighborhood="Goede buurt", time=1, started=False)
    s.save()
    print "created scenario!"

    h1 = House(neighborhood=n, house_name="Huis 1 in de goede buurt")
    h1.save()
    print "created house!"
    for i in range(1, 97):
        h1.fixeddemandprofile_set.create(time=i, consumption=2*i)
        print "   created fixeddemand! i=" + str(i)

    r = Room(house=h1, room_name="Keuken")
    r.save()
    print "created room!"

    hlv = HeatLoadVariablePower(room=r, appliance_name="HLV", currently_on=False, power_required=100,
                                isolation_coefficient=10, coefficient_of_performance=1.01, mass_of_air=1000,
                                power_consumed=100, temperature_min_inside=20, temperature_max_inside=22)

    hlv.save()
    print "created HLV!"

    oop = OnOffProfile(heatloadvariablepower=hlv)
    oop.save()

    for i in range(1, 97):
        oop.onoffinfo_set.create(time=i, OnOff=1 if 30<i<60 else 0, Info=100)
        print "   created onoffinfo! i=" + str(i)

    h2 = House(neighborhood=n, house_name="Huis 2 in de goede buurt")
    h2.save()

    for i in range(1, 97):
        h2.fixeddemandprofile_set.create(time=i, consumption=15)
        print "   created fixeddemand! i=" + str(i)

    n2 = Neighborhood(neighborhood_name="Andere buurt")
    n2.save()
    print "created other neighborhood!"