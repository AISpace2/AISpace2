import os
import fileinput
import json
import re

# find current version
jsonPath = os.path.abspath(os.path.join(os.path.dirname(__file__),'js','package.json'))
with open(jsonPath, 'r+') as f:
    data = json.load(f)
    print("Current version: " + data['version'] + ".")

version = input("Enter new a new version number, format X.Y.Z:\n")

# validate
listr = version.split('.')
try:
    assert(len(listr)==3)
    int(listr[0])
    int(listr[1])
    int(listr[2])
except:
    print("Format Error. Exit.")
    exit()

# confirm
v = input("Enter y to confirm.\n")
if v!= 'y':
    print("Exit.")
    exit()

# format version number
version_info = '('+ str(int(listr[0])) +', ' + str(int(listr[1])) + ', ' + str(int(listr[2])) +')' # e.g. (7, 1, 10)
version = str(int(listr[0]))+'.'+str(int(listr[1]))+'.'+str(int(listr[2])) # e.g. 7.1.10

# change version number specified in website
websiteVersionPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'AISpace2-gh-pages', 'install.html'))
websiteVersionFile = open(websiteVersionPath)
for line in fileinput.FileInput(websiteVersionPath, inplace=1):
    if re.findall("""\s*<span id="install-current-version">Current version: \d+\.\d+\.\d+\.</span>""", line):
        line = """<span id="install-current-version">Current version: """ + version + ".</span>"
        print(line)
    else:
        print(line.rstrip())
websiteVersionFile.close()

# change version number specified in _version.py
versionPath = os.path.abspath(os.path.join(os.path.dirname(__file__),'aispace2','_version.py'))
versionFile = open(versionPath)
for line in fileinput.FileInput(versionPath, inplace=1):
    if re.findall("version_info = \(\d+, \d+, \d+\)", line):
        line = "version_info = " + version_info
        print(line)
    else:
        print(line.rstrip())
versionFile.close()

# change version number specified in package.json
with open(jsonPath, 'r+') as f:
    data = json.load(f)
    data['version'] = version
    f.seek(0)
    json.dump(data, f, indent=2)
    f.write("\n")
    f.truncate()
    f.close()

print("Version updated to " + version + ".")
