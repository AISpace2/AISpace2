from aipython.probGraphicalModels import Belief_network
from ipywidgets import register
from traitlets import Instance, Unicode
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

    bayes_problem = Instance(klass=Belief_network, allow_none=True)\
        .tag(sync=True, from_json=json_to_bayes_problem, to_json=bayes_to_json)

    def __init__(self, problem):
        super().__init__()
        self.bayes_problem = problem

    def _handle_custom_msg(self, _, content, buffers=None):
        super().handle_custom_msgs(None, content, buffers)
        event = content.get("event", '') # detect the event msg from frontend

        # Receive msg from frontend
        # if event == "draw":




