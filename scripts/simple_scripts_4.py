#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import OpenPattern as OP
import numpy as np

# create a pattern instance
# mfs = my first skirt
# W8C  = Women / 8 year / Chiappetta
frmt = "svg"
figPATH = "../samplePatterns"
mfs = OP.Pattern("W8C", figPATH=figPATH, frmt=frmt)

# size of the dart and ease to be applied
pince = 7.25
ease = 8

# basic points
# note the way measurements are called
A = OP.Point([0, mfs.m["hauteur_taille_genou"] - 4])
B = A + OP.Point([(mfs.m["tour_bassin"] + ease) / 2, 0])
C = OP.Point([0, 0])
D = C + OP.Point([(mfs.m["tour_bassin"] + ease) / 2, 0])

A1 = A + OP.Point([0, -mfs.m["hauteur_bassin"]])
B1 = A1 + OP.Point([(mfs.m["tour_bassin"] + ease) / 2, 0])

A2 = A + OP.Point([0, -1])
B2 = B + OP.Point([0, -0.5])

F = mfs.middle(A, B)
E = mfs.middle(C, D)

G = A + OP.Point([mfs.m["tour_taille"] / 4 + 2, 0])
H = B + OP.Point([-mfs.m["tour_taille"] / 4 - 2, 0])

# we need two control points for the french curve because we need at lease three
# add one point between A1 and B1
C1 = mfs.middle(A1, B1)
# add a second just upp by one cm to control the tangents
C2 = C1 + OP.Point([0, -1])
# get the curves
points_skirt_front = [H, C1, C2]
dbskirt_f, skirt_front_side = mfs.pistolet(points_skirt_front, 2, tot=True)
points_skirt_back = [G, C1, C2]
dbskirt_b, skirt_back_side = mfs.pistolet(points_skirt_back, 2, tot=True)

# back dart
dart1 = A + OP.Point([mfs.distance(A, G) / 2, -pince])
I1, I2 = mfs.add_dart(dart1, A2, G, 2)
# front dart
dart2 = B + OP.Point([-mfs.distance(B, H) / 2, -pince])
I3, I4 = mfs.add_dart(dart2, B2, H, 2)

# dics and lists
key = ["A", "A1", "A2", "dart1", "G", "C"]
val = [A, A1, A2, dart1, G, C]

for i in range(len(key)):  # add points to the dictionnary
    mfs.add_point(key[i], val[i], dic="back")


key = ["B", "B1", "B2", "dart2", "H", "F", "E", "D"]
val = [B, B1, B2, dart2, H, F, E, D]

for i in range(len(key)):  # add points to the dictionnary
    mfs.add_point(key[i], val[i], dic="front")

mfs.Back_vertices = [
    [A2.pos(), I1.pos(), dart1.pos(), I2.pos(), G.pos()]
    + skirt_back_side
    + [E.pos(), C.pos()]
]
mfs.Front_vertices = [
    [B2.pos(), I4.pos(), dart2.pos(), I3.pos(), H.pos()]
    + skirt_front_side
    + [E.pos(), D.pos()]
]


# add legends
mfs.set_grainline(OP.Point([8, 15]), 8, -np.pi / 2)
mfs.set_fold_line(A1 - [0, 2], C + [0, 2], "left")
mfs.set_fold_line(B1 - [0, 2], D + [0, 2], "right")
mfs.add_labelled_line(A, B, "WAIST LINE", "t")
mfs.add_labelled_line(A1, B1, "HIP LINE", "t")
mfs.add_comment(mfs.middle(C, E) + [0, 2], "BACK", 0)
mfs.add_comment(mfs.middle(E, D) + [0, 2], "FRONT", 0)

# draw  the pattern
mfs.draw(save=True, fname="simple_scripts_4")
plt.show()

# done !
