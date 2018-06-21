import copy
import json
from functools import partial
from threading import Thread

from aipython.searchProblem import Arc, Search_problem_from_explicit_graph
from ipywidgets import register
from traitlets import Bool, Dict, Instance, Unicode, observe

from ..stepdomwidget import ReturnableThread, StepDOMWidget
from .searchjsonbridge import (generate_search_graph_mappings,
                               implicit_to_explicit_search_problem,
                               json_to_search_problem, search_problem_to_json)

from ... import __version__

@register
class Displayable(StepDOMWidget):
    """A Jupyter widget for visualizing search problems.

    Handles events from DFS, A*, B&B, and more. Works with implicit or explicit search problems.
    
    See the accompanying frontend file: `js/src/search/SearchVisualizer.ts`
    """
    _view_name = Unicode('SearchViewer').tag(sync=True)
    _model_name = Unicode('SearchViewerModel').tag(sync=True)
    _view_module = Unicode('aispace2').tag(sync=True)
    _model_module = Unicode('aispace2').tag(sync=True)
    _view_module_version = Unicode(__version__).tag(sync=True)
    _model_module_version = Unicode(__version__).tag(sync=True)

    # The explicit search problem that is synced to the frontend.
    # If the problem was already explicit, the problem itself; otherwise, it is converted first.
    graph = Instance(
        klass=Search_problem_from_explicit_graph, allow_none=True).tag(
            sync=True,
            from_json=json_to_search_problem,
            to_json=search_problem_to_json)

    # True if the visualization should show edge costs.
    show_edge_costs = Bool(True).tag(sync=True)

    # True if a node's heuristic value should be shown.
    show_node_heuristics = Bool(False).tag(sync=True)

    # Controls the layout engine used. Either "force" for force layout, or "tree".
    layout_method = Unicode('force').tag(sync=True)

    # The ID of the node to be used as the root of the tree.
    # Only applicable when using tree layout. Set automatically to the problem's start node.
    _layout_root_id = Unicode('').tag(sync=True)

    # Tracks if the visualization has been rendered at least once in the front-end. See the @visualize decorator.
    _previously_rendered = Bool(False).tag(sync=True)

    hide_text = Bool(False).tag(sync=True)

    def __init__(self):
        super().__init__()

        # The explicit representation of the problem.
        # If the problem was already explicit, the problem itself; otherwise, it will be converted next.
        self.graph = None

        # Arcs in tuple form (str(from_node), str(to_node)) that have been added to the explicit graph.
        # Only used if the problem is implicit. Useful when search() is ran again;
        # the explicit graph already contains neighbours that are about to be rediscovered
        self._implicit_neighbours_added = set()

        # Convert the implicit graph to an explicit graph if necessary
        if not isinstance(self.problem, Search_problem_from_explicit_graph):
            self.graph = implicit_to_explicit_search_problem(self.problem)
            self._is_problem_explicit = False
        else:
            self.graph = self.problem
            self._is_problem_explicit = True

        (self.node_map,
         self.edge_map) = generate_search_graph_mappings(self.graph)

        self._frontier = []

        # Assumption: there is a start node
        self._layout_root_id = self.node_map[str(self.graph.start)]

    def handle_custom_msgs(self, _, content, buffers=None):
        super().handle_custom_msgs(None, content, buffers)
        event = content.get('event', '')

        if event == 'initial_render':
            self._previously_rendered = True
            queued_func = getattr(self, '_queued_func', None)

            if queued_func:
                func = queued_func['func']
                args = queued_func['args']
                kwargs = queued_func['kwargs']
                self._thread = ReturnableThread(
                    target=func, args=args, kwargs=kwargs)
                self._thread.start()

    def display(self, level, *args, **kwargs):
        if args[0] == 'Expanding:':
            path = args[1]
            self._send_clear_action()
            self._send_frontier_updated_action()

            if path.arc:
                nodes_along_path = []
                arcs_of_path = []
                current = path

                while current.arc is not None:
                    arcs_of_path.append(current.arc)
                    nodes_along_path.append(current.arc.from_node)
                    current = current.initial

                # Highlight the path and end node red, and nodes along the path gray
                self._send_highlight_nodes_action(nodes_along_path, 'gray')
                self._send_highlight_path_action(arcs_of_path, 'red')
                self._send_highlight_nodes_action(path.arc.to_node, 'red')
            else:
                self._send_highlight_nodes_action(path, 'red')

        elif args[0] == 'Neighbors are':
            neighbours = args[1]
            if not neighbours:
                return

            if not self._is_problem_explicit:
                # If the problem is implicit, we may need to add newly discovered neighbours
                has_graph_changed = False
                for arc in neighbours:
                    self.graph.nodes.add(str(arc.to_node))

                    if self.problem.is_goal(arc.to_node):
                        self.graph.goals.add(str(arc.to_node))

                    if (str(arc.from_node), str(arc.to_node)
                        ) not in self._implicit_neighbours_added:
                        # Found a new neighbour!
                        self.graph.arcs.append(arc)
                        self._implicit_neighbours_added.add(
                            (str(arc.from_node), str(arc.to_node)))
                        self.graph.hmap[str(
                            arc.to_node)] = self.problem.heuristic(
                                arc.to_node)
                        has_graph_changed = True

                if has_graph_changed:
                    # Sync updated explicit representation with the front-end
                    (self.node_map, self.edge_map
                     ) = generate_search_graph_mappings(self.graph)
                    self._layout_root_id = self.node_map[str(self.graph.start)]
                    self.graph = copy.copy(
                        self.graph
                    )  # Copy necessary to trigger resynchronization

            neighbour_nodes = []
            arcs_of_path = []

            for arc in neighbours:
                neighbour_nodes.append(arc.to_node)
                arcs_of_path.append(arc)

            self._send_highlight_nodes_action(neighbour_nodes, 'blue')
            self._send_highlight_path_action(arcs_of_path, 'blue')

        elif args[0] == "Frontier:":
            self._frontier = args[1]
            self._send_clear_action()
            self._send_frontier_updated_action()

        elif args[1] == "paths have been expanded and":
            args += ('- Run search() again to find more solutions.', )

        super().display(level, *args, **kwargs)

    def _send_clear_action(self):
        """Sends a message to the front-end visualization to clear all styles applied to node/arcs."""
        self.send({'action': 'clear'})

    def _send_frontier_updated_action(self):
        """Sends a message to the front-end visualization that the frontier has been updated.
        
        This is a convenience function that uses the value of `self._frontier` to select which nodes to highlight.
        It also sends a message to the frontend asking it to persist the frontier between output calls.
        """
        nodes_to_highlight = []

        for path in self._frontier:
            nodes_to_highlight.append(path.end())

        self._send_clear_action()
        self._send_highlight_nodes_action(nodes_to_highlight, 'green')
        self.send({'action': 'setFrontier', 'frontier': str(self._frontier)})

    def _send_highlight_nodes_action(self, nodes, colour='black'):
        """Sends a message to the front-end visualization to highlight a node.

        Args:
            nodes (Any|Any[]): Node(s) in the search problem.
            colour (string|None): A HTML colour string that will be the stroke of the node.
                Defaults to 'black'/'#000000'.
        """
        # For convenience, allow the user to pass in a single arc
        if not isinstance(nodes, list):
            nodes = [nodes]

        nodeIds = []
        for node in nodes:
            nodeIds.append(self.node_map[str(node)])

        self.send({
            'action': 'highlightNodes',
            'nodeIds': nodeIds,
            'colour': colour
        })

    def _persist_frontier(self):
        """Sends a message to the front-end visualization to set the current frontier."""
        frontier = self._frontier
        self.send({'action': 'persist_frontier', 'frontier': str(frontier)})

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
            path_edge_ids.append(
                self.edge_map[(str(arc.from_node), str(arc.to_node))])

        self.send({
            'action': 'highlightPath',
            'path': path_edge_ids,
            'colour': colour
        })


def visualize(func_bg):
    """Runs a function in a background thread.

    This is meant to be used as a decorator and is required for all functions called directly in Jupyter.
    Otherwise, `display()` will block the main thread.

    Args:
        func_bg (function): The function to run in the background.

    Returns: 
        The original function, wrapped such that it will automatically run
        when the Jupyter widget is rendered.
    """

    def wrapper(self, *args, **kwargs):
        # We need to reset display_level so it doesn't carry over to next call
        self.max_display_level = 4

        if self._previously_rendered:
            self._thread = ReturnableThread(
                target=partial(func_bg, self), args=args, kwargs=kwargs)
            self._thread.start()
        else:
            self._queued_func = {
                'func': partial(func_bg, self),
                'args': args,
                'kwargs': kwargs
            }

    return wrapper
