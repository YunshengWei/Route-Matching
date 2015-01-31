# -*- coding: utf-8 -*-
"""
Created on Mon Jun 09 23:13:12 2014

@author: Yunsheng Wei
"""

import matplotlib.pyplot as plt
from math import ceil
from datetime import datetime
from helper import grid_index, dist

class Matcher:
    
    def __init__(self, vehicle, grids):
        self.vehicle = vehicle
        self.mlist = []
        self.grids = grids
        
    def append(self, start, end, route):
        self.insert(len(self.mlist), start, end, route)
        
    def insert(self, index, start, end, route):
        self.mlist.insert(index, (start, end, route))
        
    def __len__(self):
        return len(self.mlist)
        
    def __str__(self):
        return '\n'.join(["vehicle : %s" % self.vehicle.get_no()] \
                       + ["%-6s -- %6s : %s" % (start, end, route.get_no()) 
                          for start, end, route in self.mlist])
                              
    def plot(self):
        """
        plot matcher on a new figure.
        """
        row = ceil(len(self) / 2.0)
        col = 2
        plt.figure()
        for i, (start, end, route) in enumerate(self.mlist, 1):
            plt.subplot(row, col, i)
            self.vehicle.plot(start, end + 1, 'b-')
            route.plot(0, len(route), 'ro')
        plt.show()
    
    def niceprint(self):
        for start, end, route in self.mlist:
            s = ['' for _ in xrange(len(route) + 2)]
            res = vehicle_site_time(self.vehicle, start, end, route, self.grids)
            s[0], s[1] = self.vehicle.get_no(), route.get_no()
            for site_no, time in res:
                s[site_no + 2] = datetime.utcfromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")
            print ','.join(s)
            

def vehicle_site_time(vehicle, start, end, route, grids):
    """
    include start, end
    return [(site_no, time), (site_no, time)]
    """
    times = [None for _ in xrange(len(route))]
    dists = [100000 for _ in xrange(len(route))]
    for i in xrange(start, end + 1):
        loc = vehicle.get_location(i)
        idx, idy = grid_index(loc)
        sites = grids[idx][idy].get(route.get_no(), set())
        for site in sites:
            d = dist(route.get_location(site), vehicle.get_location(i))
            if d <= dists[site]:
                dists[site] = d
                times[site] = vehicle.get_GpsTime(i)
    ret_times = []
    for site, time in enumerate(times):
        if time != None:
            ret_times.append((site, time))
    return ret_times
            
            