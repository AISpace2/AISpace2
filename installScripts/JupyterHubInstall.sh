cd "$(dirname "$0")"
cd ..
cd js
npm install
cd ..
pip3 install -r requirements-dev.txt
pip3 install -e .
echo Installing Jupyter labextension ...
jupyter labextension install @jupyter-widgets/jupyterlab-manager
cd js
echo Building AISpace2 frontend ...
npm run update-lab-extension
jupyter labextension install
cd ..
jupyter lab