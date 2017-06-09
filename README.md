aispace2
===============================

blah

Installation
------------

To install use pip:

    $ pip install aispace
    $ jupyter nbextension enable --py --sys-prefix aispace


For a development installation (requires npm),

    $ git clone https://github.com/aispace/aispace2.git
    $ cd aispace2
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix aispace
    $ jupyter nbextension enable --py --sys-prefix aispace
