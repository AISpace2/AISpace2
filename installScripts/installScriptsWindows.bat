@setlocal enableextensions
@cd /d "%~dp0"
echo Make sure you have installed Anaconda, git, Node.js.
pause
cd ..
echo Installing jupyterlab ...
call pip install --upgrade jupyterlab
echo Installing ipywidgets ...
call pip install --upgrade ipywidgets
echo Installing labextension ...
jupyter labextension install @jupyter-widgets/jupyterlab-manager
echo Installing AISpace2 library ...
pip install -e .
pip install -r requirements-dev.txt
cd js
call npm install
echo Building AISpace2 frontend ...
call npm run update-lab-extension
jupyter labextension install
cd ..
jupyter lab