from aipython.cspProblem import CSP
from ipywidgets import DOMWidget, register
from traitlets import Dict, Instance, Unicode

from .cspjsonbridge import csp_from_json, csp_to_json, csp_to_python_code


@register
class CSPBuilder(DOMWidget):
    """A Jupyter widget that allows for visual creation of a CSP."""
    _view_name = Unicode('CSPBuilder').tag(sync=True)
    _model_name = Unicode('CSPBuilderModel').tag(sync=True)
    _view_module = Unicode('aispace2').tag(sync=True)
    _model_module = Unicode('aispace2').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)

    # The CSP that is synced as a graph to the frontend.
    graph = Instance(
        klass=CSP, allow_none=True).tag(
            sync=True, from_json=csp_from_json, to_json=csp_to_json)

    def __init__(self, csp=None):
        super().__init__()
        self.graph = csp

    def csp(self):
        """Converts the CSP represented by this builder into a Python CSP object."""
        return self.graph

    def py_code(self):
        """Converts the CSP represented by this builder into Python code."""
        self.send({
            'action': 'python-code',
            'code': csp_to_python_code(self.csp())
        })
