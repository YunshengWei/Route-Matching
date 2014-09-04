# -*- coding: utf-8 -*-
"""
Created on Wed Sep 03 20:28:56 2014

@author: Yunsheng Wei
"""

from __future__ import division
from math import ceil

from configuration import time_grid_width

def time_seqs_match(ts, ts_list, interval_width):
    """
    Given a time sequence, find the best match from a list of time sequences.
    ts is pos machine data.
    ts_list is vehicle stop data.
    ts_list should not be empty.
    @ return: (index, ratio)
    """
    ratios = []
    time_grid = set()
    for timestamp in ts:
        grid_index = int(ceil(timestamp / time_grid_width))
        time_grid.add(grid_index)
    for cand_ts in ts_list:
        cand_grid = set()
        for timestamp in cand_ts:
            grid_index = int(ceil(timestamp / time_grid_width))
            cand_grid.add(grid_index)
            cand_grid.add(grid_index - 1)
            cand_grid.add(grid_index + 1)
        ratios.append(len(cand_grid & time_grid) / len(time_grid))
    index = max(xrange(len(ratios)), key = lambda x: ratios[x])
    return (index, ratios[index])
    