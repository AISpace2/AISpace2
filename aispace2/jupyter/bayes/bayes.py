from aipython.probGraphicalModels import Belief_network
from aipython.probVE import VE
from ipywidgets import register
from traitlets import Instance, Unicode, Float, Integer, Bool
from .bayesjsonbridge import bayes_to_json, json_to_bayes_problem
from ..stepdomwidget import ReturnableThread, StepDOMWidget
from ... import __version__

@register
class Displayable(StepDOMWidget):
    _view_name = Unicode('BayesViewer').tag(sync=True)
    _model_name = Unicode('BayesViewerModel').tag(sync=True)
    _view_module = Unicode('aispace2').tag(sync=True)
    _model_module = Unicode('aispace2').tag(sync=True)
    _view_module_version = Unicode(__version__).tag(sync=True)
    _model_module_version = Unicode(__version__).tag(sync=True)

    graph = Instance(klass=Belief_network, allow_none=True)\
        .tag(sync=True, from_json=json_to_bayes_problem, to_json=bayes_to_json)

    line_width = Float(4.0).tag(sync=True)
    text_size = Integer(12).tag(sync=True)
    show_full_domain = Bool(False).tag(sync=True)
    detail_level = Integer(2).tag(sync=True)
    decimal_place = Integer(10).tag(sync=True)

    probCalculator = VE()

    def __init__(self):
        super().__init__()
        self.graph = self.problem
        self.probCalculator = VE(self.problem)

    def _validate_line_width(self, proposal):
        """Cap line_width at a minimum value."""
        line_width = proposal['value']
        return min(1, line_width)

    def handle_custom_msgs(self, _, content, buffers=None):
        event = content.get('event', '')

        # Receive msg from frontend
        if event == "node:query":
            name = content.get('name')
            evidences = content.get('evidences')
            self._query_node(name, evidences)
        elif event == 'initial_render':
            queued_func = getattr(self, '_queued_func', None)

            # Run queued function after we know the frontend view exists
            if queued_func:
                func = queued_func['func']
                args = queued_func['args']
                kwargs = queued_func['kwargs']
                self._previously_rendered = True
                self._thread = ReturnableThread(
                    target=func, args=args, kwargs=kwargs)
                self._thread.start()

    def _query_node(self, name, evidences):
        name_to_node = {v.name: v for v in self.graph.variables}
        node = name_to_node[name]
        evidence_list = {name_to_node[e['name']]: e['value'] for e in evidences}
        reply = self.probCalculator.query(node, evidence_list)
        self.send({
            "action": "query",
            "name": name,
            "trueProb": reply[True],
            "falseProb": reply[False]
        })
