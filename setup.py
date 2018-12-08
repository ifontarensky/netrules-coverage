#!/usr/bin/env python
#
# Author:   Ivan Fontarensky <ivan.fontarensky at gmail.com>
#
# For license information, see LICENSE
#
# ID: setup.py [] ivan.fontarensky at gmail.com $

##########################################################################
## Imports
##########################################################################

import os
import codecs

from setuptools import setup
from setuptools import find_packages

##########################################################################
## Package Information
##########################################################################

## Basic information
NAME         = "netrules-coverage"
DESCRIPTION  = "This package is used to test network probes from a test book."
AUTHOR       = "Ivan Fontarensky"
EMAIL        = "ivan.fontarensky@gmail.com"
LICENSE      = "License GPL v3"
PACKAGE      = "netrules_coverage"
REPOSITORY   = "https://github.com/ifontarensky/netrules-coverage"

## Define the keywords
KEYWORDS     = (
    'ids', 'test', 'rules'
)

## Define the classifiers
## See https://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS  = (
    "Programming Language   ::  Python  ::  3.7",
    "Natural Language   ::  English",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Topic :: Security",
    "Topic :: System :: Networking",
    "Topic :: System :: Networking :: Monitoring",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Intended Audience :: Information Technology",
    "Intended Audience :: Science/Research",
    "Intended Audience :: System Administrators",
    "Intended Audience :: Telecommunications Industry"
)

## Important Paths
PROJECT      = os.path.abspath(os.path.dirname(__file__))
REQUIRE_PATH = "docs/requirements.txt"
VERSION_PATH = os.path.join(PACKAGE, "version.py")
PKG_DESCRIBE = "docs/DESCRIPTION.rst"

## Directories to ignore in find_packages
EXCLUDES     = (
    "tests", "docs"
)

ENTRYPOINT = {}

SCRIPTS = []

##########################################################################
## Helper Functions
##########################################################################

def read(*parts):
    """
    Assume UTF-8 encoding and return the contents of the file located at the
    absolute path from the REPOSITORY joined with *parts.
    """
    with codecs.open(os.path.join(PROJECT, *parts), 'rb', 'utf-8') as f:
        return f.read()


def get_version(path=VERSION_PATH):
    """
    Reads the version.py defined in the VERSION_PATH to find the get_version
    function, and executes it to ensure that it is loaded correctly.
    """
    namespace = {}
    exec(read(path), namespace)
    return namespace['get_version']()


def get_requires(path=REQUIRE_PATH):
    """
    Yields a generator of requirements as defined by the REQUIRE_PATH which
    should point to a requirements.txt output by `pip freeze`.
    """
    for line in read(path).splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            yield line

##########################################################################
## Define the configuration
##########################################################################

config = {
    "name": NAME,
    "version": get_version(),
    "description": DESCRIPTION,
    "long_description": read(PKG_DESCRIBE),
    "license": LICENSE,
    "author": AUTHOR,
    "author_email": EMAIL,
    "maintainer": AUTHOR,
    "maintainer_email": EMAIL,
    "include_package_data": True,
    "url": REPOSITORY,
    "download_url": "{}/tarball/v{}".format(REPOSITORY, get_version()),
    "packages": find_packages(where=PROJECT, exclude=EXCLUDES),
    "install_requires": list(get_requires()),
    "classifiers": CLASSIFIERS,
    "keywords": KEYWORDS,
    "zip_safe": False,
    "entry_points": ENTRYPOINT,
    "scripts": SCRIPTS
}

##########################################################################
## Run setup script
##########################################################################

if __name__ == '__main__':
    setup(**config)