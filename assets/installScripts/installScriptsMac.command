cd "$(dirname "$0")"
cd AISpace2
read -n1 -r -p "Make sure you have installed Anaconda, git, Node.js and npm.`echo $'\nPress any key to continue ...'`"
echo Installing jupyterlab ...
conda install -c conda-forge jupyterlab
echo Installing ipywidgets. Enter 'y' when prompted to install ...
conda install -c conda-forge ipywidgets
echo install labextension ...
jupyter labextension install @jupyter-widgets/jupyterlab-manager@0.38
echo install AISpace2 library ...
pip install -e .
pip install -r requirements-dev.txt
cd js
npm install
npm run update-lab-extension
jupiter labextension install
cd ..
jupyter lab