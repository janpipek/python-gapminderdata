"""
TODO: Write this
"""

import itertools
from setuptools import setup, find_packages

VERSION = "0.0.1"

# TODO: Perhaps rename the package before registering with pypi
#   and make it support full ddf

options = dict(
    name='gapminderdata',
    version=VERSION,
    packages=find_packages(),
    # package_data={'': ['LICENSE', 'MANIFEST.in', 'README.md', 'HISTORY.txt']},
    license='MIT',
    description='Downloader and proxy to Gapminder data',
    long_description=__doc__.strip(),
    author='Jan Pipek',
    author_email='jan.pipek@gmail.com',
    url='https://github.com/janpipek/python-gapminderdata',
    install_requires = ['requests', 'pandas'],
    python_requires="~=3.6",
    extras_require = {
        # 'all' : []
    },
    entry_points = {
        'console_scripts' : [
        ]
    },
)

extras = options['extras_require']
extras['full'] = list(set(itertools.chain.from_iterable(extras.values())))
setup(**options)
