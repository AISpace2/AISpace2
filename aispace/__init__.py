from ._version import version_info, __version__

from .cspviewer import *
from .cspbuilder import *
from aipython.utilities import *

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'aispace',
        'require': 'aispace/extension'
    }]
