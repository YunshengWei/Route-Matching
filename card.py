# -*- coding: utf-8 -*-
"""
Created on Fri Sep 05 10:14:21 2014

@author: WEIYUNSHENG
"""

class Card:
    
    def __init__(self, time_sequence, tup):
        """
        Initialize Card using a list of timestamp
        tup is (posid, statid)
        """
        self.time_sequence = time_sequence
        self.tup = tup
        
    def get_no(self):
        return self.tup
        
    def __len__(self):
        return len(self.time_sequence)
        
    def get_simplified_card(self, time_width):
        """
        According to time_width, return a SimplifiedCard object.
        """
        new_time_sequence = []
        # Should I skip the first timestamp?
        if len(self.time_sequence) > 0:
            new_time_sequence = [self.time_sequence[0]]
        for i in xrange(1, len(self.time_sequence)):
            if self.time_sequence[i] - self.time_sequence[i - 1] >= time_width:
                new_time_sequence.append(self.time_sequence[i])
        return Card(new_time_sequence, self.tup)
        
    def get_time_sequence(self):
        return self.time_sequence
           
class Cards:
    
    def __init__(self):
        self.cards = {}
    
    def add(self, card):
        self.cards[card.get_no()] = card
    
    def get_card(self, no):
        return self.cards[no]
    
    def get_card_len(self, no):
        return len(self.cards[no])
        
    def all_cards_no(self):
        return self.cards.keys()
        
    def __iter__(self):
        return self.cards.itervalues()
        
    def __len__(self):
        return len(self.cards)
