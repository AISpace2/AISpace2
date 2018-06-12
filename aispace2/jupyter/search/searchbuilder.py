from aipython.searchProblem import Search_problem_from_explicit_graph
from ipywidgets import DOMWidget, register
from traitlets import Bool, Dict, Instance, Unicode, observe, Integer

from .searchjsonbridge import (json_to_search_problem, search_problem_to_json,
                               search_problem_to_python_code)

from  ... import __version__

@register
class SearchBuilder(DOMWidget):
    """A Jupyter widget that allows for visual creation of an explicit search problem.
    
    See the accompanying frontend file: `js/src/search/SearchBuilder.ts`
    """
    _view_name = Unicode('SearchBuilder').tag(sync=True)
    _model_name = Unicode('SearchBuilderModel').tag(sync=True)
    _view_module = Unicode('aispace2').tag(sync=True)
    _model_module = Unicode('aispace2').tag(sync=True)
    _view_module_version = Unicode(__version__).tag(sync=True)
    _model_module_version = Unicode(__version__).tag(sync=True)

    # The explicit search problem that is synced to the frontend.
    graph = Instance(
        klass=Search_problem_from_explicit_graph, allow_none=True).tag(
            sync=True,
            from_json=json_to_search_problem,
            to_json=search_problem_to_json)

    # True if the visualization should show edge costs.
    show_edge_costs = Bool(True).tag(sync=True)
    # True if a node's heuristic value should be shown.
    show_node_heuristics = Bool(False).tag(sync=True)
    text_size = Integer(12).tag(sync=True)

    def __init__(self, search_problem=None):
        super().__init__()
        self.graph = search_problem

    def search_problem(self):
        """Converts the search problem represented by this builder into a search problem.

        Returns:
            (aipython.searchProblem.Search_problem_from_explicit_graph):
                An explicit search problem represented by the builder.
        """
        return self.graph

    def py_code(self):
        """Converts the search problem represented by this builder into Python code.
        
        The code is added to a new cell in the notebook.
        """
        code = search_problem_to_python_code(self.search_problem())
        self.send({'action': 'python-code', 'code': code})
