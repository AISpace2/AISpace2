import requests, re
import os
from bs4 import BeautifulSoup
from configparser import ConfigParser

# Do not change this manually. Change this by runnning /updateVersion.py
version_info = (0, 8, 11)
__version__ = '.'.join(map(str, version_info))

# website url that contains avialable version.
web_ver_URL = 'https://aispace2.github.io/AISpace2/install.html'

root_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(root_path, '_version.ini')

def get_web_version():
    try:
        # read html from AISpace2 website, and parsed to get web_version
        req = requests.get(web_ver_URL)
        html_info = str(BeautifulSoup(req.content, "html.parser").find(id="install-current-version"))
        return re.findall("\d+\.\d+\.\d+", html_info)[0] 
    except:
        # in case when cannot connect to url, return stored version
        return __version__

def need_update():
    parser = read_config()
    web_version = get_web_version()
    web_ver_info = web_version.split(".")

    update_notification = parser.getboolean('config', 'update_notification')

    if (version_info[1] < int(web_ver_info[1])) and update_notification:
        return True
    return False

def toggle_update():
    writer = ConfigParser()
    writer.add_section('config')
    writer.set('config', 'update_notification', 'false')
    with open(config_path, 'w') as configfile:
        writer.write(configfile)

def read_config():
    config_reader = ConfigParser()
    config_reader.read(config_path)
    return config_reader