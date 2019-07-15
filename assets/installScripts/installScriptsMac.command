cd "$(dirname "$0")"
cd AISpace2
echo Make sure you have installed Anaconda, git, Node.js and npm.
echo Installing jupyterlab...
conda install -c conda-forge jupyterlab
echo Installing ipywidgets...
conda install -c conda-forge ipywidgets # Enter 'y' when prompted to install
jupyter labextension install @jupyter-widgets/jupyterlab-manager@0.38
echo install AISpace2 library...
pip install -e .
cd js
npm install
npm run update-lab-extension
jupiter labextension install
cd ..
jupyter lab