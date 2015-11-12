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

set_t = db.add_set('t', 1, 'time period')
set_cat = db.add_set('app', 1, 'appliances of category three')

param_TEMP_AMB = db.add_parameter_dc('TEMP_AMB', [set_t], 'Temperature of the environment (in K) -> time')
param_UA_CAT = db.add_parameter_dc('UA_REF', [set_cat], 'isolation constant of the refrigator')
param_COP_CAT = db.add_parameter_dc('COP_REF', [set_cat], 'coefficient of performance of the refrigator')
param_PCOOL_CAT = db.add_parameter_dc('PCOOL_REF', [set_cat], 'power needed for the refrigator')
param_MASS_CAT = db.add_parameter_dc('MASS_REF', [set_cat], 'mass of the cooled air inside the refrigator')

sql = 'SELECT * FROM smartgrid_heatloadinvariablepower'
c.execute(sql)
Appliance = c.fetchall()
for i in Appliance:
    set_cat.add_record(str(i[0]))

    param_COP_CAT.add_record(str(i[0])).value = i[6]
    param_MASS_CAT.add_record(str(i[0])).value = i[7]
    param_PCOOL_CAT.add_record(str(i[0])).value = i[4]
    param_UA_CAT.add_record(str(i[0])).value = i[5]

for i in range(0, 24):
    set_t.add_record(str(i))

    param_TEMP_AMB.add_record(str(i)).value = 290

if db.check_domains():
    job.run(gams_options=opt, databases=db)

    for zfr in job.out_db.get_variable('zfr_ref'):

        print zfr.level
else:
    exit('ERROR')
