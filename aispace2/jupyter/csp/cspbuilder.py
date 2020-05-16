from ipywidgets import DOMWidget, register
from traitlets import Dict, Instance, Integer, Unicode, Float

from aipython.cspProblem import CSP

from ... import __version__
from .cspjsonbridge import csp_to_json, csp_to_python_code, json_to_csp


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
    graph = Instance(klass=CSP, allow_none=True).tag(sync=True, from_json=json_to_csp, to_json=csp_to_json)
    text_size = Integer(12).tag(sync=True)
    line_width = Float(1.0).tag(sync=True)
    detail_level = Integer(2).tag(sync=True)
    decimal_place = Integer(2).tag(sync=True)

    def __init__(self, csp=None):
        super().__init__()
        self.graph = csp

    def py_code(self, need_positions=False):
        """Prints the CSP represented by Python code.
        """
        print(csp_to_python_code(self.graph, need_positions))
