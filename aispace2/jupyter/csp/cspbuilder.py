from aipython.cspProblem import CSP
from ipywidgets import DOMWidget, register
from traitlets import Dict, Instance, Unicode, Integer

from .cspjsonbridge import csp_from_json, csp_to_json, csp_to_python_code

from ... import __version__

@register
class CSPBuilder(DOMWidget):
    """A Jupyter widget that allows for visual creation of a CSP.

    See the accompanying frontend file: `js/src/csp/CSPBuilder.ts`
    
    Currently incomplete. We have not figured out how to handle how to serialize Python constraints,
    especially because they can be any arbitrary functions. The imagined scenario is if a user
    bases their CSP off of a CSP with custom constraints, modifies a few things, then tries to
    export it. How do we get those constraints back through the JSON serialization process?

    - Reference it from the object they passed in?
    - Do some weird code introspection and pull in the source code?
    - Only allow creation of CSPs from scratch and generate code from a whitelist of functions?
    """
    _view_name = Unicode('CSPBuilder').tag(sync=True)
    _model_name = Unicode('CSPBuilderModel').tag(sync=True)
    _view_module = Unicode('aispace2').tag(sync=True)
    _model_module = Unicode('aispace2').tag(sync=True)
    _view_module_version = Unicode(__version__).tag(sync=True)
    _model_module_version = Unicode(__version__).tag(sync=True)

    # The CSP that is synced as a graph to the frontend.
    graph = Instance(
        klass=CSP, allow_none=True).tag(
            sync=True, from_json=csp_from_json, to_json=csp_to_json)
    text_size = Integer(12).tag(sync=True)

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
