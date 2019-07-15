@echo off
@setlocal enableextensions
@cd /d "%~dp0"
title Installation of AISpace2
echo Make sure you have Installed Anaconda, git, nodejs and npm and add them to PATH.
pause
echo Installing jupyterlab...
conda install -c conda-forge jupyterlab
echo Installing ipywidgets...
conda install -c conda-forge ipywidgets
echo install labextension...
jupyter labextension install @jupyter-widgets/jupyterlab-manager@0.38
echo install AISpace2 library
pip install -e .
pip install -r requirements-dev.txt
cd js
npm run update-lab-extension
jupyter labextension install
cd ..
jupyter lab