# import gams
# import os, glob
# import csv
from models import *
from communicatie.planning_verstuurder import *


def send_to_pi(time):
    onoffinfo = OnOffInfo.objects.filter(time=time)
    # om vaste id's te geven: bv: {diepvries_huis_A: 1, diepvries_huis_B: 2,...}
    appliance_dictionary = {'Koelkast': 2,          # ok
                            'Diepvries': 4,         # ok
                            'Afwasmachine': 10,     # ok
                            'Auto': 16,             # ok
                            'Droogkast': 17,        # ok
                            'licht': 21,            #
                            'ventilator': 22,       #
                            'fornuis': 24,          #
                            'Wasmachine': 26}       # ok
    house_dictionary = {'Huisje 1': 0,
                        'Huisje 1 zonder vraagzijdesturing': 1,
                        'Huisje 2': 0,
                        'Huisje 2 zonder vraagzijdesturing': 1}
    for i in range(0, 2):
        if i == 0:
            scenario = Scenario.objects.all()[0].current_neighborhood
        else:
            scenario = str(Scenario.objects.all()[0].current_neighborhood) + " zonder vraagzijdesturing"
        list_to_send = []
        for onoff in onoffinfo:
            if onoff.house.neighborhood.neighborhood_name == scenario:
                house = onoff.house.house_name
                house_id = house_dictionary[house]

                if onoff.info > 0:
                    status = 1
                else:
                    status = 0

                appliance_name = onoff.appliance_name[0:-2]
                if appliance_name in appliance_dictionary:
                    appliance_id = appliance_dictionary[appliance_name]

                    list_to_send += [[house_id, status, appliance_id]]

        verstuur(list_to_send)

