Introduction and Purpose
========================


OpenPattern is an object-oriented python library whose purpose is
is to allow the drafing of patterns, in particular of clothing, to
1:1 scale and their export in pdf, svg or any format
compatible with the matplotlib library. The patterns thus constructed
can either be directly printed for use or opened
in drawing softwares like ``Inkscape``.

OpenPattern offers the possibility to create patterns "from scratch",
to use libraries of existing patterns (basic or base patterns
in particular), and to adapt and transform them.
Patterns can be integrated to the library as they are created.


The patterns can be built bespoke from a set
of measurements made on the body of a particular person (I have
created OpenPattern to design clothes for my family), or
constructed from classic ready-to-wear measurements.

The sources I used to draw the patterns come from
classic patronage works. These works, intended for couturiers
amateurs or students of fashion schools, describe the techniques of
realization of what is called the flat cut, that is to say the way
to project and trace on a 2D surface (the paper then the fabric)
3D geometric shape (the finished garment after sewing).


I used the works of four main authors. In
first place I used the four volumes of the series *The model of
fashion* by *Teresa Gilewska*, for women and for men.
I also used the first two volumes of collection *Fashion paterning techniques* by
*Antonnio Donnanno*, for women and men also. For
children and men I used volumes 3 and 4 of *The flat cut* by
*Jacqueline Chiappetta*. Finally for men
I also made incidental use of the book by *Claire Wargnier* on *Male clothing* (See the references section for a complete bibliography).
These works are all worded similarly. They expose,
step by step, the empirical techniques to draw bodysuits,
trousers, shirts etc.


The creation of a pattern can be broken down into a series of instructions such as

- draw a segment AB of length equal to 1/4 of the hip circumference,

- add a 1.5cm dart, 9cm deep, between the dots F1 and H,

- etc...

OpenPattern takes these drafting
principle and techniques almost literally by translating them
into the form of
instructions in python, and adapting them when it turns out
to be necessary.

Unlike existing commercial or free patronage softwares, the
choice made here is to create patterns by means of a script, i.e.
of a series of instructions, and not to draw it with graphical user interface (GUI).
What may seem daunting at first glance
actually offers all the flexibility of a programming language like
python.
