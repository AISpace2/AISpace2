from ._version import version_info, __version__

from .cspbuilder import CSPBuilder
from .searchbuilder import SearchBuilder

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'aispace2',
        'require': 'aispace2/extension'
    }]
