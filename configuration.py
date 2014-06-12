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

# format of lines_file
# longitude should be before latitude!
lines_file =  os.path.normpath("../data/lines.csv")
# skip the first line of lines_file?
skip_first_line = True

# "all" or [no_1, no_2]
query_no = [15711695761]
# minimum longitude used in grid
min_long = 121.0
# maximum longitude used in grid
max_long = 122.0
# minimum latitude used in grid
min_lati = 30.7
# maximum latitude used in grid
max_lati = 32.0
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

debug_mode = False
verbose = True

