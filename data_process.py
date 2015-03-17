# -*- coding: utf-8 -*-
"""
Created on Wed Sep 03 21:31:29 2014

@author: LeBronJames
"""

import sqlite3, calendar
from datetime import datetime

from mapper import Mapper
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
                  (id TEXT,
                   gpstime INTEGER,
                   latitude REAL,
                   longitude REAL)
                   """)
    cursor.execute("CREATE INDEX IF NOT EXISTS id_index ON vehicles(id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS gpstime_index ON vehicles(gpstime)")
    with open(vehicles_file, 'r') as reader:
        # the first line should give the column order
        line = reader.readline().strip()
        cols = map(lambda x: x.strip(), line.split(','))
        for line in reader:
            parts = map(lambda x:x.strip(), line.strip().split(','))
            values = {cols[i] : parts[i] for i in xrange(len(cols))}
            values['LATITUDE'] = float(values['LATITUDE'])
            values['LONGITUDE'] = float(values['LONGITUDE'])
            values['GPS_TIME'] = datetime.strptime(values['GPS_TIME'], "%Y-%m-%d %H:%M:%S")
            values['GPS_TIME'] = calendar.timegm(values['GPS_TIME'].utctimetuple())
            cursor.execute("INSERT INTO vehicles VALUES (?, ?, ?, ?)", 
                           (values['ID'], values['GPS_TIME'], 
                            values['LATITUDE'], values['LONGITUDE']))
            
    cursor.close()
    conn.commit()
    conn.close()

def cards_to_database(database, cards_file):
    """
    put data in cards_file into database.
    """
    
    mapper = Mapper(configuration.map_file)
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
            if not mapper.has_statid(parts[9]):
                continue
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