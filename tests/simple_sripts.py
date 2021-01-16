#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('./..')

import matplotlib.pyplot as plt
import OpenPattern as OP
import numpy as np

# create a pattern instance
myPattern = OP.Pattern()

#define points
A = OP.Point([0,0])
B = OP.Point([10,0])
C = OP.Point([10,10])
D = OP.Point([0,10])

#add them to you
myPattern.add_point('A',A)
myPattern.add_point('B',B)
myPattern.add_point('C',C)
myPattern.add_point('D',D)

E = OP.Point([5,5])

myPattern.add_point('E',E)


myPattern.Front_vertices = [A.pos(), B.pos(), C.pos(), E.pos(), D.pos(), A.pos()]
myPattern.draw_pattern([myPattern.Front_dic],[myPattern.Front_vertices])


plt.show()
