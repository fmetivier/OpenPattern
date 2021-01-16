#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('/home/metivier/Nextcloud/Personnel/couture/OpenPattern')

import matplotlib.pyplot as plt
import OpenPattern as OP
import numpy as np

# 1 create a pattern instance
myPattern = OP.Pattern()

# 2 define points
A = OP.Point([0,0])
B = OP.Point([10,0])
C = OP.Point([10,10])
D = OP.Point([0,10])

# 3 add them to your pattern
myPattern.add_point('A',A)
myPattern.add_point('B',B)
myPattern.add_point('C',C)
myPattern.add_point('D',D)

# 4 prepare drawing
myPattern.Front_vertices = [A.pos(), B.pos(), C.pos(), D.pos(), A.pos()]

# 5 draw
myPattern.draw(save=True, fname='simple_scripts_0')
plt.show()

#done !
