# -*- coding: utf-8 -*-
"""
Created on Thu Sep 04 14:02:02 2014

@author: WEIYUNSHENG
"""

"""
This file is used to write some scripts for testing.
"""

from mapper import Mapper
import sqlite3

conn = sqlite3.connect(r'C:\Users\WEIYUNSHENG\Desktop\Route Matching\data\Route_Matching.db')
cursor = conn.cursor()
# database should have index on Sim

cursor.execute("SELECT DISTINCT sim FROM vehicles")
all_sims = cursor.fetchall()
print type(all_sims[0][0])
for sim in all_sims:
    cursor.execute("""SELECT id, latitude, longitude, datetime(gpstime, 'unixepoch') 
                      FROM vehicles
                      WHERE sim = ? ORDER BY gpstime ASC""", sim)
    rows = cursor.fetchall()
cursor.close()
conn.close()