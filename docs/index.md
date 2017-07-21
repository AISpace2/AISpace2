# AISpace2

**AISpace2** is a suite of [Jupyter](http://jupyter.org) widgets that accompanies the book ["Artifical Intelligence 2E: Foundations of Computational Agents"](http://aipython.org).

## Start Here
1. Ensure you have [Python](http://python.org) 3.3+ and [Jupyter](http://jupyter.org) installed. If you are using JupyterHub, you won't need to install anything.

2. Launch a terminal instance. In JupyterHub, you can do this in the notebook dashboard by selecting _New > Terminal_.

3. Run the following commands to install the widget:

    ```
    pip install aispace2 --user
    jupyter nbextension enable --py aispace2 --user
    ```
Depending on your setup, you may have to use `pip3` instead of `pip` to ensure you are installing the extension to Python 3 instead of Python 2.

4. Choose a notebook to download from below. For a full list, see the [repository](https://github.com/AISpace2/AISpace2/tree/master/notebooks). 

- [Search: A*, Multiple Path Pruning, Branch and Bound](https://rawgit.com/AISpace2/AISpace2/master/notebooks/search/search.ipynb)
- [Constraint Satisfcation Problems (CSPs) using Search](https://rawgit.com/AISpace2/AISpace2/master/notebooks/csp/solving_csp_with_search.ipynb)
- [Constraint Satisfaction Problems (CSPs) using Arc Consistency](https://rawgit.com/AISpace2/AISpace2/master/notebooks/csp/csp.ipynb)

    You should download these notebooks by right-clicking a link and choosing _Save As_.

5. Open Jupyter and upload the notebook to Jupyter. In the notebook dashboard, select _Upload_ and choose the file you just downloaded.

6. Open the notebook and run the cells one-by-one. You're done!
