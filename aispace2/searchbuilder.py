from ipywidgets import DOMWidget, register
from traitlets import Dict, Unicode, Bool

from .searchjsonbridge import (
    json_to_search_problem, 
    search_problem_to_json, 
    search_problem_to_python_code
)


@register('aispace2.SearchBuilder')
class SearchBuilder(DOMWidget):
    """A Jupyter widget that allows for visual creation of an explicit search problem."""
    _view_name = Unicode('SearchBuilder').tag(sync=True)
    _model_name = Unicode('SearchBuilderModel').tag(sync=True)
    _view_module = Unicode('aispace2').tag(sync=True)
    _model_module = Unicode('aispace2').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)

    # The JSON representation of the search graph.
    graph_json = Dict().tag(sync=True)

    # True if the visualization should show edge costs.
    show_edge_costs = Bool(True).tag(sync=True)
    # True if a node's heuristic value should be shown.
    show_node_heuristics = Bool(False).tag(sync=True)

    def __init__(self, csp=None):
        super().__init__()
        (self.graph_json, _, _) = search_problem_to_json(csp)

    def search_problem(self):
        """Converts the search problem represented by this builder into a search problem.

        Returns:
            (aipython.searchProblem.Search_problem_from_explicit_graph):
                An explicit search problem represented by the builder.
        """
        return json_to_search_problem(self.graph_json)

    def py_code(self):
        """Converts the search problem represented by this builder into Python code.
        
        The code is added to a new cell in the notebook.
        """
        code = search_problem_to_python_code(self.search_problem())
        self.send({'action': 'python-code',
                   'code': code})
