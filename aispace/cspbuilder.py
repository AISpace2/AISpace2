import ipywidgets as widgets
from IPython.display import display
from ipywidgets import CallbackDispatcher, DOMWidget, Output, register
from traitlets import Dict, Float, Integer, Unicode, observe
from aipython.utilities import cspToJson
from aipython.cspProblem import CSP, Constraint
from operator import lt
from string import Template


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
        (self.graphJSON, _, _) = cspToJson(csp)

    def csp(self):
        """Converts the CSP represented by this builder into a Python CSP object."""
        domains = {
            node['name']: set(node['domain'])
            for node in self.graphJSON['nodes'] if node['type'] == 'csp:variable'
        }

        constraints = []

        for node in self.graphJSON['nodes']:
            scope = []
            if node['type'] == 'csp:constraint':
                # By convention, the source is the variable, and the target is the constraint
                # Find the links with the target as this constraint
                for link in self.graphJSON['links']:
                    if link['target']['id'] == node['id']:
                        scope.append(link['source']['name'])

                if scope:
                    constraints.append(Constraint(tuple(scope), lt))

        return CSP(domains, constraints)

    def py_code(self):
        """Converts the CSP represented by this builder into Python code."""
        csp = self.csp()

        constStrList = []
        for constraint in csp.constraints:
            constStrList.append(f"Constraint({constraint.scope}, {constraint.condition.__name__})")

        template = """from aipython.cspProblem import CSP, Constraint
csp = CSP($domains, [$constraints])"""
        self.send({'action': 'python-code',
                   'code': Template(template).substitute(domains=csp.domains, constraints=', '.join(constStrList))})
