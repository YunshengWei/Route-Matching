# -*- coding: utf-8 -*-
"""
Created on Sat Jun 07 16:30:50 2014

@author: Yunsheng Wei
"""

import matplotlib.pyplot as plt
from helper import dist

class Route:
    
    def __init__(self, route_no, sites):
        """
        route_no should be int
        """
        self.route_no = route_no
        self.sites = sites
        self.total_len = None

    def get_no(self):
        return self.route_no
    
    def get_location(self, i):
        """
        return as (longitude, latitude)
        """
        return (self.get_longitude(i), self.get_latitude(i))
    
    def get_latitude(self, i):
        return self.sites[i][1]
        
    def get_longitude(self, i):
        return self.sites[i][0]
        
    def get_dest_loc(self):
        return self.get_location(-1)
    
    def get_start_loc(self):
        return self.get_location(0)
        
    def __len__(self):
        """
        count of sites
        """
        return len(self.sites)
        
    def __iter__(self):
        return iter(self.sites)

    def plot(self, start, end, *args1, **args2):
        """
        plot route data on a 2d plane on current figure.
        [start, end)
        """    
        x, y = zip(*[self.get_location(i) for i in xrange(start, end)]) 
        plt.plot(x, y, *args1, **args2)
        
    def length(self):
        """
        total distance between adjacent sites,
        use lines to link adjacent sites.
        """
        if self.total_len == None:
            self.total_len = 0
            for i in xrange(1, len(self)):
                self.total_len += dist(self.get_location(i), self.get_location(i - 1))
        return self.total_len

class Routes:
    def __init__(self):
        self.routes = {}
        
    def get_route_len(self, i):
        return len(self.routes[i])
    
    def add(self, route):
        self.routes[route.get_no()] = route
        
    def get_route(self, no):
        return self.routes[no]
        
    def all_routes_no(self):
        return self.routes.keys()
    
    def __len__(self):
        return len(self.routes)
        
    def __iter__(self):
        return self.routes.itervalues()