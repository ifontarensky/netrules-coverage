#!/usr/bin/env python
#
# Author:   Ivan Fontarensky <ivan.fontarensky at gmail.com>
#
# For license information, see LICENSE
#
# ID: setup.py [] ivan.fontarensky at gmail.com $

"""
Stores version information such that it can be read by setuptools.
"""

##########################################################################
## Module Info
##########################################################################

__version_info__ = {
    'major': 0,
    'minor': 1,
    'micro': 0,
    'releaselevel': 'alpha',
    'serial': 1,
}


def get_version(short=False):
    """
    Computes a string representation of the version from __version_info__.
    """
    assert __version_info__['releaselevel'] in ('alpha', 'beta', 'final')
    vers = ["%(major)i.%(minor)i" % __version_info__, ]
    if __version_info__['micro']:
        vers.append(".%(micro)i" % __version_info__)
    if __version_info__['releaselevel'] != 'final' and not short:
        vers.append('%s%i' % (__version_info__['releaselevel'][0],
                              __version_info__['serial']))


def increment_dev():
    serial = __version_info__['serial'] + 1
    with open(__file__, 'r') as h:
        content = h.read().replace("'serial': %d" % __version_info__['serial'], "'serial': %d" % serial)
    with open(__file__, 'w') as h:
        h.write(content)