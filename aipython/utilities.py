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
import importlib
import multiprocessing
import threading
import types
from functools import partial
from time import sleep

import ipywidgets as widgets
from IPython.display import display
from ipywidgets import CallbackDispatcher, DOMWidget, Output, register
from traitlets import Dict, Float, Integer, Unicode, observe

class threadWR(threading.Thread):
    """threadWR is a thread extended to allow a return value.
    To get the return value, use this thread as normal, but assign it to a variable on creation.
    calling var.join() will return the return value.
    the return value can also be gotten directly via ._return, but this is not safe.
    """
    def __init__(self, *args, **kwargs):
        super(threadWR, self).__init__(*args, **kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args, **kwargs):
        super(threadWR, self).join(*args, **kwargs)
        return self._return


@register('aispace.CSPViewer')
class Displayable(DOMWidget):
    max_display_level = 4
    sleep_time = 0.2

    _view_name = Unicode('CSPViewer').tag(sync=True)
    _model_name = Unicode('CSPViewerModel').tag(sync=True)
    _view_module = Unicode('aispace').tag(sync=True)
    _model_module = Unicode('aispace').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)
    
    graphJSON = Dict().tag(sync=True)
    line_width = Float(2.0).tag(sync=True)

    def __init__(self, csp):
        super().__init__()
        self.on_msg(self._handle_custom_msgs)
        (self.graphJSON, self.domainMap, self.linkMap) = cspToJson(csp)
        self.visualizer = self
        self._desired_level = 4
        self.sleep_time = 0.2
        self.displayed_once = False

        # If Con_solver is not defined at the time of creation, import the existing one
        try:
            module = importlib.import_module('__main__')
            Con_solver = getattr(module, 'Con_solver')
        except AttributeError:
            module = importlib.import_module('aipython.cspConsistency')
            Con_solver = getattr(module, 'Con_solver')

        self._domains = csp.domains.copy()
        self._block_for_user_input = threading.Event()

        self._selected_arc = None
        self._user_selected_arc = False

        self._initialize_controls()

    def wait_for_arc_selection(self, to_do):
        # Running in Auto mode. Don't block!
        if self._desired_level == 1:
            return to_do.pop()

        self._block_for_user_input.wait()
        
        if self._user_selected_arc:
            to_do.discard(self._selected_arc)
            return self._selected_arc
        else:
            # User did not select. Return random arc.
            return to_do.pop()

    def _initialize_controls(self):
        def advance_visualization(desired_level):
            def advance():
                self._user_selected_arc = False
                self._desired_level = desired_level
                self._block_for_user_input.set()
                self._block_for_user_input.clear()

            return advance

        advance_visualization1 = advance_visualization(1)

        def auto_step():
            advance_visualization1()
            
            if not self._thread.is_alive():
                retValue = self._thread._return
                if type(retValue) is not list:
                    retValue = [retValue]
                self.send({'action': 'output', 
                    'result': f"There are no more solutions. Solution(s) found: {', '.join(str(x) for x in retValue)}"})
        
        self._controls = {
            'fine-step': advance_visualization(4),
            'step': advance_visualization(2),
            'auto-step': auto_step
        }

    def _handle_custom_msgs(self, _, content, buffers=None):
        event = content.get('event', '')

        if event == 'arc:click':
            varChar = content.get('varId')
            const = self.csp.constraints[content.get('constId')]
            self._desired_level = 2

            self._selected_arc = (varChar, const)
            self._user_selected_arc = True
            self._block_for_user_input.set()
            self._block_for_user_input.clear()
        elif event == 'fine-step:click':
            self._controls['fine-step']()
        elif event == 'step:click':
            self._controls['step']()
        elif event == 'auto-step:click':
            self._controls['auto-step']()
        elif event == 'initial_render':
            tasks = getattr(self, '__tasks', [])
            if len(tasks) > 0:
                task = tasks.pop()
                func = task['func']
                args = task['args']
                kwargs = task['kwargs']
                self.displayed_once = True
                self.send({ 'action': 'begin_func' })
                self._thread = threadWR(target=func, args=args, kwargs=kwargs)
                self._thread.start()
    
    def display(self, level, *args, **kwargs):
        """print the arguments if level is less than or equal to the
        current max_display_level.
        level is an integer.
        the other arguments are whatever arguments print can take.
        """
        shouldWait = True
        if args[0] == 'Domain pruned':
            variable = args[2]
            domain = args[4]
            constraint = args[6]
            self._send_set_domain_action(variable, domain)

        if args[0] == "Processing arc (":
            variable = args[1]
            constraint = args[3]
            self._send_highlight_action(variable, constraint, style='bold', colour=None)
            
        if args[0] == 'Domain pruned':
            variable = args[2]
            constraint = args[6]
            self._send_highlight_action(variable, constraint, style='bold', colour='green')
            
        if args[0] == "Arc: (" and args[4] == ") is inconsistent":
            variable = args[1]
            constraint = args[3]
            self._send_highlight_action(variable, constraint, style='bold', colour='red')
            
        if args[0] == "Arc: (" and args[4] == ") now consistent":
            variable = args[1]
            constraint = args[3]
            self._send_highlight_action(variable, constraint, style='normal', colour='green')
            shouldWait = False
        
        if args[0] == "  adding" and args[2] == "to to_do.":
            if args[1] != "nothing":
                arcList = list(args[1])
                for arc in arcList:
                    self._send_highlight_action(arc[0], arc[1], style='normal', colour='blue')
        
        text = ' '.join(map(str, args))
        self.send({'action': 'output', 'result': text})

        if level <= self._desired_level:
            if shouldWait:
                self._block_for_user_input.wait()
        elif args[0] == "solution:":
            self._block_for_user_input.wait()
        else:
            sleep(self.sleep_time)

    def _send_highlight_action(self, var, const, style='normal', colour=None):
        self.send({'action': 'highlightArc', 'arcId': self.linkMap[(var, const)], 
                    'style': style, 'colour': colour})

    def _send_set_domain_action(self, var, domain):
        self.send({'action': 'setDomain', 'nodeId': self.domainMap[var], 'domain': list(domain)})

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


def delay_until_render(func_to_delay):
    def wrapper(self, *args, **vargs):
        if self.displayed_once is False:
            tasks = getattr(self, '__tasks', [])
            self.__tasks = tasks
            self.__tasks.append({'func': partial(func_to_delay, self), 'args': args, 'kwargs': vargs})
        else:
            return func_to_delay(self, *args, **vargs)
    
    return wrapper
    
if __name__ == "__main__":
    test()

