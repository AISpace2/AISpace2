# utilities.py - AIFCA utilities
# AIFCA Python3 code Version 0.7. Documentation at http://artint.info/code/python/

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from ipywidgets import Widget, CallbackDispatcher, register
from traitlets import Unicode, observe
from time import sleep
import random
import uuid
import threading

@register('aispace.Displayable')
class Displayable(Widget):
    """"""
    _model_name = Unicode('DisplayModel').tag(sync=True)
    _model_module = Unicode('aispace').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)
    max_display_level = 4
    sleep_time = 0.2

    def display(self,level,*args,**kwargs):
        """print the arguments if level is less than or equal to the
        current max_display_level.
        level is an integer.
        the other arguments are whatever arguments print can take.
        """
        if level <= self.max_display_level:
            text = ' '.join(map(str, args))
            self.send({'action': 'output', 'result': text, 'process_id': threading.current_thread().ident })
            pass #print(*args)  ##if error you are using Python2 not Python3

        if args[0] == 'Domain pruned':
            nodeName = args[2]
            domain = args[4]
            consName = args[6]
            self.send({'action': 'setDomain', 'nodeName': nodeName, 'domain': domain, 'process_id': threading.current_thread().ident})
                   # setDomain(nodeName, elementValue)

        if args[0] == "Processing arc (":
            varName = args[1]
            consName = args[3]
            self.send({'action': 'highlightArc', 'varName': varName,
                'consName': consName.__repr__(), 'style': 'bold',
                'colour': 'na', 'process_id': threading.current_thread().ident})
            for i in range(len(self.csp.constraints)):
                if self.csp.constraints[i] == consName:
                    self.send({'action': 'highlightArc', 'varName': varName,
                'consName': consName.__repr__(), 'style': 'bold',
                'colour': 'na', 'process_id': threading.current_thread().ident})
            # highlightArc(varName, consName.__repr__(), "bold","na")
            
        if args[0] == 'Domain pruned':
            varName = args[2]
            consName = args[6]
            self.send({'action': 'highlightArc', 'varName': varName,
                'consName': consName.__repr__(), 'style': 'bold',
                'colour': 'green', 'process_id': threading.current_thread().ident})
            # highlightArc(varName, consName.__repr__(), "bold","green")
            
        if args[0] == "Arc: (" and args[4] == ") is inconsistent":
            varName = args[1]
            consName = args[3]
            self.send({'action': 'highlightArc', 'varName': varName,
                'consName': consName.__repr__(), 'style': 'bold',
                'colour': 'red', 'process_id': threading.current_thread().ident})
            # highlightArc(varName, consName.__repr__(), "bold","red")
            
        if args[0] == "Arc: (" and args[4] == ") now consistent":
            varName = args[1]
            consName = args[3]
            self.send({'action': 'highlightArc', 'varName': varName,
                'consName': consName.__repr__(), 'style': '!bold',
                'colour': 'green', 'process_id': threading.current_thread().ident})
            # highlightArc(varName, consName.__repr__(), "!bold","green")
        
        if args[0] == "  adding" and args[2] == "to to_do.":
            if args[1] != "nothing":
                arcList = list(args[1])
                for i in range(len(arcList)):
                    self.send({'action': 'highlightArc', 'varName': arcList[i][0],
                'consName': arcList[i][1].__repr__(), 'style': '!bold',
                'colour': 'blue', 'process_id': threading.current_thread().ident})
        sleep(self.sleep_time)

    def wait_for_arc_selection(self, arcs):
        pass
        
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
def cspToJson(cspObject):
    """Converts a CSP to a JSON representation."""
    cspJSON = {'nodes': [],
                 'links': []}

    # Maps variables to their IDs
    domainMap = {var: str(uuid.uuid4()) for var in cspObject.domains}

    # Maps (variable, constraint) to their corresponding arc IDs
    linkMap = dict()

    for i, (var, value) in enumerate(cspObject.domains.items()):
        cspJSON['nodes'].append({'id': domainMap[var], 'name': var, 'type': 'csp:variable', 'idx': i, 'domain': list(value)})

    for (i, cons) in enumerate(cspObject.constraints):
        consId = str(uuid.uuid4())
        cspJSON['nodes'].append({'id': consId, 'name': cons.__repr__(), 'type': 'csp:constraint', 'idx': i})

        link1Id = str(uuid.uuid4())
        link1 = {'id': link1Id, 'source': domainMap[cons.scope[0]], 'target': consId}

        cspJSON['links'].append(link1)
        linkMap[(cons.scope[0], cons)] = link1Id

        if len(cons.scope) == 2:
            consId2 = str(uuid.uuid4())
            link2Id = str(uuid.uuid4())
            link2 = {'id': link2Id, 'source': domainMap[cons.scope[1]], 'target': consId}

            cspJSON['links'].append(link2)
            linkMap[(cons.scope[1], cons)] = link2Id
    
    return (cspJSON, domainMap, linkMap)
    
if __name__ == "__main__":
    test()

