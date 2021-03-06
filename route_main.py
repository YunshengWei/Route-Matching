# -*- coding: utf-8 -*-
"""
Created on Sat Jun 07 16:44:32 2014

@author: Yunsheng Wei
"""

from __future__ import division
import traceback, time
from math import ceil
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt 

import cPickle as pickle

import configuration
from configuration import min_long, min_lati, \
max_long, max_lati, grid_len_long, grid_len_lati, \
match_thres, around_grid, match_dist, match_thres_one, \
split_pts_int, stop_time, connector_file, lines_file_supplement

from matcher import Matcher
from helper import dist, grid_index, \
make_empty_grids_dict, process_routes, neighbor_id
from read_data import read_vehicles, read_routes, read_routes_supplement
from connector import Connector
from route import Routes

#########################################################
# Debug code
def check_order(vehicle):
    """
    This function is only used for debug.
    check vehicle column 'Id' is in order
    """
    last_id = float('-inf')
    for Id, _, _, _ in vehicle:
        assert Id > last_id, \
        "vehicle %d column Id not in order" % vehicle.get_no()
        last_id = Id
    print "vehicle %d column Id is in order." % vehicle.get_no()
    
def check_vehicle_long_lati(vehicle):
    """
    This function is only used for debug.
    check all longitudes are in (min_long, max_long)
    all latitudes are in (min_lati, max-lati)
    """
    for Id, lati, longi, _ in vehicle:
        assert min_lati < lati < max_lati, \
        "vehicle %d latitude out of range, Id %d" % (vehicle.get_no(), Id)
        assert min_long < longi < max_long, \
        "vehicle %d longitude out of range, Id %d" % (vehicle.get_no(), Id)
    print "vehicle %d longitudes and latitudes are legal." % vehicle.get_no()
        
def check_route_long_lati(route):
    """
    This function is only used for debug.
    check all longitudes are in (min_long, max_long)
    all latitudes are in (min_lati, max-lati)
    """
    for longi, lati in route:
        assert min_lati < lati < max_lati, \
        "route %d latitude out of range" % route.get_no()
        assert min_long < longi < max_long, \
        "route %d longitude out of range" % route.get_no()
    print "route %d longitudes and latitudes are legal." % route.get_no()
    
def check_GPS_time(vehicle):
    """
    This function is only used for debug.
    check vehicle GPSTime is in order.
    """
    last_datetime = datetime(2011, 1, 1, 0, 0, 0)
    for _, _, _, time in vehicle:
        time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        assert time >= last_datetime, \
        "vehicle %d column GPSTime not in order" % vehicle.get_no()
        last_datetime = time
    print "vehicle %d column GPSTime is in order." % vehicle.get_no()
######################################################### 

#########################################################
# Deprecated
def make_empty_grids():
    """
    make empty grids in [min_long, max_long] * [min_lati, max_lati]
    """
    num_long = int(ceil((max_long - min_long) / grid_len_long)) + 1
    num_lati = int(ceil((max_lati - min_lati) / grid_len_lati)) + 1
    grids = [[dict() for i in xrange(num_lati)] for j in xrange(num_long)]
    return grids
#########################################################
    

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
        id_x, id_y = grid_index(location)
        if (id_x, id_y) in used: continue
        used.add((id_x, id_y))
        for route_no, sites in grids[id_x][id_y].iteritems():
#             for site_no in sites:
#                site_loc = routes.get_route(route_no).get_location(site_no)
#                if dist(site_loc, location) < match_dist:
#                    matched[route_no].add(site_no)
            matched[route_no] |= sites
    route_cands = Routes()
    for route_no, sites in matched.iteritems():
        if len(sites) / routes.get_route_len(route_no) >= match_thres:
            route_cands.add(routes.get_route(route_no))
    return route_cands

def subset_match(vehicle, start, end, route, grids):
    """
    return whether vehicle[start..end] match route
    """
    used = set()
    matched_sites_no = set()
    route_no = route.get_no()
    for i in xrange(start, end + 1):
        loc = vehicle.get_location(i)
        id_x, id_y = grid_index(loc)
        if (id_x, id_y) in used: continue
        used.add((id_x, id_y))
        if grids[id_x][id_y].has_key(route_no):
            matched_sites_no |= grids[id_x][id_y][route_no]
    return True if len(matched_sites_no) / len(route) > match_thres_one else False
    
def subset_match_with_dist(vehicle, start, end, route, grids):
    """
    return whether vehicle[start..end] match route.
    unlike subset_match, subset_match_with_dist 
    considers match_dist, is slower but more accurate.
    """
    matched_sites_no = set()
    route_no = route.get_no()
    for i in xrange(start, end + 1):
        loc = vehicle.get_location(i)
        id_x, id_y = grid_index(loc)
        if grids[id_x][id_y].has_key(route_no):
            sites_no_set = set(site_no for site_no in grids[id_x][id_y][route_no]
                               if dist(route.get_location(site_no), loc) < match_dist)
            matched_sites_no |= sites_no_set
    return True if len(matched_sites_no) / len(route) > match_thres_one else False    

#########################################################
# Deprecated
def split_cands(routes):
    """
    return split candidates according to destinations of route in routes
    """
    split_pts = dict()
    for route in routes:
        dest_loc = route.get_dest_loc()
        for id_x, id_y in neighbor_id(*grid_index(dest_loc)):
            split_pts.setdefault((id_x, id_y), set())
            split_pts[(id_x, id_y)].add(route)
    return split_pts
#########################################################
    