'''
def trigger_gams():
    scenario = Scenario.objects.all()[0]
    house_all = House.objects.all()
    print 'test'
    for house in house_all:
        print 'test'
        if house.neighborhood.neighborhood_name == scenario.current_neighborhood:
            # gams workshop initialisatie
            ws = gams.GamsWorkspace(working_directory=os.getcwd(), debug=gams.DebugLevel.ShowLog)

            job = ws.add_job_from_file('SEH_volledige_code_met_database_7december.gms')

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
            param_deadline_cat2 = db.add_parameter_dc('DEADLINE_CAT2', [set_cat2], 'latest allowed moment for finish')

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

            available_energy = AvailableEnergy.objects.filter(
                neighborhood__neighborhood_name=scenario.current_neighborhood)
            for i in available_energy:
                param_resloc.add_record(str(i.time)).value = i.amount
            # fixed demand

            fixed_demand = FixedDemandProfile.objects.filter(house=house)
            for i in fixed_demand:
                param_dcat1.add_record(str(i.time)).value = i.consumption

            # shifting load
            shiftingloadcycle = ShiftingLoadCycle.objects.filter(room__house=house)
            for i in shiftingloadcycle:
                set_cat2.add_record(str(i.appliance_name))

                param_n_cycles_cat2.add_record(str(i.appliance_name)).value = 1
                param_deadline_cat2.add_record(str(i.appliance_name)).value = i.latest_end_time
                total_duration = 0
                shiftingloadprofile = ShiftingLoadProfile.objects.filter(shiftingloadcycle=i)
                for profile in shiftingloadprofile:
                    total_duration += 1
                    param_d_cycle_cat2.add_record(
                        [str(i.appliance_name), str(profile.time)]).value = profile.consumption
                param_dur_cat2.add_record(str(i.appliance_name)).value = total_duration


            # heatloadinvariablepower
            category3 = HeatLoadInvariablePower.objects.filter(room__house=house)
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

            category4 = HeatLoadVariablePower.objects.filter(room__house=house)[0]
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

            thermo_profile = ThermoProfile.objects.filter(house=house)
            for x in thermo_profile:
                param_t_min_cat4.add_record(str(x.time)).value = x.temp_min
                param_t_max_cat4.add_record(str(x.time)).value = x.temp_max
            """
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
            
            for time in range(1, 96):
                param_t_min_cat4.add_record(str(time)).value = category4.temperature_min_inside
                param_t_max_cat4.add_record(str(time)).value = category4.temperature_max_inside

            param_pload_battery = db.add_parameter_dc('Pload_battery', ['1'], 'laadvermogen')
            param_capacity_battery = db.add_parameter_dc('Capacity_battery', ['1'], 'capaciteit')
            """
            car = Car.objects.filter(house=house)
            """
            param_pload_battery.add_record(['1']).value = car[0].load_capacity
            param_capacity_battery.add_record(['1']).value = car[0].power_capacity
            """
            opt.defines["PLOAD"] = str(car[0].load_capacity)
            opt.defines["CAP"] = str(car[0].total_power_capacity)

            print 'job run?'
            print db
            job.run(gams_options=opt, databases=db)
            print 'job run'
            print 'test'

            # delete all previous entries


            # CalculatedConsumption
            for x in job.out_db.get_variable('total_load'):
                house.calculatedconsumption_set.create(time=x.keys[0], total_consumption=x.level)
            # onoffprofile car
            car_profile = OnOffProfile(car = car[0])
            car_profile.save()
            for x in job.out_db.get_variable('P_cat5'):
                car_profile.onoffinfo_set.create(time=x.keys[0], info=x.level, on_off=1 if x.level > 0 else 0)
            # onoffprofile verwarming (category4)
            category4_profile = OnOffProfile(heatloadvariablepower=category4)
            category4_profile.save()
            for x in job.out_db.get_variable('P_cat4'):
                category4_profile.onoffinfo_set.create(time=x.keys[0], info=x.level, on_off=1 if x.level > 0 else 0)
            # onoffprofile invariablepower
            category3_profile = []
            for index in range(0, len(category3)):
                category3_profile += [OnOffProfile(heatloadinvariablepower=category3[index])]
                category3_profile[index].save()

            for x in job.out_db.get_variable('z_cat3'):
                for index in range(0, len(category3)):
                    if x.keys[1] == category3[index].appliance_name:
                        category3_profile[index].onoffinfo_set.create(time=x.keys[0], info=category3[index].power_required if x.level > 0 else 0, on_off=x.level)
            # onoffprofile shiftingload
            for x in job.out_db.get_variable('ti'):
                if x.level == 1:
                    appl_name = x.keys[1]
                    # get shiftingloadprofile
                    shiftingloadcycle = ShiftingLoadCycle.objects.filter(room__house=house, appliance_name=appl_name)[0]
                    # make onoffprofile

                    shiftingload_consumption = OnOffProfile(shiftingloadcycle=shiftingloadcycle)
                    shiftingload_consumption.save()
                    # make onoffinfo
                    total_duration = 0
                    shiftingloadprofile = ShiftingLoadProfile.objects.filter(shiftingloadcycle=shiftingloadcycle)
                    list_of_times = []
                    for index in range(0, len(shiftingloadprofile)):
                        total_duration += 1
                        shiftingload_consumption.onoffinfo_set.create(time=int(x.keys[0])+index, info=shiftingloadprofile[index].consumption, on_off=1)
                        list_of_times += [int(x.keys[0])+index]
                    # fill the rest with 0
                    for i in range(1, 97):
                        if i not in list_of_times:
                            shiftingload_consumption.onoffinfo_set.create(time=i, info=0, on_off=0)

            print 'test'
            for f in glob.glob('_gams_py_*'):
                if str(f) != '_gams_py_gdb1.gdx':
                    os.remove(f)
            print "all done"
'''


def get_consumption(house=None, neighborhood=None):
    """
    Returns a list of consumption data for the given house, or for all the houses in the current neighborhood together.
    e.g. [[1, 25.4], [2, 27.3], ..., [96, 12.5]]
    """
    scenario = Scenario.objects.all()[0]
    if neighborhood is None:
        current_neighborhood_name = scenario.current_neighborhood
        current_neighborhood = Neighborhood.objects.get(neighborhood_name=current_neighborhood_name)
    else:
        current_neighborhood = neighborhood
        current_neighborhood_name = current_neighborhood.neighborhood_name

    consumption = [[i/4.0, 0] for i in range(96)]

    if house is not None:
        calculated_consumption = CalculatedConsumption.objects.filter(house=house)
        for x in calculated_consumption:
            consumption[x.time-1][1] = x.total_consumption
    else:
        calculated_consumption = CalculatedConsumption.objects.filter(house__neighborhood=current_neighborhood)
        for x in calculated_consumption:
            consumption[x.time-1][1] += x.total_consumption

    return consumption


