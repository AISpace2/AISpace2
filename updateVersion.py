import os
import fileinput
import json

versionPath = os.path.abspath(os.path.join(os.path.dirname(__file__),'aispace2','_version.py'))
versionFile = open(versionPath)
jsonPath = os.path.abspath(os.path.join(os.path.dirname(__file__),'js','package.json'))

with open(jsonPath, 'r+') as f:
    data = json.load(f)
    print("Previous Version in Extension:")
    print(data['version'])


version = input("Enter new Version: Format X.Y.Z\n")


listr = version.split('.')
try:
    assert(len(listr)==3)
    int(listr[0])
    int(listr[1])
    int(listr[2])
except:
    print("Format Error")
    exit()
    

pyVersion = '('+ str(int(listr[0])) +', ' + str(int(listr[1])) + ', ' + str(int(listr[2])) +')'
version = str(int(listr[0]))+'.'+str(int(listr[1]))+'.'+str(int(listr[2]))
print(version)
v = input("Enter y to confirm\n")
if v!= 'y':
    exit()
for line in fileinput.FileInput(versionPath, inplace=1):
    if line.startswith('version_info'):
        line = 'version_info = ' + pyVersion
        print(line)
    else:
        print(line.rstrip())
        

with open(jsonPath, 'r+') as f:
    data = json.load(f)
    data['version'] = version
    f.seek(0)
    json.dump(data, f, indent=2)
    f.truncate()
print('Completed')