# utilities.py - AIFCA utilities
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from time import sleep
import random
import uuid

class Displayable(object):
    max_display_level = 4
    sleep_time = 0.2

    def display(self,level,*args,**kwargs):
        """print the arguments if level is less than or equal to the
        current max_display_level.
        level is an integer.
        the other arguments are whatever arguments print can take.
        """

        if getattr(self, 'visualizer', None) is not None:
            self.visualizer.display(level, *args, **kwargs)
        else:
            if level <= self.max_display_level:
                print(*args)

def argmax(gen):
    """gen is a generator of (element,value) pairs, where value is a real.
    argmax returns an element with maximal value.
    If there are multiple elements with the max value, one is returned at random.
    """
    maxv = float('-Infinity')       # negative infinity
    maxvals = []      # list of maximal elements
    for (e,v) in gen:
        if v>maxv:
            maxvals,maxv = [e], v
        elif v==maxv:
            maxvals.append(e)
    return random.choice(maxvals)

# Try:
# argmax(enumerate([1,6,3,77,3,55,23]))

def flip(prob):
    """return true with probability prob"""
    return random.random() < prob

def dict_union(d1,d2):
    """returns a dictionary that contains the keys of d1 and d2.
    The value for each key that is in d2 is the value from d2,
    otherwise it is the value from d1.
    This does not have side effects.
    """
    d = dict(d1)    # copy d1
    d.update(d2)
    return d

def test():
    """Test part of utilities"""
    assert argmax(enumerate([1,6,55,3,55,23])) in [2,4]
    assert dict_union({1:4, 2:5, 3:4},{5:7, 2:9}) == {1:4, 2:9, 3:4, 5:7} 
    print("Passed unit test in utilities")

import json

def cspToJSON(csp):
    cspJSON = {'nodes': {}, 'edges': {}}

    # Maps variables to their IDs
    domainMap = {var: str(uuid.uuid4()) for var in csp.domains}

    # Maps (variable, constraint) to their corresponding arc IDs
    linkMap = dict()

    for i, (var, value) in enumerate(csp.domains.items()):
        cspJSON['nodes'][domainMap[var]] = {'id': domainMap[var], 'name': var, 'type': 'csp:variable', 'idx': i, 'domain': list(value)}


    for (i, cons) in enumerate(csp.constraints):
        consId = str(uuid.uuid4())
        cspJSON['nodes'][consId] = {'id': consId, 'name': cons.__repr__(), 'type': 'csp:constraint', 'idx': i}

        link1Id = str(uuid.uuid4())
        link1 = {'id': link1Id, 'source': domainMap[cons.scope[0]], 'dest': consId}

        cspJSON['edges'][link1Id] = link1
        linkMap[(cons.scope[0], cons)] = link1Id

        if len(cons.scope) == 2:
            consId2 = str(uuid.uuid4())
            link2Id = str(uuid.uuid4())
            link2 = {'id': link2Id, 'source': domainMap[cons.scope[1]], 'dest': consId}

            cspJSON['edges'][link2Id] = link2
            linkMap[(cons.scope[1], cons)] = link2Id
    
    return (cspJSON, domainMap, linkMap)

    
if __name__ == "__main__":
    test()

