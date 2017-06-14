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

from aipython.utilities import Displayable, cspToJson


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
        (self.graphJSON, self.domainMap, self.linkMap) = cspToJson(csp)
        self._desired_level = 4
        self.sleep_time = 0.2

        # If Con_solver is not defined at the time of creation, import the existing one
        try:
            module = importlib.import_module('__main__')
            Con_solver = getattr(module, 'Con_solver')
        except AttributeError:
            module = importlib.import_module('aipython.cspConsistency')
            Con_solver = getattr(module, 'Con_solver')

        self._con_solver = Con_solver(csp)
        self._override_con_solver(Con_solver)

        self._block_for_user_input = threading.Event()
        self._thread = threading.Thread(target=self._con_solver.make_arc_consistent)
        self._thread.start()
        self._selected_arc = None
        self._user_selected_arc = False

        def step(btn):
            self._user_selected_arc = False
            self._desired_level = 2
            self._block_for_user_input.set()
            self._block_for_user_input.clear()

        def fine_step(btn):
            self._user_selected_arc = False
            self._desired_level = 4
            self._block_for_user_input.set()
            self._block_for_user_input.clear()

        def auto_arc(btn):
            self._thread = threading.Thread(target=self._con_solver.make_arc_consistent)
            self._thread.start()
            self._user_selected_arc = False
            self._desired_level = 1
            self._block_for_user_input.set()
            self._block_for_user_input.clear()

        def auto_solve(btn):
            self._thread = threading.Thread(target=self._con_solver.solve_one)
            self._thread.start()
            self._user_selected_arc = False
            self._desired_level = 1
            self._block_for_user_input.set()
            self._block_for_user_input.clear()

        fine_step_btn = widgets.Button(description='Fine Step')
        fine_step_btn.on_click(fine_step)
        step_btn = widgets.Button(description='Step')
        step_btn.on_click(step)
        auto_arc_btn = widgets.Button(description='Auto Arc Consistency')
        auto_arc_btn.on_click(auto_arc)
        auto_solve_btn = widgets.Button(description='Auto Solve')
        auto_solve_btn.on_click(auto_solve)
        
        display(widgets.HBox([fine_step_btn, step_btn, auto_arc_btn, auto_solve_btn]))

    def _override_con_solver(self, Con_solver):
        """Magic that monkey-patches Con_solver to work."""
        def arc_select(self, to_do):
            if self._desired_level == 1:
                return to_do.pop()

            self._block_for_user_input.wait()
            
            if self._user_selected_arc:
                to_do.discard(self._selected_arc)
                return self._selected_arc
            else:
                # User did not select. Return random arc
                return to_do.pop()

        Con_solver.wait_for_arc_selection = partial(arc_select, self)
        Con_solver.display = self.display

        def __getattribute__(self_, attr):
            if attr == 'solve_one':
                method = object.__getattribute__(self_, attr)
                if not method:
                    raise Exception("Method %s not implemented" % attr)
                if type(method) == types.MethodType:
                    for key, val in self_.domains.items():
                        self._send_set_domain_action(key, val)
                return method

            return object.__getattribute__(self_, attr)
        Con_solver.__getattribute__ = __getattribute__

    def _handle_custom_msgs(self, _, content, buffers=None):
        if content.get('event', '') == 'arc:click':
            varChar = content.get('varId')
            const = self._con_solver.csp.constraints[content.get('constId')]
            self._desired_level = 2

            self._selected_arc = (varChar, const)
            self._user_selected_arc = True
            self._block_for_user_input.set()
            self._block_for_user_input.clear()
    
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
        else:
            sleep(self.sleep_time)

    def _send_highlight_action(self, var, const, style='normal', colour=None):
        self.send({'action': 'highlightArc', 'arcId': self.linkMap[(var, const)], 
                    'style': style, 'colour': colour})

    def _send_set_domain_action(self, var, domain):
        self.send({'action': 'setDomain', 'nodeId': self.domainMap[var], 'domain': list(domain)})