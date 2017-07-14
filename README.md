# AISpace2

## About
This is a Jupyter extension that aims to replace the existing AISpace Java applets. We want users to be able to interact and play with algorithms, not only visually as with the existing applets, but also by modifying the algorithms' code directly and seeing the results.

## User Installation

    $ pip install aispace2 --user
    $ jupyter nbextension enable --py --user aispace2

Note that if you have both `pip` and `pip3` installed, you should use `pip3` instead.

## Development Installation

For a development installation (requires npm),

    $ git clone https://github.com/aispace2/aispace2.git
    $ cd aispace2
    $ ./server.sh

Note that `./server.sh` uses `pip3`. You may need to change it to use `pip` if that is not available.

This will install the extension locally and link it to Jupyter.

During development, you do not need to refresh the page or reinstall the Jupyter extension as a result of Python changes, but you will need to restart the kernel. For front-end changes to take effect, you will need to run Webpack and refresh the page. You may run `npm run dev` while inside the `js/` folder to start a watcher that automatically recompiles your changes. You still need to provide the refresh, however.
