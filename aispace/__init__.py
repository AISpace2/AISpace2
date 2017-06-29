from ._version import version_info, __version__

from .cspbuilder import CSPBuilder

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'aispace',
        'require': 'aispace/extension'
    }]
