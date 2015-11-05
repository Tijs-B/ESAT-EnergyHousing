from gams import *
import os
import sys

ws = GamsWorkspace()

ws.gamslib("trnsport")
t1 = ws.add_job_from_file("trnsport.gms")
t1.run()

for rec in t1.out_db["x"]:
    print "x(" + rec.keys[0] + "," + rec.keys[1] + "): level=" + str(rec.level) + " marginal=" + str(rec.marginal)