from __future__ import print_function
from setuptools import setup, find_packages, Command
from setuptools.command.sdist import sdist
from setuptools.command.build_py import build_py
from setuptools.command.egg_info import egg_info
from subprocess import check_call
import os
import sys
import platform

here = os.path.dirname(os.path.abspath(__file__))
node_root = os.path.join(here, 'js')
is_repo = os.path.exists(os.path.join(here, '.git'))

npm_path = os.pathsep.join([
    os.path.join(node_root, 'node_modules', '.bin'),
                os.environ.get('PATH', os.defpath),
])

from distutils import log
log.set_verbosity(log.DEBUG)
log.info('setup.py entered')
log.info('$PATH=%s' % os.environ['PATH'])

LONG_DESCRIPTION = 'A Jupyter extension for the next-generation of AISpace'

version_ns = {}
with open(os.path.join(here, 'aispace2', '_version.py')) as f:
    exec(f.read(), {}, version_ns)

setup_args = {
    'name': 'aispace2',
    'version': version_ns['__version__'],
    'description': 'A Jupyter extension for the next-generation of AISpace',
    'long_description': LONG_DESCRIPTION,
    'include_package_data': True,
    'data_files': [
        ('share/jupyter/nbextensions/aispace2', [
            'aispace2/static/extension.js',
            'aispace2/static/index.js',
        ]),
    ],
    'install_requires': [
        'ipywidgets>=7.0.0',
        'matplotlib>=2.0.0'
    ],
    'packages': find_packages(),
    'zip_safe': False,
    'cmdclass': {
    },

    'author': 'AISpace2',
    'author_email': 'info@aispace.org',
    'url': 'https://aispace2.github.io/AISpace2/',
    'keywords': [
        'ipython',
        'jupyter',
        'widgets',
        'artifical intelligence',
        'education'
    ],
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Framework :: IPython',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Multimedia :: Graphics',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
}

setup(**setup_args)
