# -*- coding: utf-8 -*-
"""
Created on Wed Sep 03 20:28:56 2014

@author: Yunsheng Wei
"""

from __future__ import division
from math import ceil
import sqlite3

import configuration
from card import Card, Cards

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

def match_card_from_vehicles(card, mapper, connector, routes):
    """
    find the best match for the card
    """
    route_nos = mapper.get_lineid_from_statid(card.get_no()[1])
    routes = [routes.get_route(route_no) for route_no in route_nos]
    
    cand_vehicles = []
    for route_no in route_nos:    
        cand_vehicles += connector.get_cands(route_no)
    cand_vehicles_unique = []
    for vehicle in cand_vehicles:
        if vehicle not in cand_vehicles_unique:
            cand_vehicles_unique.append(vehicle)
            
    card = card.get_simplified_card()
    max_ratio = 0
    for vehicle in cand_vehicles_unique:
        match_num = 0
        locations = vehicle.get_locations_at_timestamps(card.get_time_sequence)
        


if __name__ == "__main__":
    cards = read_cards(configuration.database, configuration.card_query_tuple)
    for card in cards:
        print card.get_no(), card.time_sequence
        break




