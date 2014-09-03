# -*- coding: utf-8 -*-
"""
Created on Wed Sep 03 21:31:29 2014

@author: LeBronJames
"""

import sqlite3

import configuration

def vehicles_to_database(database, vehicles_file):
    """
    put data in vehicles_file into database
    """
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS vehicles
                   (id INTEGER PRIMARY KEY,
                   latitude REAL,
                   longitude REAL,
                   time INTEGER)
                   """)    
    
    cursor.commit()
    cursor.close()
    conn.close()