def split_vehicle_by_route(vehicle, route):
    """
    split vehicle according to route
    """
    split_ids = []
    last_dist = float('inf')
    last_id = -split_pts_int - 100
    for i in xrange(len(vehicle)):
        # choose best split points for current route
        # from continuous split points
        cur_dist = dist(vehicle.get_location(i), route.get_dest_loc())
        if cur_dist < match_dist:
            if i - last_id >= split_pts_int:
                split_ids.append([i, route.get_no()])
                last_dist = cur_dist
            elif cur_dist <= last_dist:
                split_ids[-1][0] = i
                last_dist = cur_dist
            last_id = i
    return split_ids
                
def split_vehicle_by_route_with_time(vehicle, route):
    """
    split vehicle according to route.
    Compared with split_vehicle_by_route, this version
    also takes into account stop_time
    """    
    pass

def split_vehicle_by_routes(vehicle, route_cands):
    """
    split vehicle according to route in route_cands
    """
    split_indices = []
    for route in route_cands:
        split_indices += split_vehicle_by_route(vehicle, route)
    split_indices.sort(key = lambda x : x[0])
    split_pts = []
    last_i = -1
    for i, route_no in split_indices:
        if last_i == i:
            split_pts[-1][1].add(route_no)
        else:
            split_pts.append((i, set([route_no])))
        last_i = i
    return split_pts

def match_route_dp(vehicle, routes, grids):
    """
    dynamic programming algorithm to match routes.
    
    """
    route_cands = filter_by_grids(vehicle, routes, grids)
    split_indices = split_vehicle_by_routes(vehicle, route_cands)
    # (match_routes_count, match_sites_count)
    # match_sited_count is compared only when
    # match_routes_count are equal
    aux = [(0, 0)] * (len(split_indices) + 1)
    back_points = [None] * (len(split_indices) + 1)
    valid = [False] * len(split_indices)
    for i, (j, route_no_set) in enumerate(split_indices, 1):
        aux[i] = aux[i - 1]
        back_points[i] = back_points[i - 1]
        cand_pts = [(0, 0)] + [(k + 1, s + 1) for k, (s, _) in enumerate(split_indices[0:i-1]) 
                               if valid[k]]
        for route_no in route_no_set:
            for s, k in reversed(cand_pts):
                if subset_match_with_dist(vehicle, k, j, routes.get_route(route_no), grids):
                    if 1 + aux[s][0] > aux[i][0] \
                    or aux[s][0] + 1 == aux[i][0] \
                    and aux[s][1] + routes.get_route(route_no).length() > aux[i][1]:
                        valid[i - 1] = True
                        aux[i] = (aux[s][0] + 1, aux[s][1] + routes.get_route(route_no).length())
                        back_points[i] = (s, k, route_no)
    matcher = Matcher(vehicle, grids)
    i = len(vehicle) - 1
    s = len(back_points) - 1
    while back_points[s] != None:
        s, k, route_no = back_points[s]
        matcher.insert(0, k, i, routes.get_route(route_no))
        i = k - 1
    return matcher

#########################################################
# Not finished
def error_handling():
    """
    Handle errors and write error info into file.
    known possible errors: 
    1. latitude or longitude out of range
    2. vehicle column 'Id' not in order
    """
    pass
#########################################################

if __name__ == "__main__":
    routes = read_routes(configuration.lines_file)
    routes = read_routes_supplement(routes, configuration.lines_file_supplement)
    grids1 = make_empty_grids_dict()
    grids2 = make_empty_grids_dict()
    process_routes(routes, grids1, grids2)
    vehicles = read_vehicles(configuration.database, configuration.query_no)
    plt.close('all')
    matchers = []
    for vehicle in vehicles:
        try:
            #print "vehicle %s" % vehicle.get_no()
            #t0 = time.clock()
            matcher = match_route_dp(vehicle, routes, grids1)
            #print matcher
            #matcher.plot()
            matcher.niceprint(grids2)
            matchers.append(matcher)
        except:
            print traceback.format_exc()
        finally:
            pass
            #print "Elapsed time : %s" % (time.clock()- t0)
            #print "-" * 40
    connector = Connector(matchers)
    pickle.dump(connector, open(connector_file, 'wb'))
    
#    i = 0
#    plt.figure()
#    plt.hold()
#    for vehicle in vehicles:
#        pass
#    while i < len(vehicle):
#        k = len(vehicle) - 1
#        for j in xrange(i, len(vehicle)):
#            if vehicle.get_location(j) != vehicle.get_location(i):
#                k = j - 1
#                break
#        if vehicle.get_GpsTime(k) - vehicle.get_GpsTime(i) >= stop_time:
#            print i, datetime.utcfromtimestamp(vehicle.get_GpsTime(i)).strftime("%Y-%m-%d %H:%M:%S"), \
#            k, datetime.utcfromtimestamp(vehicle.get_GpsTime(k)).strftime("%Y-%m-%d %H:%M:%S")
#            plt.plot(vehicle.get_location(i)[0], vehicle.get_location(i)[1], 'ro')
#        i = k + 1
#    routes.get_route('108').plot(0, len(routes.get_route('108')))
#    routes.get_route('70').plot(0, len(routes.get_route('70')))
#    routes.get_route('48').plot(0, len(routes.get_route('48')))
#    plt.show()
            

#    plt.figure()
#    vehicle.plot(0, len(vehicle), 'b--')
#    r1 = routes.get_route(77)
#    r2 = routes.get_route(103)
#    r1.plot(0, len(r1), 'g<')
#    r2.plot(0, len(r2), 'rH')
        
        
        
        
        
        
    