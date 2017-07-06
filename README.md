# AISpace2

## About
This is a Jupyter extension that aims to replace the existing AISpace Java applets. We want users to be able to interact and play with algorithms, not only visually as with the existing applets, but also by modifying the algorithms' code directly and seeing the results.

## User Installation

    $ pip install aispace --user
    $ jupyter nbextension enable --py --user aispace

Note that if you have both `pip` and `pip3` installed, you should use `pip3` instead.

## Development Installation

For a development installation (requires npm),

    $ git clone https://github.com/aispace2/aispace2.git
    $ cd aispace2
    $ pip install -e . --user
    $ jupyter nbextension install --py --user
    $ jupyter nbextension enable --py --user


Note that if you have both `pip` and `pip3` installed, you should use `pip3` instead.
