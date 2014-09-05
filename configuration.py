# -*- coding: utf-8 -*-
"""
Created on Sat Jun 07 16:31:20 2014

@author: Yunsheng Wei
"""

"""
This file serves as the configuration file.
Modify this file to change some constants.
"""

import os

# database should have index on Sim
database = os.path.normpath("../data/Route_Matching.db")

# vehicles_file
# first line should give name of columns
vehicles_file = os.path.normpath("../data/gps-2014-3-26.txt")

# map_file
# skip first line
map_file = os.path.normpath("../data/stat-line-map.txt")

# cards_file
# Do NOT need to skip the first line!
cards_file = os.path.normpath("../data/data.txt")

# format of lines_file
# longitude should be before latitude!
lines_file =  os.path.normpath("../data/lines.csv")
# skip the first line of lines_file?
skip_first_line = True

# matchers_file
matchers_file = os.path.normpath("../data/matchers.dat")

# "all" or [no_1, no_2]
query_no = "all"

# "all" or [(posid, statid), (posid, statid)]
card_query_tuple = "all"

############################################
# Deprecated
# minimum longitude used in grid
min_long = 121.0
# maximum longitude used in grid
max_long = 122.0
# minimum latitude used in grid
min_lati = 30.7
# maximum latitude used in grid
max_lati = 32.0
############################################

# grid length of longitude
grid_len_long = 0.004
# grid length of latitude
grid_len_lati = 0.004
# threshold of match used in filter_by_grids
match_thres = 0.9
# threshold of match used in subset_match
match_thres_one = 0.9
# distance of match
match_dist = 0.01
# number of grids in neighborhood
around_grid = 1
# intervals between split points for one route (included)
split_pts_int = 10
# time length used to help decide whether vehicle is at stop (measured in seconds)
stop_time = 60
# time used to split card time (measured in seconds)
between_card_time = 60
# width for time grid
time_grid_width = 20


debug_mode = False
verbose = True

