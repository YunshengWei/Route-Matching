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
database = os.path.normpath("../data_2015-01-27/Route_Matching.db")

# vehicles_file
# first line should give name of columns
vehicles_file = os.path.normpath("../data_2015-01-27/gps-2014-3-26-convert.txt")

# map_file
# skip first line
map_file = os.path.normpath("../data_2015-01-27/stat-line-map.txt")

# cards_file
# Do NOT need to skip the first line!
cards_file = os.path.normpath("../data_2015-01-27/data.txt")

# format of lines_file
# longitude should be before latitude!
# Skip the first line!
lines_file =  os.path.normpath("../data_2015-01-27/busline-2014.csv")
lines_file_supplement = os.path.normpath("../data_2015-01-27/BusLinePoint-2014.csv")

# connector_file
connector_file = os.path.normpath("../data_2015-01-27/connector.dat")

# "all" or [no_1, no_2]
query_no = ["B36281"]
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
match_thres_one = 0.85
# distance of match
match_dist = 0.002
# number of grids in neighborhood
around_grid = 1
# intervals between split points for one route (included)
split_pts_int = 10
# time length used to help decide whether vehicle is at stop (measured in seconds)
stop_time = 60
# time used to split card time (measured in seconds)
between_card_time = 40
# outlier distance threshold
outlier_dist_thres = 0.1
# distance between card time
dist_card_time = 0.001
# distance from stop when swiping cards
dist_stop = 0.002
# max time offset (measured in seconds)
max_time_offset = 300
# offset step
offset_step = 20
offsets = [-max_time_offset + offset_step * i 
           for i in xrange(int(2*max_time_offset/offset_step + 1))]
# ratio #1 > #2
thres_ratio = 0.1
# min_ratio
min_ratio = 0.7

debug_mode = False
verbose = True

