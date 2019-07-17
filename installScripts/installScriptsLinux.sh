dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd $dir
cd ..
echo Installing jupyterlab ...
conda install -c conda-forge jupyterlab=0.35
echo Installing ipywidgets. Enter 'y' when prompted to install ...
conda install -c conda-forge ipywidgets=7.4.2
echo Installing labextension ...
jupyter labextension install @jupyter-widgets/jupyterlab-manager@0.38
echo Installing AISpace2 library ...
pip install -e .
pip install -r requirements-dev.txt
cd js
npm install
npm run update-lab-extension
jupyter labextension install
cd ..
jupyter lab
