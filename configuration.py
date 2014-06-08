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
lines_file =  os.path.normpath("../data/lines.csv")
# "all" or [no_1, no_2]
query_no = "all"
min_long = 121.1
max_long = 121.9
min_lati = 31.1
max_lati = 31.5
grid_len_long = 0.004
grid_len_lati = 0.004

match_thres = 0.9
match_thres_one = 0.9
match_dist = 0.01
around_grid = 1
debug_mode = False