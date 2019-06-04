cd "$(dirname "$0")"
conda install -c conda-forge jupyterlab
conda install -c conda-forge ipywidgets # Enter 'y' when prompted to install
pip install aispace2 --user
jupyter labextension install aispace2
jupyter labextension install @jupyter-widgets/jupyterlab-manager
git clone https://github.com/AISpace2/AISpace2.git
cd AISpace2
jupyter lab