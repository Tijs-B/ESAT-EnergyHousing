import sqlite3 as sq
import gams
import os
import time
import glob

conn = sq.connect('db.sqlite3')
c = conn.cursor()

ws = gams.GamsWorkspace(working_directory=os.getcwd())

job = ws.add_job_from_file('SEH-frigo-huis-vriezer-database-communicatie (1).gms')

opt = ws.add_options()

db = ws.add_database()
opt.defines["SupplyDataFileName"] = db.name

# define the sets for gams

set_t = db.add_set('t', 1, 'time')
set_cat1 = db.add_set('cat1', 1, 'appliances of category one')
set_cat2 = db.add_set('cat2', 1, 'appliances of category two')
set_cat3 = db.add_set('cat3', 1, 'appliances of category three')
set_cat4 = db.add_set('cat4', 1, 'appliances of category four')
# define parameters
param_TEMP_AMB = db.add_parameter_dc('TEMP_AMB', [set_t], 'Temperature of the environment (in K) -> time')
param_PRICE = db.add_parameter_dc('PRICE', [set_t], 'price of energy')
param_RESLOC = db.add_parameter_dc('RESLOC', [set_t], 'local supply renewables')

param_DCAT1 = db.add_parameter_dc('DCAT1', [set_t], 'category 1 demand')

param_CYC_CAT2 = db.add_parameter_dc('CYC_CAT2', [set_cat2, set_t], 'demand of cat 2')

param_UA_CAT3 = db.add_parameter_dc('UA_CAT3', [set_cat3], 'isolation constant')
param_COP_CAT3 = db.add_parameter_dc('COP_CAT3', [set_cat3], 'coefficient of performance ')
param_PCOOL_CAT3 = db.add_parameter_dc('PCOOL_CAT3', [set_cat3], 'power needed ')
param_MASS_CAT3 = db.add_parameter_dc('MASS_CAT3', [set_cat3], 'mass of the cooled air inside ')

param_UA_CAT4 = db.add_parameter_dc('UA_CAT4', [set_cat4], 'isolation constant of')
param_COP_CAT4 = db.add_parameter_dc('COP_CAT4', [set_cat4], 'coefficient of performance')
param_PCOOL_CAT4 = db.add_parameter_dc('PCOOL_CAT4', [set_cat4], 'power needed ')
param_MASS_CAT4 = db.add_parameter_dc('MASS_CAT4', [set_cat4], 'mass of the cooled air inside')

sql = 'SELECT * FROM smartgrid_fixeddemand'
c.execute(sql)
category1 = c.fetchall()
for i in category1:




sql = 'SELECT * FROM smartgrid_heatloadinvariablepower'
c.execute(sql)
category3 = c.fetchall()
for i in category3:
    set_cat3.add_record(str(i[0]))

    param_COP_CAT3.add_record(str(i[0])).value = i[6]     #indices moeten aangepast worden afhankelijk van database!!!
    param_MASS_CAT3.add_record(str(i[0])).value = i[7]
    param_PCOOL_CAT3.add_record(str(i[0])).value = i[4]
    param_UA_CAT3.add_record(str(i[0])).value = i[5]

sql = 'SELECT * FROM smartgrid_heatloadvariablepower'
c.execute(sql)
category4 = c.fetchall()
for i in category4:
    set_cat4.add_record(str(i[0]))

    param_COP_CAT4.add_record(str(i[0])).value = i[6]     #indices moeten aangepast worden afhankelijk van database!!!
    param_MASS_CAT4.add_record(str(i[0])).value = i[7]
    param_PCOOL_CAT4.add_record(str(i[0])).value = i[4]
    param_UA_CAT4.add_record(str(i[0])).value = i[5]




if db.check_domains():
    job.run(gams_options=opt, databases=db)
    onoff = list()
    i = 1
    id_nummer = 1       # id van de refrigirator
    for zfr in job.out_db.get_variable('zfr_ref'):
        onoff.append((i, zfr.keys[0], zfr.level, 0, id_nummer))
        i = i+1
    c.executemany("INSERT OR REPLACE INTO smartgrid_onoffinfo VALUES(? ,? ,? ,? ,?)", onoff)
    conn.commit()
else:
    exit('ERROR')