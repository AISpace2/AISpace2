@setlocal enableextensions
@cd /d "%~dp0"
cd ..
cd js
echo Building AISpace2 frontend ...
call npm run update-lab-extension
jupyter labextension install
cd ..
jupyter lab