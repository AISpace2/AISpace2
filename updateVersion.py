import fileinput
import json
import os
import re
import sys

from termcolor import colored

jsonPath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'js', 'package.json'))

if sys.argv[1]:
    version = sys.argv[1]
else:
    # find current version
    with open(jsonPath, 'r+') as f:
        data = json.load(f)
        print("Current version: " + data['version'] + ".")

    version = input("Enter new a new version number, format X.Y.Z: ")


# validate
listr = version.split('.')
try:
    assert(len(listr) == 3)
    int(listr[0])
    int(listr[1])
    int(listr[2])
except:
    print("Format Error. Exit.")
    exit()

# confirm
print(colored("DEVELOPMENT USE ONLY. NORMAL USER PLEASE EXIT.", "red", "on_green"))
v = input("Enter y to confirm, any other key to exit: ")
if v != 'y':
    print("Exit.")
    exit()

# format version number
version_info = '(' + str(int(listr[0])) + ', ' + str(int(listr[1])) + ', ' + str(int(listr[2])) + ')'  # e.g. (7, 1, 10)
version = str(int(listr[0])) + '.' + str(int(listr[1])) + '.' + str(int(listr[2]))  # e.g. 7.1.10

# change version number specified in website
websiteVersionPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'AISpace2-gh-pages', 'install.html'))
websiteVersionFile = open(websiteVersionPath)
for line in fileinput.FileInput(websiteVersionPath, inplace=True):
    print(re.sub("""span id="install-current-version">Current version: \d+\.\d+\.\d+\.</span>""", """span id="install-current-version">Current version: """ + version + ".</span>", line).rstrip())
for line in fileinput.FileInput(websiteVersionPath, inplace=True):
    print(re.sub("""li>Download <a href="./assets/AISpace2-\d+\.\d+\.\d+\.zip" download>AISpace2</a> and unzip the file in the directory where you want to store it.</li>""",
                 """li>Download <a href="./assets/AISpace2-""" + version + """.zip" download>AISpace2</a> and unzip the file in the directory where you want to store it.</li>""",
                 line).rstrip())
websiteVersionFile.close()

# change version number specified in _version.py
versionPath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'aispace2', '_version.py'))
versionFile = open(versionPath)
for line in fileinput.FileInput(versionPath, inplace=True):
    print(re.sub("version_info = \(\d+, \d+, \d+\)", "version_info = " + version_info, line).rstrip())
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
