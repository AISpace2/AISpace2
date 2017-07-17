from functools import partial
from threading import Thread

from ipywidgets import register
from traitlets import Dict, Unicode, Bool

from aispace2.searchjsonbridge import search_problem_to_json

from .stepdomwidget import StepDOMWidget


@register('aispace2.SearchViewer')
class Displayable(StepDOMWidget):
    _view_name = Unicode('SearchViewer').tag(sync=True)
    _model_name = Unicode('SearchViewerModel').tag(sync=True)
    _view_module = Unicode('aispace2').tag(sync=True)
    _model_module = Unicode('aispace2').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)
    graph_json = Dict().tag(sync=True)
    problem = None
    search = None

    # True if the visualization should show edge costs.
    show_edge_costs = Bool(True).tag(sync=True)

    def __init__(self):
        super().__init__()

        (self.graph_json, self.node_map,
         self.edge_map) = search_problem_to_json(self.problem)

    def display(self, level, *args, **kwargs):
        if args[0] == 'Expanding: ':
            self._send_clear_action()
            path = args[1]

            # Highlight the path and end node red, and nodes along the path gray
            if path.arc:
                path_arcs = []
                current = path

                while current.arc is not None:
                    path_arcs.append(current.arc)
                    self._send_highlight_node_action(
                        current.arc.to_node, 'gray')
                    current = current.initial

                self._send_highlight_path_action(path_arcs, 'red')
                self._send_highlight_node_action(path.arc.to_node, 'red')

        elif args[0] == 'Neighbors are':
            neighbours = args[1]
            for arc in neighbours:
                self._send_highlight_path_action(arc, 'blue')
                self._send_highlight_node_action(arc.to_node, 'blue')

        super().display(level, *args, **kwargs)

    def _send_clear_action(self):
        """Sends a message to the front-end visualization to clear all styles applied to node/arcs."""
        self.send({'action': 'clear'})

    def _send_highlight_node_action(self, node, colour='black'):
        """Sends a message to the front-end visualization to highlight a node.

        Args:
            node (Any): A node in the search problem, typically a string
            colour (string|None): A HTML colour string that will be the stroke of the node.
                Defaults to 'black'/'#000000'.
        """
        self.send({'action': 'highlightNode',
                   'nodeId': self.node_map[node], 'colour': colour})

    def _send_highlight_path_action(self, arcs, colour='black'):
        """Sends a message to the front-end visualization to highlight a path.

        Args:
            arcs (aipython.searchProblem.Arc|:obj:`list` of :obj:`aipython.searchProblem.Arc`):
                An Arc or list of Arcs that represent a path to be highlighted.
            colour (string|None): A HTML colour string that is used as the stroke of the path.
                Defaults to 'black'/'#000000'.
        """
        # For convenience, allow the user to pass in a single arc
        if not isinstance(arcs, list):
            arcs = [arcs]

        path_edge_ids = []
        for arc in arcs:
            path_edge_ids.append(self.edge_map[(arc.from_node, arc.to_node)])

        self.send({'action': 'highlightPath',
                   'path': path_edge_ids, 'colour': colour})


def visualize(func_bg):
    """Runs a function in a background thread.

    Args:
        func_bg (function): The function to run in the background.

    Returns: 
        The original function, wrapped such that it will automatically run
        when the Jupyter widget is rendered.
    """

    def wrapper(self, *args, **kwargs):
        # We need to reset display_level so it doesn't carry over to next call
        self._display_block_level = 4
        self._thread = Thread(
            target=partial(func_bg, self), args=args, kwargs=kwargs)
        self._thread.start()
    return wrapper
