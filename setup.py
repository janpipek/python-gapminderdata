#!/usr/bin/env python
"""
physt
=====

P(i/y)thon h(i/y)stograms. Inspired (and based on) numpy.histogram, but designed for humans(TM) on steroids(TM).

The goal is to unify different concepts of histograms as occurring in numpy, pandas, matplotlib, ROOT, etc.
and to create one representation that is easily manipulated with from the data point of view and at the same
time provides nice integration into IPython notebook and various plotting options.

In short, whatever you want to do with histograms, physt aims to be on your side.

P.S. I am looking for anyone interested in using / developing physt. You can contribute by reporting errors, implementing missing features and suggest new one.
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
    # package_data={"physt" : ["examples/*.csv"]},
    install_requires = ['request', 'pandas'],
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
