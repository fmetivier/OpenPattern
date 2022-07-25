Classes
=======

Introduction
------------

A pattern is a series of curves and lines that draws the outline
of pieces that must be cut and sewn to create a garment. To these
curve are added control points. In OpenPattern the lines
and curves are saved in lists, control points in dictionaries.


OpenPattern is organized around classes which allow the creation of these points and curves and which inherit one from
others. This structure has the advantage of adhering to the techniques pattern making.
Indeed a shirt, a jacket or a vest are adaptations
from a bodysuit, a dress derives from the assembly of a skirt and a bodysuit,
finally skirts and trousers derive from generic forms called
basics (basic skirt, basic pants).

OpenPattern currently has two levels of inheritance.

- The parent class ``Pattern``: This is the general class that defines a pattern and the methods to drawing and manipulate it.

- Basic classes derived from Pattern: ``Basic_Bodice,Basic_Trousers, Cuffs, Collars``.

- The classes derived from the base classes: shirt, pyjamas etc... which inherit from ``Basic_Bodice`` or ``Basic_Trousers`` etc...

Patterns call a class ``Point`` which allows to
define a pattern point with its position and properties.
This class redefines addition operations and offers various
manipulations such as rotation. The interest here is to have an object
flexible that allows you to start from a basic pattern and alter it.

Finally, a pattern is built from body measurements. These are stored
in a sqlite3 database contained in the ``measurement.db`` file.
This database contains a whole series of standard measurements from the various books mentioned above and can also contain the specific measurements that you will take on your loved ones.



Pattern Class
-------------

  .. automodule:: OpenPattern.Pattern
    :members:


Skirts and Culottes
-------------------

.. automodule:: OpenPattern.Skirts
  :members:

Trousers
--------
.. automodule:: OpenPattern.Trousers
  :members:

Bodices class
-------------

.. automodule:: OpenPattern.Bodices
  :members:


Shirts
------

  .. automodule:: OpenPattern.Shirts
    :members:

Ancillary classes: Plackets, Cuffs and Collars
----------------------------------------------

  .. automodule:: OpenPattern.Collars
    :members:

  .. automodule:: OpenPattern.Cuffs
    :members:

  .. automodule:: OpenPattern.Placket
    :members:


Waistcoats
----------

  .. automodule:: OpenPattern.Waist_Coats
    :members:


Points Classes
--------------

.. automodule:: OpenPattern.Points
  :members:
