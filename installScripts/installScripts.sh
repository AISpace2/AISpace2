cd "$(dirname "$0")"
read -n1 -r -p "Make sure you have installed Anaconda, git, Node.js.`echo $'\nPress any key to continue ...'`"
cd ..
echo Installing jupyterlab ...
pip install --upgrade jupyterlab
echo Installing ipywidgets ...
pip install --upgrade ipywidgets
echo Installing labextension ...
jupyter labextension install @jupyter-widgets/jupyterlab-manager
echo Installing AISpace2 library ...
pip install -e .
pip install -r requirements-dev.txt
cd js
npm install
echo Building AISpace2 frontend ...
npm run update-lab-extension
jupyter labextension install
cd ..
jupyter lab