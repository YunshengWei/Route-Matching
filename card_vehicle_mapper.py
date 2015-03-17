# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 15:29:53 2015

@author: WEIYUNSHENG
"""

class CardVehicleMapper:
    """
    Used to record the result of matching cards to vehicles
    """
    
    def __init__(self):
        self.mapper = dict()
    
    def add_map(self, tup, vehicle_no, offset):
        """
        tup is (posid, statid)
        """
        self.mapper[tup] = (vehicle_no, offset)
    
    def lookup(self, tup):
        return self.mapper.get(tup)
    