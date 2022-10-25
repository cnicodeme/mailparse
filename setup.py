# -*- config:utf-8 -*-

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from codecs import open
from os import path
import re

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'mailparse/__version__.py'), encoding='utf-8') as fp:
    try:
        version = re.findall(
            r"^__version__ = \"([^']+)\"\r?$", fp.read(), re.M
        )[0]
    except IndexError:
        raise RuntimeError("Unable to determine version.")

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='mailparse',
    version=version,
    license='MIT',
    description='Encode raw emails into Python dict objects and build raw emails from Python dict.',
    long_description_content_type='text/markdown',
    long_description=long_description,
    url='https://github.com/cnicodeme/mailparse',
    author='Cyril Nicodeme',
    author_email='contact@cnicodeme.com',
    keywords='mail email parse parser encode decode encoder decoder eml',
    project_urls={
        # 'Official Website': 'https://github.com/cnicodeme/mailparse',
        # 'Documentation': 'https://github.com/cnicodeme/mailparse',
        'Source': 'https://github.com/cnicodeme/mailparse',
    },
    packages=find_packages(),
    platforms='any',

    # For a list of valid classifiers, see
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',

        'Topic :: Communications :: Email',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Text Processing',

        'License :: OSI Approved :: MIT License',

        "Operating System :: OS Independent",
        "Programming Language :: Python",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: PyPy",
    ]
)
