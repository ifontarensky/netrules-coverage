.. highlight:: sh

*************************
Download and Installation
*************************

Overview
========

 0. Install `Python 3.4+ <https://www.python.org/downloads/>`_.
 1. `Download and install netrules-coverage. <#installing-netrules-coverage-v0-x>`_
 2. `Follow the platform-specific instructions (dependencies) <#platform-specific-instructions>`_.
 3. (Optional): `Install additional software for special features <#optional-software-for-special-features>`_.
 4. Run NetRules-Coverage with root privileges.

Each of these steps can be done in a different way depending on your platform.


Installing netrules-coverage v0.x
=================================

The following steps describe how to install (or update) NetRules-Coverage itself.
Dependent on your platform, some additional libraries might have to be installed to make it actually work.
So please also have a look at the platform specific chapters on how to install those requirements.

.. note::

   The following steps apply to Unix-like operating systems (Linux, BSD, Mac OS X).
   For Windows, see the  `special chapter <#windows>`_ below.

Make sure you have Python installed before you go on.

Latest release
--------------

.. note::
   To get the latest versions, with bugfixes and new features, but maybe not as stable, see
   the `development version <#current-development-version>`_.



You can also download the `latest version <https://github.com/ifontarensky/netrules-coverage/archive/master.zip>`_ to a
temporary directory and install it in the standard `distutils <http://docs.python.org/inst/inst.html>`_ way::

$ cd /tmp
$ wget --trust-server-names https://github.com/ifontarensky/netrules-coverage/archive/master.zip   # or wget -O master.zip https://github.com/ifontarensky/netrules-coverage/archive/master.zip
$ unzip master.zip
$ cd master
$ sudo python setup.py install

Current development version
----------------------------

.. index::
   single: Git, repository

If you always want the latest version with all new features and bugfixes, use NetRules-Coverage's Git repository:

1. Install the Git version control system. For example, on Debian/Ubuntu use::

      $ sudo apt-get install git

   or on OpenBSD::

      $ doas pkg_add git

2. Check out a clone of NetRules-Coverage's repository::

   $ git clone https://github.com/ifontarensky/netrules-coverage.git

3. Install NetRules-Coverage in the standard distutils way::

   $ cd netrules-coverage
   $ sudo python setup.py install

Then you can always update to the latest version::

   $ git pull
   $ sudo python setup.py install

