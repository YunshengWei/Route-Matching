# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 21:30:10 2014

@author: LeBronJames
"""

"""
Thie module defines some useful helper functions
used by more than one modules
to avoid circular imports.
"""

from math import sqrt, ceil
from collections import defaultdict
import datetime
import matplotlib.pyplot as plt

from configuration import min_long, grid_len_long, \
min_lati, grid_len_lati, around_grid, match_dist, \
split_pts_int
import configuration

def dist(p1, p2):
    """
    calculate euclidian distance between p1 and p2
    """
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    
def grid_index(p):
    """
    p[0] is longitude, p[1] is latitude
    """
    return (int(ceil((p[0] - min_long) / float(grid_len_long))), 
            int(ceil((p[1] - min_lati) / float(grid_len_lati))))
            
def make_empty_grids_dict():
    """
    make empty grids using defaultdict as
    underlying data structure instead of list.
    This function is more robust than make_empty_grids, 
    and does not assume ranges of longitude and latitude.
    """
    grids = defaultdict(lambda : defaultdict(dict))
    return grids

def process_routes(routes, grid):
    """
    put routes in corresponding grids
    """
    for route in routes:
        route_no = route.get_no()
        for i, site in enumerate(route):      
            idx, idy = grid_index(site)
            for longi, lati in neighbor_id(idx, idy):
                grid[longi][lati].setdefault(route_no, set())
                grid[longi][lati][route_no].add(i)

def neighbor_id(id_x, id_y):
    """
    return neighborhood location of (id_x, id_y),
    i.e.  [id_x - around_gird, id_x + around_gird] 
        * [id_y - around_grid, id_y + around_grid]
    """
    for i in xrange(-around_grid + id_x, around_grid + id_x + 1):
        for j in xrange(-around_grid + id_y, around_grid + id_y + 1):
            yield (i, j)            

def weighted_location(time, location1, location2, time1, time2):
    """
    return location at time t.
    time must be (time1, time2)
    """
    l0 = (location2[0] - location1[0]) / float(time2 - time1) + location1[0]
    l1 = (location2[1] - location1[1]) / float(time2 - time1) + location1[1]
    return (l0, l1)
    
def binary_search(ele, l, key = lambda x: x):
    """
    binary search ele in a list l,
    return ('found', index) (if hit) (if many hits, return only one)
    or ('interval', (index1, index2))
    or ('head', 0)
    or ('end', len(l)-1)
    or None if l is empty
    """
    if not l:
        return None
    if key(l[0]) > ele:
        return ('head', 0)
    if key(l[-1]) < ele:
        return ('end', len(l) - 1)
    start = 0
    end = len(l) - 1
    while end >= start:
        pivot = int(ceil((start + end) / 2.0))
        if key(l[pivot]) == ele:
            return ('found', pivot)
        elif key(l[pivot]) > ele:
            end = pivot - 1
        else:
            start = pivot + 1
    return ('interval', (end, start))
    
#def extract_time_series_from_vehicle(vehicle, routes):
#    """
#    extract time series from vehicle according to given routes.
#    """
#    # Use the naivest methods for now.
#    # the same logic as split_vehicle_by_route
#    all_split_ids = []
#    for route in routes:
#        split_ids = []
#        for k, site in enumerate(route):
#            last_dist = float('inf')
#            last_id = -split_pts_int - 100
#            for i in xrange(len(vehicle)):
#                cur_dist = dist(vehicle.get_location(i), site)
#                if cur_dist >= match_dist:
#                    continue
#                if i - last_id >= split_pts_int:
#                    split_ids.append([vehicle.get_GpsTime(i), 
#                                      route.get_no(), k])
#                    last_dist = cur_dist    
#                elif cur_dist <= last_dist:
#                    split_ids[-1][0] = vehicle.get_GpsTime(i)
#                    last_dist = cur_dist
#                last_id = i
#        
#        split_ids.sort(key = lambda x:x[0])
#        new_split_ids = []
#        for i in xrange(0, len(split_ids) - 1):
#            if split_ids[i][2] != split_ids[i + 1][2]:
#                new_split_ids.append(split_ids[i])
#        new_split_ids.append(split_ids[-1])
#        split_ids = new_split_ids
#                
#        maxmins = []
#        if split_ids[0][2] > split_ids[1][2]:
#            maxmins.append((0, 'max'))
#        if split_ids[0][2] < split_ids[1][2]:
#            maxmins.append((0, 'min'))
#        
#        for i in xrange(1, len(split_ids) - 1):
#            if split_ids[i][2] > split_ids[i + 1][2] and split_ids[i] > split_ids[i - 1][2]:
#                maxmins.append((i, 'max'))
#            if split_ids[i][2] < split_ids[i + 1][2] and split_ids[i] < split_ids[i - 1][2]:
#                maxmins.append((i, 'min'))
#                
#        if split_ids[-1][2] < split_ids[-2][2]:
#            maxmins.append((len(split_ids) - 1, 'min'))
#        if split_ids[-1][2] > split_ids[-2][2]:
#            maxmins.append((len(split_ids) - 1, 'max'))
#
#        splits =                 
#        all_split_ids += split_ids
#
#    all_split_ids.sort(key = lambda x: x[0])
#    
#    return all_split_ids
#    
#    
#if __name__ == "__main__":
#    vehicles = read_data.read_vehicles(configuration.database, ['013661842734'])
#    routes = read_data.read_routes(configuration.lines_file)
#    routes = [routes.get_route('14'), routes.get_route('15')]
#    for vehicle in vehicles:
#        ts = extract_time_series_from_vehicle(vehicle, routes[:1])
#        for a,b,c in ts:
#            print datetime.datetime.utcfromtimestamp(a).strftime("%Y-%m-%d %H:%M:%S"),b,c
#        vehicle.plot(0, 4999)
#        plt.hold(True)
#        vehicle.plot(5000, 9000, 'ro')
        
    
    
    
    
    
    
    
    
    