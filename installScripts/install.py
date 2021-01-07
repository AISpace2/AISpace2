from subprocess import check_call,call
import os
dirname = os.path.dirname(__file__)
parentpath = os.path.abspath(os.path.join(dirname, os.pardir))
jspath = os.path.abspath(os.path.join(parentpath, 'js'))
print(jspath)
print("Make sure you have installed pip and Node.js.")
input("Press Enter to continue...")

isPIP = None; #None: No pip detected, False: using pip3, True: using pip
isNPM = None; #None: No NPM detected, False: using powershell, True: useing CMD
isNode = None; #None: No Node detected, False: using powershell, True: useing CMD
try:
	check_call(['pip3', '--version'])
	isPIP = False
except:
	check_call(['pip','--version'])
	isPIP = True
try:
	check_call(['npm','--version'])
	isNPM = True
except:
	try:
		check_call(['powershell', '-command','npm', '--version'])
		isNPM = False
	except:
		isNPM = None

try:
	check_call(['node','--version'])
	isNode = True
except:
	try:
		check_call(['powershell', '-command','node', '--version'])
		isNode= False
	except:
		isNode = None

if isPIP==None or isNPM == None or isNode==None :
	if isPIP==None: print("pip is not installed")
	if isNPM==None: print("npm is not installed")
	if isNode==None: print("nodejs is not installed")
	exit()

pipcmd = 'pip' if isPIP else 'pip3'
powershell = [] if isNPM else ['powershell', '-command']
os.chdir(parentpath)
try:
	check_call([pipcmd, 'install', '--upgrade','jupyterlab'])
	check_call([pipcmd, 'install', '--upgrade','ipywidgets'])
	check_call([pipcmd, 'install','-r','requirements-dev.txt'])
	check_call([pipcmd, 'install','-e','.'])
except:
	print('Error During Install')

os.chdir(jspath)
try:
	check_call(powershell + ['npm', 'install'])
    check_call(['jupyter','labextension', 'install' ,'@jupyter-widgets/jupyterlab-manager'])
	check_call(powershell + ['npm', 'run','update-lab-extension'])
	check_call(['jupyter','labextension', 'install'])
except:
	print('Error During Install')
os.chdir(parentpath)
check_call(['jupyter','lab'])
