cd "$(dirname "$0")"
read -n1 -r -p "Make sure you have installed pip and Node.js.`echo $'\nPress any key to continue ...'`"
cd ..
echo Installing jupyterlab ...
pip3 install --upgrade jupyterlab
echo Installing ipywidgets ...
pip3 install --upgrade ipywidgets
echo Installing labextension ...
jupyter labextension install @jupyter-widgets/jupyterlab-manager
echo Installing AISpace2 library ...
pip3 install -r requirements-dev.txt
pip3 install -e .
cd js
npm install
echo Building AISpace2 frontend ...
npm run update-lab-extension
jupyter labextension install
cd ..
jupyter lab