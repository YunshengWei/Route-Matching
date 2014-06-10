# -*- coding: utf-8 -*-
"""
Created on Mon Jun 09 23:13:12 2014

@author: Yunsheng Wei
"""

class Matcher:
    
    def __init__(self, vehicle_no):
        self.vehicle_no = vehicle_no
        self.mlist = []        
        
    def append(self, start, end, route_no):
        self.mlist.append((start, end, route_no))
        
    def insert(self, index, start, end, route_no):
        self.mlist.insert(index, (start, end, route_no))
        
    def __len__(self):
        return len(self.mlist)
        
    def __str__(self):
        return '\n'.join(["vehicle : %s" % self.vehicle_no] \
                       + ["%-6s -- %6s : %s" % (start, end, route_no) 
                          for start, end, route_no in self.mlist])
                              
    