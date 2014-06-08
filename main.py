# -*- coding: utf-8 -*-
"""
Created on Sat Jun 07 16:44:32 2014

@author: Yunsheng Wei
"""

from __future__ import division
import sqlite3
from math import sqrt, ceil
from collections import defaultdict
import configuration
from configuration import min_long, min_lati, \
max_long, max_lati, grid_len_long, grid_len_lati, \
match_thres, around_grid, match_dist, match_thres_one

from vehicle import Vehicle, Vehicles
from route import Route, Routes

#########################################################
# Debug code
def check_order(vehicles):
    """
    This function is only used for debug.
    check every vehicle in vehicles is in order
    """
    for vehicle in vehicles:
        last_id = float('-inf')
        for Id, _, _, _ in vehicle:
            assert Id > last_id, \
            "vehicle %d column Id not in order" % vehicle.get_no()
            last_id = Id
    print "All vehicles column Id are in order."
#########################################################
    
def read_vehicles(database, query_no):
    """
    read vehicle data
    """
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    # database should have index on Sim
    if query_no == "all":
        cursor.execute("SELECT DISTINCT Sim FROM Vehicles")
        all_sims = cursor.fetchall()
    else:
        all_sims = [(no, ) for no in query_no]
    vehicles = Vehicles()
    for sim in all_sims:
        # Order by Id?
        cursor.execute("""SELECT Id, Latitude, Longitude, GpsTime FROM Vehicles
                          WHERE Sim = ?""", sim)
        results = cursor.fetchall()
        vehicle = Vehicle(results, sim[0])
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
            route_no = int(parts[0])
            sites = [tuple(map(float, s.split('|'))) for s in parts[1:]]
            route = Route(route_no, sites)
            routes.add(route)
    return routes

def dist(p1, p2):
    """
    calculate euclidian distance between p1 and p2
    """
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    

def grid_index(p):
    """
    p[0] is longitude, p[1] is latitude
    """
    return (int(ceil((p[0] - min_long) / grid_len_long)), 
            int(ceil((p[1] - min_lati) / grid_len_lati)))

def make_empty_grids():
    """
    make grids in [min_long, max_long] * [min_lati, max_lati]
    """
    num_long = int(ceil((max_long - min_long) / grid_len_long)) + 1
    num_lati = int(ceil((max_lati - min_lati) / grid_len_lati)) + 1
    grids = [[set() for i in xrange(num_lati)] for j in xrange(num_long)]
    return grids
    
def process_routes(routes, grid):
    """
    put routes in corresponding grids
    """
    for route in routes:
        route_no = route.get_no()
        for i, site in enumerate(route):      
            x, y = grid_index(site)
            for longi, lati in neighbor_loc(x, y):
                grid[longi][lati].add((route_no, i))

def neighbor_loc(x, y):
    """
    return neighborhood location of (x, y),
    i.e.  [x - around_gird, x + around_gird] * [y - around_grid, y + around_grid]
    """
    for i in xrange(-around_grid + x, around_grid + x + 1):
        for j in xrange(-around_grid + y, around_grid + y + 1):
            yield (i, j)

#########################################################
# Deprecated
def neighborhood(grid, x, y, used = None):
    """
    return a generator yielding neighborhood of (x, y)
    not in used and update used (if used is given)
    [x - around_grid, x + around_grid] * [y - around_grid, y + around_grid]
    """
    if used == None:
        for i in xrange(-around_grid + x, around_grid + x + 1):
            for j in xrange(-around_grid + y, around_grid + y + 1):
                yield grid[i][j]
    else:
        if (x, y) in used: return
        for i in xrange(-around_grid + x, around_grid + x + 1):
            for j in xrange(-around_grid + y, around_grid + y + 1):
                if (i, j) not in used:
                    used.add((i, j))
                    yield grid[i][j]
#########################################################

def filter_by_grids(vehicle, routes, grids):
    """
    filter impossible routes by grids,
    return candidate routes
    """
    used = set()
    matched = defaultdict(set)
    for i in xrange(len(vehicle)):
        location = vehicle.get_location(i)
        x, y = grid_index(location)
        if (x, y) in used: continue
        used.add((x, y))
        for route_no, site_no in grids[x][y]:
            site_loc = routes.get_route(route_no).get_location(site_no)
            if dist(site_loc, location) < match_dist:
                matched[route_no].add(site_no)
    candi_routes = Routes()
    for route_no, sites in matched.iteritems():
        if len(sites) / routes.get_route_len(route_no) >= match_thres:
            candi_routes.add(routes.get_route(route_no))
    return candi_routes

def subset_match(vehicle, route, start, end):
    """
    return whether vehicle[start..end] match route
    """
    ya_grid = 
    

def split_cands(routes):
    """
    return split candidates according to destinations of route in routes
    """
    pass

def match_dp(vehicle, routes):
    """
    dynamic programming algorithm to match routes
    """
    pass
    

if __name__ == "__main__":
    grids = make_empty_grids()
    routes = read_routes(configuration.lines_file)
    process_routes(routes, grids)
    vehicles = read_vehicles(configuration.database, configuration.query_no)
    if configuration.debug_mode:
        check_order(vehicles)
    for vehicle in vehicles:
        pass
    
    
    
    
    