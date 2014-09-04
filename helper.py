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

from math import sqrt

def dist(p1, p2):
    """
    calculate euclidian distance between p1 and p2
    """
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
