# -*- coding: utf-8 -*-
"""
Created on Wed Sep 03 21:31:29 2014

@author: LeBronJames
"""

import sqlite3, calendar
from datetime import datetime

import configuration

def vehicles_to_database(database, vehicles_file):
    """
    put data in vehicles_file into database.
    Attention: this method can not be run repeatedly!
    """
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS vehicles
                  (id INTEGER PRIMARY KEY,
                   latitude REAL,
                   longitude REAL,
                   gpstime INTEGER,
                   sim TEXT)
                   """)
    cursor.execute("""
                   CREATE INDEX IF NOT EXISTS sim_index ON vehicles(sim)
                   """)
    cursor.execute("""
                   CREATE INDEX IF NOT EXISTS gpstime_index ON vehicles(gpstime)
                   """)
    with open(vehicles_file, 'r') as reader:
        # the first line should give the column order        
        line = reader.readline().strip()
        cols = map(lambda x: x.lower().strip(), line.split(','))
        for line in reader:
            line = line.strip()
            parts = map(lambda x:x.strip(), line.split(','))
            values = {cols[i] : parts[i] for i in xrange(len(cols))}
            values['id'] = int(values['id'])
            values['latitude'] = float(values['latitude'])
            values['longitude'] = float(values['longitude'])
            values['gpstime'] = datetime.strptime(values['gpstime'], "%Y-%m-%d %H:%M:%S")
            values['gpstime'] = calendar.timegm(values['gpstime'].utctimetuple())
            cursor.execute("INSERT INTO vehicles VALUES (?, ?, ?, ?, ?)", 
                           (values['id'], values['latitude'], values['longitude'],
                            values['gpstime'], values['sim']))
            
    cursor.close()
    conn.commit()
    conn.close()

def cards_to_database(database, cards_file):

if __name__ == "__main__":
    vehicles_to_database(configuration.database, configuration.vehicles_file)