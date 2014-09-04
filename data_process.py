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
    """
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS vehicles")
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS vehicles
                  (id INTEGER PRIMARY KEY,
                   latitude REAL,
                   longitude REAL,
                   gpstime INTEGER,
                   sim TEXT)
                   """)
    cursor.execute("CREATE INDEX IF NOT EXISTS sim_index ON vehicles(sim)")
    cursor.execute("CREATE INDEX IF NOT EXISTS gpstime_index ON vehicles(gpstime)")
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
    """
    put data in cards_file into database.
    """
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS cards")
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS cards
                  (posid TEXT,
                   time INTEGER,
                   statid TEXT)
                   """)
    cursor.execute("CREATE INDEX time_index ON cards(time)")
    cursor.execute("CREATE INDEX statid_index ON cards(statid)")
    cursor.execute("CREATE INDEX posid_index ON cards(posid)")
    with open(cards_file, 'r') as reader:
        for line in reader:
            parts = line.strip().split(',')
            assert len(parts) == 15
            if parts[5].count(':') == 1:
                parts[5] = parts[5] + ":00"
            parts[5] = datetime.strptime(parts[5], "%Y/%m/%d %H:%M:%S")
            parts[5] = calendar.timegm(parts[5].utctimetuple())
            cursor.execute("INSERT INTO cards VALUES (?, ?, ?)",
                           (parts[3], parts[5], parts[9]))
            
    cursor.close()
    conn.commit()
    conn.close()

if __name__ == "__main__":
    cards_to_database(configuration.database, configuration.cards_file)