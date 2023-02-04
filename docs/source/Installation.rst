Installation
============

Requirements
------------

OpenPattern is a python 3 library, hence works on any machine as
long as you have a working distribution.

OpenPattern also requires the following libraries to work properly.

- matplotlib
- numpy
- scipy
- json
- sqlite3

The two last libraries are embedded in the standard library so
they should be installed with any python installation.


Installation
------------

To install the library you must first

- clone the Github directory https://github.com/fmetivier/OpenPattern.git somewhere on your computer
- open a terminal in the root directory
- run the follwing code

.. code-block:: command

  python3 setup.py install.

.. warning::
  sudo / administrator rights may be needed depending on your  computer configuration.

As said before OpenPattern comes with an sqlite3 ``measurements.db`` database.
This base contains a set of standard French and Italian sizes.
