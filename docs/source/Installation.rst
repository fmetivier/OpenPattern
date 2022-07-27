Installation
============

Requirements
------------

OpenPattern is a python 3 library, hence works on any machine as long as you have a working distribution.

OpenPattern also requires the following libraries to work properly.
* matplotlib
* numpy
* scipy
* json
* sqlite3

If you want to have a direct access the measurements
database from the terminal you'll have to install the sqlite3 engine.

Installation
------------

To install the library you must first
* clone the directory somewhere on your computer
* open a terminal in the root directory
* run the follwin code

.. code-block:: command

  python3 setup.py install.

.. warning::
  sudo / administrator rights may be needed depending on your computer configuration.

As said before OpenPattern comes with an sqlite3 ``measurements.db`` database. This base contains a set of standard French and Italian sizes.

By default OpenPattern assumes that this file resides in the *same directory*
as your scripts. This is the simplest way to start rapidly.
Yet you can place it anywhere and tell OpenPattern where to search
for it.
