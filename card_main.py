# -*- coding: utf-8 -*-
"""
Created on Wed Sep 03 20:28:56 2014

@author: Yunsheng Wei
"""

from __future__ import division
import cPickle as pickle
import matplotlib.pyplot as plt

from configuration import map_file, \
lines_file, connector_file, between_card_time, \
database, card_query_tuple, query_no, dist_card_time, \
dist_stop, offsets
from read_data import read_cards, read_routes, read_vehicles
from helper import grid_index, make_empty_grids_dict, process_routes, dist
from mapper import Mapper
import connector

#def time_seqs_match(ts, ts_list, interval_width):
#    """
#    Given a time sequence, find the best match from a list of time sequences.
#    ts is pos machine data.
#    ts_list is vehicle stop data.
#    ts_list should not be empty.
#    @ return: (index, ratio)
#    """
#    ratios = []
#    time_grid = set()
#    for timestamp in ts:
#        grid_index = int(ceil(timestamp / time_grid_width))
#        time_grid.add(grid_index)
#    for cand_ts in ts_list:
#        cand_grid = set()
#        for timestamp in cand_ts:
#            grid_index = int(ceil(timestamp / time_grid_width))
#            cand_grid.add(grid_index)
#            cand_grid.add(grid_index - 1)
#            cand_grid.add(grid_index + 1)
#        ratios.append(len(cand_grid & time_grid) / len(time_grid))
#    index = max(xrange(len(ratios)), key = lambda x: ratios[x])
#    return (index, ratios[index])
    

def match_card_from_vehicles(card, mapper, connector, routes, grids, vehicles):
    """
    find the best match for the card
    """
    route_nos = mapper.get_lineid_from_statid(card.get_no()[1])
    
    cand_vehicles_nos = set()
    for route_no in route_nos:    
        cand_vehicles_nos |= connector.get_cands(route_no)

    cand_vehicles = [vehicles.get_vehicle(vehicle_no)
                     for vehicle_no in cand_vehicles_nos]
                
    card = card.get_simplified_card(between_card_time)
    max_max_num = 0
    max_vehicle = None
    best_best_offset = 0
    plt.close('all')
    for vehicle in cand_vehicles:
        match_num_1 = 0
        best_offset = 0
        for offset in offsets:
            match_num = 0
            time_sequences = map(lambda x: x + offset, card.get_time_sequence())
            locations = vehicle.get_locations_at_timestamps(time_sequences)
#            x, y = zip(*filter(None, locations))
#            plt.figure()
#            vehicle.plot(0, len(vehicle))
#            plt.plot(x, y, 'gs')
#            for route_no in list(route_nos)[:1]:
#                route = routes.get_route(route_no)
#                route.plot(0, len(route), 'ro')
#                
#            plt.show()

            last_location = (0, 0)
            for location in locations:
                if location == None:
                    continue
                gid = grid_index(location)
                for route_no in route_nos:
                    tmp_set = grids[gid[0]][gid[1]].get(route_no, set())
                    if not tmp_set or dist(location, last_location) <= dist_card_time:
                        continue
                    route = routes.get_route(route_no)
                    min_dist = min(dist(location, route.get_location(i)) for i in tmp_set)
                    if min_dist < dist_stop:
                        match_num += 1
                        break
                last_location = location
            if match_num > match_num_1:
                match_num_1 = match_num
                best_offset = offset
            
        print vehicle.get_no(), match_num_1, '/', len(card), best_offset
        if match_num_1 > max_max_num:
            max_max_num = match_num_1
            max_vehicle = vehicle
            best_best_offset = best_offset
    return max_max_num, len(card), max_vehicle, best_best_offset


if __name__ == "__main__":
    conn = pickle.load(open(connector_file, 'rb'))
    cards = read_cards(database, card_query_tuple)
    mapper = Mapper(map_file)
    routes = read_routes(lines_file)

    cand_vehicles_nos = set()
    for card in cards:
        route_nos = mapper.get_lineid_from_statid(card.get_no()[1])
        for route_no in route_nos:    
            cand_vehicles_nos |= conn.get_cands(route_no)
    query_no_tmp = list(cand_vehicles_nos)

    vehicles = read_vehicles(database, query_no_tmp)
    
    grids = make_empty_grids_dict()
    process_routes(routes, grids)
  
    for card in cards:
        print card.get_no()
        max_max_num, num_cards, vehicle, offset = match_card_from_vehicles(card, mapper, conn, routes, grids, vehicles)
        if vehicle == None:
            print "No match"
        else:
            print "Best match:\n", max_max_num, '/', num_cards, vehicle.get_no(), offset
        #_ = raw_input("press any key to continue")




