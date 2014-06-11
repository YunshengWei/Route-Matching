# -*- coding: utf-8 -*-
"""
Created on Mon Jun 09 23:13:12 2014

@author: Yunsheng Wei
"""

import matplotlib.pyplot as plt
from math import ceil

class Matcher:
    
    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.mlist = []        
        
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
    