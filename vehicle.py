# -*- coding: utf-8 -*-
"""
Created on Sat Jun 07 16:27:47 2014

@author: Yunsheng Wei
"""

import matplotlib.pyplot as plt
from helper import weighted_location, dist
from configuration import outlier_dist_thres
from helper import binary_search, weighted_location

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
    
    def denoise(self):
        """
        return a new vehicle with outlier removed
        """
#        if len(self.vlist) < 3:
#            return self
#        new_vlist = [self.vlist[0]]
#        for i in xrange(1, len(self.vlist) - 1):
#            if dist(self.get_location(i), self.get_location(i-1)) > outlier_dist_thres \
#            and dist(self.get_location(i), self.get_location(i+1)) > outlier_dist_thres:
#                print ("remove outlier in %s" % self.get_no()), self.get_location(i-1), \
#                self.get_location(i), self.get_location(i+1)
#                continue
#            new_vlist.append(self.vlist[i])
#        new_vlist.append(self.vlist[-1])
        
        # Assume self.vlist[0] is not outlier and time is continuous.
        if not self.vlist:
            return self
        new_vlist = [self.vlist[0]]
        for i in xrange(1, len(self.vlist)):
            if dist(self.get_location(i), (new_vlist[-1][2], new_vlist[-1][1])) < outlier_dist_thres:
                new_vlist.append(self.vlist[i])
        return Vehicle(new_vlist, self.get_no())
        
    def plot(self, start, end, *args1, **args2):
        """
        plot vehicle data on a 2d plane on current figure.
        [start, end)
        """    
        x, y = zip(*[self.get_location(i) for i in xrange(start, end)]) 
        plt.plot(x, y, *args1, **args2)
        
    def plot_points(self, list_of_indices, *args1, **args2):
        """
        plot vehicle data on a 2d plane on current figure.
        """
        x, y = zip(*[self.get_location(i) for i in list_of_indices])
        plt.plot(x, y, *args1, **args2)
        
    def get_location_at_timestamp(self, ts):
        """
        get the location of the vehicle at time nearest to ts.
        location as (longitude, latitude)
        use binary search
        """
        if not self.vlist:
            return None
        result = binary_search(ts, self.vlist, key = lambda x: x[3])
        if result[0] == 'found':
            return self.get_location(result[1])
        if result[0] == 'interval':
            return weighted_location(ts, self.get_location(result[1][0]),\
            self.get_location(result[1][1]), self.get_GpsTime(result[1][0]), \
            self.get_GpsTime(result[1][1]))
        return self.get_location(result[1])
        
    def get_locations_at_timestamps(self, times):
        """
        get locations at times.
        times should be ascended order.
        location as (longitude, latitude)
        """
        return [self.get_location_at_timestamp(time)
                for time in times]
    
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