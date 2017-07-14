from ipywidgets import DOMWidget, register
from traitlets import Dict, Unicode

from .searchjsonbridge import json_to_search_problem, search_problem_to_json


@register('aispace2.SearchBuilder')
class SearchBuilder(DOMWidget):
    """A Jupyter widget that allows for visual creation of a CSP."""
    _view_name = Unicode('SearchBuilder').tag(sync=True)
    _model_name = Unicode('SearchBuilderModel').tag(sync=True)
    _view_module = Unicode('aispace2').tag(sync=True)
    _model_module = Unicode('aispace2').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)
    graph_json = Dict().tag(sync=True)

    def __init__(self, csp=None):
        super().__init__()
        (self.graph_json, _, _) = search_problem_to_json(csp)

    def search_problem(self):
        return json_to_search_problem(self.graph_json)
