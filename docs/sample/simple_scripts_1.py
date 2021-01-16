#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('/home/metivier/Nextcloud/Personnel/couture/OpenPattern')

import matplotlib.pyplot as plt
import OpenPattern as OP
import numpy as np

# create a pattern instance
myPattern = OP.Pattern()

#define points
A = OP.Point([0,0])
B = OP.Point([20,0])
C = OP.Point([20,15])
D = OP.Point([5,15])

# add a dart between C and D
E = OP.Point([12.5,8])
I1,I2 = myPattern.add_dart(E,C,D,2)

#add the points to your pattern
myPattern.add_point('A',A)
myPattern.add_point('B',B)
myPattern.add_point('C',C)
myPattern.add_point('D',D)
myPattern.add_point('E',E)
myPattern.add_point('I1',I1)
myPattern.add_point('I2',I2)

#prepare drawing
myPattern.Front_vertices = [A.pos(), B.pos(), C.pos(), I2.pos(), E.pos(),I1.pos(), D.pos(), A.pos()]

#draw
myPattern.draw(save=True, fname='simple_scripts_1')
plt.show()

#done !
