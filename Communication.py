import sqlite3 as sq

def make_appliance_list():
    """
    take appliances, make a list, with each a unique number
    :return:
    """
    conn = sq.connect('db.sqlite3')
    cur = conn.cursor()

    # bevat house als values, en rooms in dat house als keys
    # {room:house}
    room_dictionary = {}

    sql = 'SELECT * FROM smartgrid_room'
    cur.execute(sql)
    room = cur.fetchall()
    for i in room:
        room_dictionary[i[0]] = [i[2]]

    # bevat {appliance_name: [house, type, type_id, individual id]}
    appliance_list = {}
    # om vaste id's te geven: bv: {diepvries_huis_A: 1, diepvries_huis_B: 2,...
    fixed_appliance_list = {}

    id = 0

    sql = 'SELECT * FROM smartgrid_shiftingloadcycle'
    cur.execute(sql)
    shiftingload = cur.fetchall()
    for i in shiftingload:
        room_id = i[4]
        house_id = room_dictionary[room_id][0]
        typ = 1
        shiftingload_id = i[0]
        # shiftingload_id = fixed_appliance_list[i[1]]
        appliance_list[i[1]] = [house_id, typ, shiftingload_id, id]
        id += 1
        # print appliance_list

    sql = 'SELECT * FROM smartgrid_heatloadvariablepower'
    cur.execute(sql)
    heatloadvariable = cur.fetchall()
    for i in heatloadvariable:
        room_id = i[8]
        house_id = room_dictionary[room_id][0]
        typ = 2
        heatloadvariable_id = i[0]
        # heatloadvariable_id = fixed_appliance_list[i[1]]
        appliance_list[i[1]] = [house_id, typ, heatloadvariable_id, id]
        id += 1
        # print appliance_list

    sql = 'SELECT * FROM smartgrid_heatloadinvariablepower'
    cur.execute(sql)
    heatloadinvariable = cur.fetchall()
    for i in heatloadinvariable:
        room_id = i[8]
        house_id = room_dictionary[room_id][0]
        typ = 3
        heatloadinvariable_id = i[0]
        # heatloadinvariable_id = fixed_appliance_list[i[1]]
        appliance_list[i[1]] = [house_id, typ, heatloadinvariable_id, id]
        id += 1
        # print appliance_list

    return appliance_list

def communication_information(appliance_list):
    """
    create the list, which is used by communication
    :return:
    """
    conn = sq.connect('db.sqlite3')
    cur = conn.cursor()
    # bevat {onoffprofile_id, appliance}
    onoff_profile = {}

    sql = 'SELECT * FROM smartgrid_onoffprofile'
    cur.execute(sql)
    onoff = cur.fetchall()
    for i in onoff:
        for j in appliance_list:
            # als onoffprofile van shiftingload
            if appliance_list[j][1] == 1 and appliance_list[j][2] == i[4]:
                onoff_profile[i[0]] = j
            if appliance_list[j][1] == 2 and appliance_list[j][2] == i[3]:
                onoff_profile[i[0]] = j
            if appliance_list[j][1] == 3 and appliance_list[j][2] == i[2]:
                onoff_profile[i[0]] = j

    # [[[house, app, status],[house, app, status]...],[[house, app, status],[house, app, status],...]]
    comm_info_list = [list([]) for _ in xrange(95)]
    sql = 'SELECT * FROM smartgrid_onoffinfo'
    cur.execute(sql)
    onoffinfo = cur.fetchall()
    for i in onoffinfo:
        time = i[1]
        appliance_name = onoff_profile[i[4]]
        house = appliance_list[appliance_name][0]
        status = i[3]
        appliance_id = appliance_list[appliance_name][3]

        comm_info_list[time] += [[house, appliance_id, status]]
    print comm_info_list

    return comm_info_list


appliance_list = make_appliance_list()
communication_information(appliance_list)
