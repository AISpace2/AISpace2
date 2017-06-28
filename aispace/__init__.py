from ._version import version_info, __version__

from .cspviewer import CSPViewer
from .cspbuilder import CSPBuilder

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'aispace',
        'require': 'aispace/extension'
    }]
