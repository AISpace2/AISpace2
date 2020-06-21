cd "$(dirname "$0")"
cd ..
cd js
echo Building AISpace2 frontend ...
npm run update-lab-extension
jupyter labextension install
cd ..
jupyter lab