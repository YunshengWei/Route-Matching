# -*- coding: utf-8 -*-
"""
Created on Sat Jun 07 16:27:47 2014

@author: Yunsheng Wei
"""

class Vehicle:
    
    def __init__(self, vlist, vehicle_no):
        """
        vehicle_no should be int
        """
        self.vehicle_no = vehicle_no
        self.vlist = vlist
        
    def __len__(self):
        return len(self.vlist)

    def get_no(self):
        return self.vehicle_no

    def get_data(self, i):
        return self.vlist[i]
    
    def get_location(self, i):
        """
        return as (longitude, latitude)
        """
        return (self.get_longitude(i), self.get_latitude(i))
    
    def get_latitude(self, i):
        return self.vlist[i][1]
    
    def get_longitude(self, i):
        return self.vlist[i][2]
        
    def get_id(self, i):
        return self.vlist[i][0]
    
    def get_GpsTime(self, i):
        return self.vlist[i][3]
    
    def __iter__(self):
        return iter(self.vlist)

class Vehicles:
    
    def __init__(self):
        self.vehicles = {}
    
    def add(self, vehicle):
        self.vehicles[vehicle.get_no()] = vehicle
    
    def get_vehicle(self, no):
        return self.vehicles[no]
    
    def get_vehicle_len(self, no):
        return len(self.vehicles[no])
        
    def all_vehicles_no(self):
        return self.vehicles.keys()
        
    def __iter__(self):
        return self.vehicles.itervalues()
        
    def __len__(self):
        return len(self.vehicles)