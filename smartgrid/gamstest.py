from gams import *
import os
import sys
import sqlite3 as sq


conn = sq.connect('db.sqlite3')
c = conn.cursor()

price = list()

for i in range(1, 45):
    price.append((i, i, 20, 1))
for i in range(45, 97):
    price.append((i, i, 10, 1))

c.executemany("INSERT INTO smartgrid_ambienttemp VALUES (?, ?, ?, ?)", price)
conn.commit()