import threading
from functools import partial
from time import sleep

from ipywidgets import DOMWidget, register
from traitlets import Dict, Float, Unicode

from aispace.searchjsonbridge import search_problem_to_json

@register('aispace.SearchViewer')
class Displayable(DOMWidget):
    _view_name = Unicode('SearchViewer').tag(sync=True)
    _model_name = Unicode('SearchViewerModel').tag(sync=True)
    _view_module = Unicode('aispace').tag(sync=True)
    _model_module = Unicode('aispace').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)
    graph_json = Dict().tag(sync=True)

    def __init__(self):
        super().__init__()
        (self.graph_json, _, self.edge_map) = search_problem_to_json(self.problem)
        self._block_for_user_input = threading.Event()

    def display(self, level, *args, **kwargs):
        if args[0] == 'Expanding:':
            path = args[1]
            if path.arc:
                path_edges = []
                current = path
                while current.arc is not None:
                    edge_id = self.edge_map[(current.arc.from_node, current.arc.to_node)]
                    path_edges.append(edge_id)
                    current = current.initial
                self.send({'action': 'highlightPath', 'path': path_edges})

        text = ' '.join(map(str, args))
        self.send({'action': 'output', 'text': text})
        sleep(1)

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
