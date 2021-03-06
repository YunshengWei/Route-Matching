# -*- coding: utf-8 -*-
"""
Created on Thu Sep 04 13:01:52 2014

@author: WEIYUNSHENG
"""

import configuration

class Mapper:
    
    def __init__(self, map_file):
        """
        initialize Mapper from map_file
        """
        self.statid2lineid = {}
        self.lineid2statid = {}
        with open(map_file, 'r') as reader:
            reader.readline()
            for line in reader:
                line = line.strip()
                if not line:
                    continue
                tjrlstatid, busline_id = line.split(',')
                tjrlstatid = tjrlstatid.strip()
                busline_id = map(lambda x: x.strip(), filter(None, busline_id.split('|')))
                self.statid2lineid.setdefault(tjrlstatid, set())
                self.statid2lineid[tjrlstatid] |= set(busline_id)
                for bid in busline_id:
                    self.lineid2statid.setdefault(bid, set())
                    self.lineid2statid[bid].add(tjrlstatid)
        
    def get_lineid_from_statid(self, statid):
        return self.statid2lineid.get(statid, set())
        
    def get_statid_from_lineid(self, lineid):
        return self.lineid2statid.get(lineid, set())
    
    def all_lineids(self):
        return self.lineid2statid.keys()
    
    def all_statids(self):
        return self.statid2lineid.keys()
        
    def has_lineid(self, lineid):
        return self.lineid2statid.has_key(lineid)
    
    def has_statid(self, statid):
        return self.statid2lineid.has_key(statid)
    
# unit test
if __name__ == "__main__":
    mapper = Mapper(configuration.map_file)
    print sorted(mapper.all_lineids(), key = lambda x: int(x))
#    print mapper.all_statids()