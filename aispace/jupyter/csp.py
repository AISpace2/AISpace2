import threading
from functools import partial
from time import sleep

from ipywidgets import DOMWidget, register
from traitlets import Dict, Float, Unicode

from aispace.cspjsonbridge import csp_to_json


class ReturnableThread(threading.Thread):
    """A thread extended to allow a return value.
    To get the return value, use this thread as normal, but assign it to a variable on creation.
    calling var.join() will return the return value.
    the return value can also be gotten directly via ._return, but this is not safe.
    """

    def __init__(self, *args, **kwargs):
        super(ReturnableThread, self).__init__(*args, **kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, timeout=None):
        super().join(timeout)
        return self._return


@register('aispace.CSPViewer')
class Displayable(DOMWidget):
    _view_name = Unicode('CSPViewer').tag(sync=True)
    _model_name = Unicode('CSPViewerModel').tag(sync=True)
    _view_module = Unicode('aispace').tag(sync=True)
    _model_module = Unicode('aispace').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)

    graph_json = Dict().tag(sync=True)
    line_width = Float(2.0).tag(sync=True)
    sleep_time = Float(0.2).tag(sync=True)

    def __init__(self):
        super().__init__()
        self.on_msg(self._handle_custom_msgs)
        self.visualizer = self

        self._desired_level = 4
        self._displayed_once = False

        # You MUST wait() on this event only on a background thread!
        self._block_for_user_input = threading.Event()

        self._selected_arc = None
        self._has_user_selected_arc = False

        self._selected_var = None

        self._initialize_controls()
        (self.graph_json, self._domain_map, self._edge_map) = csp_to_json(self.csp)

    def wait_for_arc_selection(self, to_do):
        """Pauses execution until an arc has been selected and returned.

        If the algorithm is running in auto mode, an arc is returned immediately.
        Otherwise, this function blocks until an arc is selected by the user.

        Args:
            to_do (set): A set of arcs to choose from. This set will be modified.

        Returns:
            (string, Constraint):
                A tuple (var_name, constraint) that represents an arc from `to_do`.
        """
        # Running in Auto mode. Don't block!
        if self._desired_level == 1:
            return to_do.pop()

        self._block_for_user_input.wait()

        if self._has_user_selected_arc:
            to_do.discard(self._selected_arc)
            return self._selected_arc

        # User did not select. Return random arc.
        return to_do.pop()

    def wait_for_var_selection(self, iter_var):
        self._block_for_user_input.wait()
        self._desired_level = 4
        if self._selected_var in list(iter_var):
            return self._selected_var
        else:
            self._block_for_user_input.wait()

    def _initialize_controls(self):
        """Sets up functions that can be used to control the visualization."""
        def advance_visualization(desired_level):
            def advance():
                self._has_user_selected_arc = False
                self._desired_level = desired_level
                self._block_for_user_input.set()
                self._block_for_user_input.clear()

                if not self._thread.is_alive():
                    return_value = self._thread.join()
                    if not isinstance(return_value, list):
                        return_value = [return_value]

                    self.send({'action': 'output',
                            'text': 'Algorithm execution finished. Returned: {}'.format(
                                ', '.join(str(x) for x in return_value)
                            )})
            return advance

        self._controls = {
            'fine-step': advance_visualization(4),
            'step': advance_visualization(2),
            'auto-step': advance_visualization(1)
        }

    def _handle_custom_msgs(self, _, content, buffers=None):
        event = content.get('event', '')

        if event == 'arc:click':
            var_name = content.get('varId')
            const = self.csp.constraints[content.get('constId')]
            self._desired_level = 2

            self._selected_arc = (var_name, const)
            self._has_user_selected_arc = True
            self._block_for_user_input.set()
            self._block_for_user_input.clear()
        elif event == 'var:click':
            var_name = content.get('varId')
            self._selected_var = var_name
            self._block_for_user_input.set()
            self._block_for_user_input.clear()
        elif event == 'fine-step:click':
            self._controls['fine-step']()
        elif event == 'step:click':
            self._controls['step']()
        elif event == 'auto-step:click':
            self._controls['auto-step']()
        elif event == 'initial_render':
            queued_func = getattr(self, '_queued_func', None)
            if queued_func:
                func = queued_func['func']
                args = queued_func['args']
                kwargs = queued_func['kwargs']
                self._displayed_once = True
                self.send({'action': 'begin_func'})
                self._thread = ReturnableThread(
                    target=func, args=args, kwargs=kwargs)
                self._thread.start()

    def display(self, level, *args, **kwargs):
        """Informs the widget about a new state to update the visualization in response to.

        Args:
            level (int): An integer in [1, 4] that specifies how "important" the message is.
                It may also be interpreted as a level of "specificity".
                1 means very general, such as the algorithm has finished.
                4 means very specific, such as some very minor algorithmic detail.
            *args: Any extra data to help the visualization update.
        """
        should_wait = True

        if args[0] == 'Performing AC with domains':
            should_wait = False
            domains = args[1]
            for var, domain in domains.items():
                self._send_set_domain_action(var, domain)

        elif args[0] == 'Domain pruned':
            variable = args[2]
            domain = args[4]
            constraint = args[6]
            self._send_set_domain_action(variable, domain)

        elif args[0] == "Processing arc (":
            variable = args[1]
            constraint = args[3]
            self._send_highlight_action(
                variable, constraint, style='bold', colour=None)

        elif args[0] == 'Domain pruned':
            variable = args[2]
            constraint = args[6]
            self._send_highlight_action(
                variable, constraint, style='bold', colour='green')

        elif args[0] == "Arc: (" and args[4] == ") is inconsistent":
            variable = args[1]
            constraint = args[3]
            self._send_highlight_action(
                variable, constraint, style='bold', colour='red')

        elif args[0] == "Arc: (" and args[4] == ") now consistent":
            variable = args[1]
            constraint = args[3]
            self._send_highlight_action(
                variable, constraint, style='normal', colour='green')
            should_wait = False

        elif args[0] == "  adding" and args[2] == "to to_do.":
            if args[1] != "nothing":
                arcs = list(args[1])
                for arc in arcs:
                    self._send_highlight_action(
                        arc[0], arc[1], style='normal', colour='blue')

        text = ' '.join(map(str, args))
        self.send({'action': 'output', 'text': text})

        if level <= self._desired_level:
            if should_wait:
                self._block_for_user_input.wait()
        elif args[0] == "solution:":
            self._block_for_user_input.wait()
        else:
            sleep(self.sleep_time)

    def _send_highlight_action(self, var, const, style='normal', colour=None):
        """Sends a message to the front-end visualization to highlight an arc.

        Args:
            var (string): The name of the variable that is part of the arc to highlight.
            const (Constraint): The constraint that is affecting `var`.
            style ('normal'|'bold'): Style of the highlight.
            colour (string|None): A HTML colour string for the colour of the line.
                Passing in None will keep the existing colour of the arc.
        """

        self.send({'action': 'highlightArc', 'arcId': self._edge_map[(var, const)],
                   'style': style, 'colour': colour})

    def _send_set_domain_action(self, var, domain):
        """Sends a message to the front-end visualization to set the domain of a variable.

        Args:
            var (string): The name of the variable whose domain should be changed.
            domain (List[int|string]): The updated domain of the variable.
        """
        self.send({'action': 'setDomain',
                   'nodeId': self._domain_map[var], 'domain': list(domain)})


def visualize(func_to_delay):
    """Enqueues a function that does not run until the Jupyter widget has rendered.

    Once the Jupyter widget has rendered once, further invocation of the wrapped function
    behave as if unwrapped.

    Args:
        func_to_delay (function): The function to delay.

    Returns: 
        The original function, wrapped such that it will automatically run
        when the Jupyter widget is rendered.
    """
    def wrapper(self, *args, **kwargs):
        if self._displayed_once is False:
            self._queued_func = {
                'func': partial(func_to_delay, self),
                'args': args, 'kwargs': kwargs
            }
        else:
            return func_to_delay(self, *args, **kwargs)

    return wrapper
