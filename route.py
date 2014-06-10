# -*- coding: utf-8 -*-
"""
Created on Sat Jun 07 16:30:50 2014

@author: Yunsheng Wei
"""

class Route:
    def __init__(self, route_no, sites):
        """
        route_no should be int
        """
        self.route_no = route_no
        self.sites = sites

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
        return len(self.sites)
        
    def __iter__(self):
        return iter(self.sites)

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