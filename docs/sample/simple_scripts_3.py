#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('/home/metivier/Nextcloud/Personnel/couture/OpenPattern')

import matplotlib.pyplot as plt
import OpenPattern as OP
import numpy as np

# create a pattern instance
myPattern = OP.Pattern()

# define points
A = OP.Point([0,0])
B = OP.Point([20,0])
C = OP.Point([20,15])
D = OP.Point([5,15])

# add a dart between C and D
E = OP.Point([12.5,8])
I1,I2 = myPattern.add_dart(E,C,D,2)

# add the points to your pattern
myPattern.add_point('A',A)
myPattern.add_point('B',B)
myPattern.add_point('C',C)
myPattern.add_point('D',D)
myPattern.add_point('E',E)
myPattern.add_point('I1',I1)
myPattern.add_point('I2',I2)

# prepare drawing
# organize vertices
myPattern.Front_vertices = [A.pos(), B.pos(), C.pos(), I2.pos(), E.pos(),\
    I1.pos(), D.pos(), A.pos()]

# add legends
myPattern.set_grainline(OP.Point([8,10]), 8, -np.pi/2)
myPattern.set_fold_line(C-[0,2], B+[0,2],'right')
myPattern.add_comment(OP.Point([12.5,15.5]),'TOP',0)
myPattern.add_comment(OP.Point([10,-0.5,]),'BOTTOM',0)


a = 70
myPattern.add_comment(OP.Point([2.8,8,]),'VV',a*np.pi/180) # workaround for notches

# draw
# here comes the new part
# create a figure and an axes
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])

# copy and translate/rotate  myPattern
# then add the new pattern to myPattern list of patterns
P2 = myPattern.copy()
P2.translate(30,0)
myPattern.add_pattern(P2)

P3 = myPattern.copy()
P3.translate(0,30)
P3.rotate(P3.Front_dic['E'].copy(),np.pi/2)
myPattern.add_pattern(P3)

P4 = myPattern.copy()
P4.rotate(P4.Front_dic['A'].copy(), np.pi/4)
P4.translate(35,30)
myPattern.add_pattern(P4)

# draw the subpatterns onf fig,ax
f, a  = myPattern.draw_subpatterns(fig, ax, overlay = True)
# in the end draw mypattern on top of it
myPattern.draw(save=True, fname='simple_scripts_3', ifig = f, iax = a)

plt.show()

# done !
