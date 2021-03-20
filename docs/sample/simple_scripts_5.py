#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('/home/metivier/Nextcloud/Personnel/couture/OpenPattern')

import matplotlib.pyplot as plt
import OpenPattern as OP
import numpy as np

# create a pattern instance
P1 = OP.Pattern()

# define points
A = OP.Point([0,0])
B = OP.Point([20,0])
C = OP.Point([20,15])
D = OP.Point([5,15])

# add a dart between C and D
E = OP.Point([12.5,8])
I1,I2 = P1.add_dart(E,C,D,2)

# add the points to your pattern
P1.add_point('A',A)
P1.add_point('B',B)
P1.add_point('C',C)
P1.add_point('D',D)
P1.add_point('E',E)
P1.add_point('I1',I1)
P1.add_point('I2',I2)

# prepare drawing
P1.Front_vertices = [[A.pos(), B.pos(), C.pos(), I2.pos(), E.pos(),\
    I1.pos(), D.pos(), A.pos()]]

#Mirror the pattern to unfold it
du, vu = P1.unfold(P1.Front_dic,P1.Front_vertices[0],P1.Front_dic['C'],P1.Front_dic['B'])

P1.Front_vertices.append(vu)
for key,val in du.items():
    P1.add_point(key,val)


# draw the unfolded pattern
P1.draw(save=True, fname='simple_scripts_5')
plt.show()

# done !
