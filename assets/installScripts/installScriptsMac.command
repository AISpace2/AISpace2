cd "$(dirname "$0")"
chmod u+x jupyterlab.command
cp jupyterlab.command ../jupyterlab.command
cd ..
cd AISpace2
conda install -c conda-forge jupyterlab
conda install -c conda-forge ipywidgets # Enter 'y' when prompted to install
pip install -e .
jupyter labextension install @jupyter-widgets/jupyterlab-manager@0.38
cd js
npm install
npm run update-lab-extension
jupiter labextension install
cd ..
jupyter lab