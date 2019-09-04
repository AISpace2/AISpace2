import time
import requests, re
from bs4 import BeautifulSoup

# Do not change this manually. Change this by runnning /updateVersion.py
version_info = (0, 7, 11)
__version__ = '.'.join(map(str, version_info))

update_notification = True

# website url that contains avialable version.
webVerURL = 'https://aispace2.github.io/AISpace2/install.html'
# lookup_time stores unix time of last look up of new ver.
lookup_time = 0
# time in seconds (currently one day), between checking the web url for new version.
cache_duration = 86400
# version of AISpace2 avialable on the website.
web_version = None


def get_web_version():
    global web_version
    global lookup_time
    # only updates web_version if time since last check is greater than cache_duration.
    if web_version != None and (time.time() - lookup_time < cache_duration):
        return web_version
    else:
        try:
            # read html from AISpace2 website, and parsed to get web_version
            req = requests.get(webVerURL)
            html_info = str(BeautifulSoup(req.content, "html.parser").find(id="install-current-version"))
            web_version = re.findall("\d+\.\d+\.\d+", html_info)[0]
            lookup_time = time.time()
            return web_version
        except:
            # in case when cannot connect to url, return stored version
            return __version__