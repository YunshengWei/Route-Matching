# -*- coding: utf-8 -*-
"""
Created on Fri Sep 05 11:02:40 2014

@author: WEIYUNSHENG
"""

class Connector:
    """
    This class is used to connect the vehicle and card.    
    """
    
    def __init__(self, matchers):
        """
        matchers is a list of Matcher
        """
        self.connector = {}
        for matcher in matchers:
            vehicle_no = matcher.vehicle.get_no()
            for _, _, route in matcher.mlist:
                self.connector.setdefault(route.get_no(), set())
                if vehicle_no not in self.connector[route.get_no()]:
                    self.connector[route.get_no()].add(vehicle_no)
                    
    def get_cands(self, route_no):
        return self.connector.get(route_no, set())
        
