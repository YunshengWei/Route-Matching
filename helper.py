# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 21:30:10 2014

@author: LeBronJames
"""

"""
Thie module defines some useful helper functions
used by more than one modules
to avoid circular imports.
"""

from math import sqrt, ceil
from collections import defaultdict

from configuration import min_long, grid_len_long, \
min_lati, grid_len_lati, around_grid

def dist(p1, p2):
    """
    calculate euclidian distance between p1 and p2
    """
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    
def grid_index(p):
    """
    p[0] is longitude, p[1] is latitude
    """
    return (int(ceil((p[0] - min_long) / float(grid_len_long))), 
            int(ceil((p[1] - min_lati) / float(grid_len_lati))))
            
def make_empty_grids_dict():
    """
    make empty grids using defaultdict as
    underlying data structure instead of list.
    This function is more robust than make_empty_grids, 
    and does not assume ranges of longitude and latitude.
    """
    grids = defaultdict(lambda : defaultdict(dict))
    return grids

def process_routes(routes, grid):
    """
    put routes in corresponding grids
    """
    for route in routes:
        route_no = route.get_no()
        for i, site in enumerate(route):      
            idx, idy = grid_index(site)
            for longi, lati in neighbor_id(idx, idy):
                grid[longi][lati].setdefault(route_no, set())
                grid[longi][lati][route_no].add(i)

def neighbor_id(id_x, id_y):
    """
    return neighborhood location of (id_x, id_y),
    i.e.  [id_x - around_gird, id_x + around_gird] 
        * [id_y - around_grid, id_y + around_grid]
    """
    for i in xrange(-around_grid + id_x, around_grid + id_x + 1):
        for j in xrange(-around_grid + id_y, around_grid + id_y + 1):
            yield (i, j)            

def weighted_location(time, location1, location2, time1, time2):
    """
    return location at time t.
    time must be (time1, time2)
    """
    l0 = (location2[0] - location1[0]) / float(time2 - time1) + location1[0]
    l1 = (location2[1] - location1[1]) / float(time2 - time1) + location1[1]
    return (l0, l1)
    
def binary_search(ele, l, key = lambda x: x):
    """
    binary search ele in a list l,
    return ('found', index) (if hit) (if many hits, return only one)
    or ('interval', (index1, index2))
    or ('head', 0)
    or ('end', len(l)-1)
    or None if l is empty
    """
    if not l:
        return None
    if key(l[0]) > ele:
        return ('head', 0)
    if key(l[-1]) < ele:
        return ('end', len(l) - 1)
    start = 0
    end = len(l) - 1
    while end >= start:
        pivot = int(ceil((start + end) / 2.0))
        if key(l[pivot]) == ele:
            return ('found', pivot)
        elif key(l[pivot]) > ele:
            end = pivot - 1
        else:
            start = pivot + 1
    return ('interval', (end, start))
    
    
    
    