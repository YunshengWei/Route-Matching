# -*- coding: utf-8 -*-
"""
Created on Fri Sep 05 15:21:09 2014

@author: WEIYUNSHENG
"""

import sqlite3
from vehicle import Vehicle, Vehicles
from route import Route, Routes
from card import Card, Cards

def read_vehicles(database, query_no):
    """
    read vehicle data
    """
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    # database should have index on Sim
    if query_no == "all":
        cursor.execute("SELECT DISTINCT id FROM vehicles")
        all_ids = cursor.fetchall()
    else:
        all_ids = [(no, ) for no in query_no]
    vehicles = Vehicles()
    for ID in all_ids:
        # Order by Id?
        cursor.execute("""SELECT gpstime, latitude, longitude 
                          FROM vehicles
                          WHERE id = ? ORDER BY gpstime ASC""", ID)
        results = cursor.fetchall()
        vehicle = Vehicle(results, ID[0])
        vehicle = vehicle.denoise()
        vehicles.add(vehicle)
    cursor.close()
    conn.close()
    return vehicles
    
def read_routes(route_file):
    """
    read route data
    """
    with open(route_file, 'r') as f:
        # the first line is title        
        f.readline()
        routes = Routes()
        for line in f:
            line = line.strip()
            if not line: continue
            parts = filter(None, line.split(','))            
            route_no = parts[0]
            sites = [tuple(map(float, s.split('|'))) for s in parts[1:]]
            route = Route(route_no, sites)
            routes.add(route)
    return routes
    
def read_routes_supplement(routes, route_supp_file):
    with open(route_supp_file, 'r') as f:
        # the first line is title        
        f.readline()
        for line in f:
            line = line.strip()
            if not line: continue
            parts = filter(None, line.split(','))            
            route_no = parts[0]
            sites = [tuple(map(float, s.split('|'))) for s in parts[1:]]
            routes.get_route(route_no).add_supplement_info(sites)
    return routes
    
def read_cards(database, query_tuple):
    """
    read card data
    """
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    if query_tuple == "all":
        cursor.execute("SELECT DISTINCT posid, statid FROM cards")
        all_cards = cursor.fetchall()
    else:
        all_cards = query_tuple
    cards = Cards()
    for t in all_cards:
        cursor.execute("""SELECT time FROM cards
                          WHERE posid = ? AND statid = ?
                          ORDER BY time ASC""", t)
        results = cursor.fetchall()
        results = [time[0] for time in results]
        card = Card(results, t)
        cards.add(card)
    cursor.close()
    conn.close()
    return cards