#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import OpenPattern as OP
import numpy as np

# create a pattern instance
myPattern = OP.Pattern(figPATH="../samplePatterns", frmt="svg")

# define points
A = OP.Point([0, 0])
B = OP.Point([20, 0])
C = OP.Point([20, 15])
D = OP.Point([5, 15])

# add a dart between C and D
E = OP.Point([12.5, 8])
I1, I2 = myPattern.add_dart(E, C, D, 2)

# add the hip point somewhere between A and D
H = OP.Point([2, 10])

# draw a curved fit between DHA
# beware that the order of the points is important !
curve_distance, curve_points = myPattern.pistolet([D, H, A], tot=True)

# add the points to your pattern
myPattern.add_point("A", A)
myPattern.add_point("B", B)
myPattern.add_point("C", C)
myPattern.add_point("D", D)
myPattern.add_point("E", E)
myPattern.add_point("I1", I1)
myPattern.add_point("I2", I2)
myPattern.add_point("H", H)
# prepare drawing
# organize vertices
myPattern.Front_vertices = (
    [A.pos(), B.pos(), C.pos(), I2.pos(), E.pos(), I1.pos(), D.pos()]
    + curve_points
    + [A.pos()]
)

# add legends
myPattern.set_grainline(OP.Point([8, 10]), 8, -np.pi / 2)
myPattern.set_fold_line(C - [0, 2], B + [0, 2], "right")
myPattern.add_comment(OP.Point([12.5, 15.5]), "TOP", 0)
myPattern.add_comment(
    OP.Point(
        [
            10,
            -0.5,
        ]
    ),
    "BOTTOM",
    0,
)


a = 70
# workaround for notches
myPattern.add_comment(
    OP.Point(
        [
            2.8,
            8,
        ]
    ),
    "VV",
    a * np.pi / 180,
)
# draw
myPattern.draw(save=True, fname="simple_scripts_2-2")
plt.show()

# done !
