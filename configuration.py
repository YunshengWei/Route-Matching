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
query_no = "all"
min_long = 121.0
max_long = 122.0
min_lati = 30.7
max_lati = 32.0
grid_len_long = 0.004
grid_len_lati = 0.004

match_thres = 0.9
match_thres_one = 0.9
match_dist = 0.01
around_grid = 1
# intervals between split points for one route (included)
split_pts_int = 10
debug_mode = False
verbose = True

