Installation
============

Requirements
------------

OpenPattern requires the following libraries to work properly.
* matplotlib
* numpy
* scipy
* json
* sqlite3

If you want to access the measurements database from the terminal
or some GUI you'll have to install the sqlite3 engine

Installation
------------

To install the library you must first
* clone the directory somewhere on your computer
* open a terminal in the root directory
* run ``python3 setup.py install``.
sudo rights may be needed depending on your computer configuration.

OpenPattern comes with an sqlite3 ``measurements.db`` database. This base contains a set of standard French and Italian sizes.

By default OpenPattern assumes that this file resides in the *same directory* as your scripts. This is the simplest way to start rapidly. Yet you can place it anywhere and tell OpenPattern where to search for it (see the doc for more informations).
