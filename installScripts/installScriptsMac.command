cd "$(dirname "$0")"
read -n1 -r -p "Make sure you have installed Anaconda, git, Node.js and npm.`echo $'\nPress any key to continue ...'`"
cd ..
echo Installing jupyterlab ...
conda install -c conda-forge jupyterlab
echo Installing ipywidgets. Enter 'y' when prompted to install ...
conda install -c conda-forge ipywidgets
echo Installing labextension ...
jupyter labextension install @jupyter-widgets/jupyterlab-manager
echo Installing AISpace2 library ...
pip install -e .
pip install -r requirements-dev.txt
cd js
npm install
npm run update-lab-extension
jupyter labextension install
cd ..
jupyter lab