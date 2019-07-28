version_info = (0, 7, 10)

try:
    import os
    import json
    jsonPath = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','js','package.json'))
    with open(jsonPath, 'r+') as f:
        data = json.load(f)

    version = data['version'].split('.')
    version_info = (int(version[0]), int(version[1]), int(version[2]))
except:
    pass



__version__ = '.'.join(map(str, version_info))
