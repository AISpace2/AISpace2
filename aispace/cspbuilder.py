from string import Template

import ipywidgets as widgets
from IPython.display import display
from ipywidgets import CallbackDispatcher, DOMWidget, Output, register
from traitlets import Dict, Float, Integer, Unicode, observe

from .cspjsonbridge import csp_from_json, csp_to_json, csp_to_python_code


@register('aispace.CSPBuilder')
class CSPBuilder(DOMWidget):
    """Allows visual creation of a CSP."""
    _view_name = Unicode('CSPBuilder').tag(sync=True)
    _model_name = Unicode('CSPBuilderModel').tag(sync=True)
    _view_module = Unicode('aispace').tag(sync=True)
    _model_module = Unicode('aispace').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)
    graphJSON = Dict().tag(sync=True)

    def __init__(self, csp=None):
        super().__init__()
        (self.graphJSON, _, _) = csp_to_json(csp)

    def csp(self):
        """Converts the CSP represented by this builder into a Python CSP object."""
        return csp_from_json(self.graphJSON)

    def py_code(self):
        """Converts the CSP represented by this builder into Python code."""

        self.send({'action': 'python-code',
                   'code': csp_to_python_code(self.csp())})
