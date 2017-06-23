import ipywidgets as widgets
from IPython.display import display
from ipywidgets import CallbackDispatcher, DOMWidget, Output, register
from traitlets import Dict, Float, Integer, Unicode, observe
from aipython.utilities import cspToJson

@register('aispace.CSPBuilder')
class CSPBuilder(DOMWidget):
    """Build a CSP."""
    _view_name = Unicode('CSPBuilder').tag(sync=True)
    _model_name = Unicode('CSPBuilderModel').tag(sync=True)
    _view_module = Unicode('aispace').tag(sync=True)
    _model_module = Unicode('aispace').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)
    csp = Dict().tag(sync=True)

    def __init__(self, csp=None):
        super().__init__()
        (self.graphJSON, _, _) = cspToJson(csp)
        self.csp = self.graphJSON

    def get_csp(self):
        """Converts JSON back to Python obj"""
        pass