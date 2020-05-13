from ipywidgets import DOMWidget, register
from traitlets import Bool, Dict, Instance, Integer, Unicode, Float

from aipython.probGraphicalModels import Belief_network

from ... import __version__
from .bayesjsonbridge import (bayes_problem_to_json,
                              bayes_problem_to_python_code,
                              json_to_bayes_problem)


@register
class BayesBuilder(DOMWidget):
    """A Jupyter widget that allows for visual creation of a Belief Network.
    See the accompanying frontend file: `js/src/bayes/BayesBuilder.ts`
    """
    _view_name = Unicode('BayesBuilder').tag(sync=True)
    _model_name = Unicode('BayesBuilderModel').tag(sync=True)
    _view_module = Unicode('aispace2').tag(sync=True)
    _model_module = Unicode('aispace2').tag(sync=True)
    _view_module_version = Unicode(__version__).tag(sync=True)
    _model_module_version = Unicode(__version__).tag(sync=True)

    # The Bayes problem that is synced as a graph to the frontend.
    graph = Instance(klass=Belief_network, allow_none=True).tag(
        sync=True, from_json=json_to_bayes_problem, to_json=bayes_problem_to_json)
    text_size = Integer(12).tag(sync=True)
    line_width = Float(1.0).tag(sync=True)
    detail_level = Integer(2).tag(sync=True)
    decimal_place = Integer(2).tag(sync=True)

    def __init__(self, bayes_problem=None):
        super().__init__()
        self.graph = bayes_problem

    def py_code(self, need_positions=False):
        """Prints the bayes problem represented by Python code.
        """
        print(bayes_problem_to_python_code(self.graph, need_positions))
