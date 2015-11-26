from models import *
from planning_verstuurder import *

def send_to_pi(time):
    scenario = Scenario.objects.all()[0]
    onoffinfo = OnOffInfo.objects.filter(time=time)
    # om vaste id's te geven: bv: {diepvries_huis_A: 1, diepvries_huis_B: 2,...}
    fixed_appliance_dictionary = {}
    list_to_send = []
    for onoff in onoffinfo:
        if onoff.house.neighbourhood == scenario.current_neighborhood:
            house = onoff.house.house_name
            status = onoff.Info
            appliance_name = onoff.appliance_name
            # appliance_id = fixed_appliance_list[appliance_name]
            list_to_send += [[house, status, appliance_name]]
    verstuur(list_to_send)