def create_test_database():
    n = Neighborhood(neighborhood_name="Goede buurt")
    n.save()
    print "created neighborhood!"

    for i in range(1, 97):
        n.ambienttemp_set.create(time=i, temperature=2 * i)
        print "   created ambienttemp! i=" + str(i)
        n.energyprice_set.create(time=i, price=i ** 2 - 3 * i)
        print "   created energyprice! i=" + str(i)
        n.availableenergy_set.create(time=i, amount=100 * i ** 2 - 50 * i)
        print "   created availableenergy! i=" + str(i)

    s = Scenario(scenario_name="Default scenario", current_neighborhood="Goede buurt", time=1, started=False)
    s.save()
    print "created scenario!"

    h1 = House(neighborhood=n, house_name="Huis 1 in de goede buurt")
    h1.save()
    print "created house!"
    for i in range(1, 97):
        h1.fixeddemandprofile_set.create(time=i, consumption=2 * i)
        print "   created fixeddemand! i=" + str(i)

    r = Room(house=h1, room_name="Keuken")
    r.save()
    print "created room!"

    hlv = HeatLoadVariablePower(room=r, appliance_name="HLV", currently_on=False, power_required=100,
                                isolation_coefficient=10, coefficient_of_performance=1.01, mass_of_air=1000
                                )

    hlv.save()
    print "created HLV!"

    oop = OnOffProfile(heatloadvariablepower=hlv)
    oop.save()

    for i in range(1, 97):
        oop.onoffinfo_set.create(time=i, on_off=1 if 30 < i < 60 else 0, info=100)
        print "   created onoffinfo! i=" + str(i)

    h2 = House(neighborhood=n, house_name="Huis 2 in de goede buurt")
    h2.save()

    for i in range(1, 97):
        h2.fixeddemandprofile_set.create(time=i, consumption=15)
        print "   created fixeddemand! i=" + str(i)

    n2 = Neighborhood(neighborhood_name="Andere buurt")
    n2.save()
    print "created other neighborhood!"

    n3 = Neighborhood(neighborhood_name="Store")
    n3.save()

    hs = House(neighborhood=n3, house_name="Store")
    hs.save()

    rs = Room(house=hs, room_name="Store")
    rs.save()
    print "created the store! $.$"



def add_csv_to_database(filename, object, type=None):
    """
    Voegt een csv (onder /smartgrid/csv) toe aan de database.
    Parameters:
    - filename: de naam van het bestand
    - object: Neighborhood, House or OnOffProfile
    - type: (alleen voor een Neighborhood): "ambienttemp", "energyprice" of "availableenergy"
    Alle waarden moeten ints of floats zijn met een . ipv een ,.
    Er moet 1 kolom zijn in het csv bestand.
    """

    with open(os.path.join("csv", filename), 'rU') as file: # Exception handling

        if isinstance(object, Neighborhood):
            if type == "ambienttemp":
                i = 1
                reader = csv.reader(file) # Open csv reader
                for row in reader:
                    a = AmbientTemp(neighborhood=object, time=i, temperature=float(row[0]))
                    a.save()
                    print "Time:", i
                    print "Amount:", float(row[0])
                    i += 1
            elif type == "energyprice":
                i = 1
                reader = csv.reader(file) # Open csv reader
                for row in reader:
                    e = EnergyPrice(neighborhood=object, time=i, price=float(row[0]))
                    e.save()
                    print "Time:", i
                    print "Amount:", float(row[0])
                    i += 1
            elif type == "availableenergy":
                i = 1
                reader = csv.reader(file) # Open csv reader
                for row in reader:
                    string = row[0]
                    data = string.split(';')
                    e = AvailableEnergy(neighborhood=object, time=i, amount=float(data[0]), wind=float(data[1]))
                    e.save()
                    print "Time:", i
                    i += 1
            else:
                print 'ERROR: Wrong type "' + str(type) + '".'

        elif isinstance(object, House):
            if type == "thermo":
                i = 1
                reader = csv.reader(file) # Open csv reader
                for row in reader:
                    string = row[0]
                    data = string.split(';')
                    t = ThermoProfile(house=object, time=i, temp_min=float(data[0]), temp_max=float(data[1]))
                    t.save()
                    print "Time:", i
                    print "Amount:", float(data[0]), float(data[1])
                    i += 1
            elif type == "fixeddemand":
                i = 1
                reader = csv.reader(file) # Open csv reader
                for row in reader:
                    f = FixedDemandProfile(house=object, time=i, consumption=float(row[0]))
                    f.save()
                    print "Time:", i
                    print "Amount:", float(row[0])
                    i += 1

        elif isinstance(object, OnOffProfile):
            i = 1
            reader = csv.reader(file) # Open csv reader
            for row in reader:
                if float(row[0]) == 0:
                    o = OnOffInfo(onoffprofile=object, time=i, on_off=0, info=1.0)
                    o.save()
                else:
                    o = OnOffInfo(onoffprofile=object, time=i, on_off=1, info=float(row[0]))
                    o.save()
                print "Time:", i
                print "Amount:", float(row[0])
                i += 1
        else:
            print 'ERROR: Wrong object, class "' + object.__class__.__name__ + '" not expected.'

        print "FINISHED!"