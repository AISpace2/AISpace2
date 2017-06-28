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

from aipython.utilities import Displayable
from .cspjsonbridge import csp_to_json

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
class CSPViewer(DOMWidget):
    """Visualize and interact with a CSP."""
    _view_name = Unicode('CSPViewer').tag(sync=True)
    _model_name = Unicode('CSPViewerModel').tag(sync=True)
    _view_module = Unicode('aispace').tag(sync=True)
    _model_module = Unicode('aispace').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)
    
    graphJSON = Dict().tag(sync=True)
    line_width = Float(2.0).tag(sync=True)

    def __init__(self, csp):
        super(CSPViewer, self).__init__()

        self.on_msg(self._handle_custom_msgs)
        (self.graphJSON, self.domainMap, self.linkMap) = csp_to_json(csp)
        self._desired_level = 4
        self.sleep_time = 0.2

        # If Con_solver is not defined at the time of creation, import the existing one
        try:
            module = importlib.import_module('__main__')
            Con_solver = getattr(module, 'Con_solver')
        except AttributeError:
            module = importlib.import_module('aipython.cspConsistency')
            Con_solver = getattr(module, 'Con_solver')

        self._con_solver = Con_solver(csp, visualizer=self)

        self._domains = csp.domains.copy()
        self._block_for_user_input = threading.Event()
        self._thread = threadWR(target=self._con_solver.make_arc_consistent, args=(self._domains,))
        self._thread.start()
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

        def auto_arc():
            self._thread = threadWR(target=self._con_solver.make_arc_consistent, args=(self._domains,))
            self._thread.start()
            advance_visualization1()

        def auto_solve():
            self._thread = threadWR(target=self._con_solver.solve_one, args=(self._domains,))
            self._thread.start()
            advance_visualization1()

        def backtrack():
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
            'auto-ac': auto_arc,
            'auto-solve': auto_solve,
            'backtrack': backtrack
        }

    def _handle_custom_msgs(self, _, content, buffers=None):
        event = content.get('event', '')

        if event == 'arc:click':
            varChar = content.get('varId')
            const = self._con_solver.csp.constraints[content.get('constId')]
            self._desired_level = 2

            self._selected_arc = (varChar, const)
            self._user_selected_arc = True
            self._block_for_user_input.set()
            self._block_for_user_input.clear()
        elif event == 'fine-step:click':
            self._controls['fine-step']()
        elif event == 'step:click':
            self._controls['step']()
        elif event == 'auto-ac:click':
            self._controls['auto-ac']()
        elif event == 'auto-solve:click':
            self._controls['auto-solve']()
        elif event == 'backtrack:click':
            self._controls['backtrack']()
    
    def display(self, level, *args, **kwargs):
        """print the arguments if level is less than or equal to the
        current max_display_level.
        level is an integer.
        the other arguments are whatever arguments print can take.
        """
        shouldWait = True

        if args[0] == 'Performing AC with domains':
            domains = args[1]
            for var, domain in domains.items():
                self._send_set_domain_action(var, domain)

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