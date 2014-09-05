# -*- coding: utf-8 -*-
"""
Created on Wed Sep 03 20:28:56 2014

@author: Yunsheng Wei
"""

from __future__ import division
import cPickle as pickle

from configuration import map_file, \
lines_file, connector_file, between_card_time, \
database, card_query_tuple, query_no
from read_data import read_cards, read_routes, read_vehicles
from helper import grid_index, make_empty_grids_dict, process_routes
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
    print card.time_sequence
    max_ratio = 0.0
    max_vehicle = None
    for vehicle in cand_vehicles:
        match_num = 0
        locations = vehicle.get_locations_at_timestamps(card.get_time_sequence)
        for location in locations:
            if location == None:
                continue
            gid = grid_index(location)
            for route_no in route_nos:
                if grids[gid[0]][gid[1]].has_key(route_no):
                    match_num += 1
                    break
            
        ratio = match_num / float(len(card))
        if ratio > max_ratio:
            max_ratio = ratio
            max_vehicle = vehicle
    return max_ratio, max_vehicle


if __name__ == "__main__":
    cards = read_cards(database, card_query_tuple)
    print "Finished PART1"
    mapper = Mapper(map_file)
    print "Finished PART2"
    routes = read_routes(lines_file)
    print "Finished PART3"
    vehicles = read_vehicles(database, query_no)
    print "Finished PART4"
    
    grids = make_empty_grids_dict()
    process_routes(routes, grids)
    conn = pickle.load(open(connector_file, 'rb'))
    
    for card in cards:
        print card.get_no()
        match_card_from_vehicles(card, mapper, conn, routes, grids, vehicles)




