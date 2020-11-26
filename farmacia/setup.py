import sys

from ast import literal_eval
from setuptools import setup

VERSION = '0.1.0'

PACKAGES = [
    'farmacia',
]

SCRIPTS = []

REQUIREMENTS = 'requirements.json'

DEPENDENCIES = literal_eval(open(REQUIREMENTS, 'r', encoding='utf-8').read())

setup(
    name='farmacia',
    python_requires=DEPENDENCIES['python'],
    version=VERSION,
    author='',
    author_email='',
    packages=PACKAGES,
    scripts=SCRIPTS,
    description='Scrapers de propriedades de farmacos desenvlvido como projeto de TCC',
    long_description=open('README.rst', 'r', encoding='utf-8').read(),
    install_requires=[' >= '.join([kv, DEPENDENCIES['packages'][kv]])
                      for kv in DEPENDENCIES['packages']],
    entry_points = {'scrapy': ['settings = farmacia.settings']}
)
