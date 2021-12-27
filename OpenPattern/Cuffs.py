#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append('./..')

import matplotlib.pyplot as plt
import numpy as np
import json

from scipy.interpolate import splprep,  splev
from matplotlib.patches import Polygon, PathPatch
from matplotlib.path import Path
from matplotlib.backends.backend_pdf import PdfPages

from OpenPattern.Pattern import Pattern
from OpenPattern.Points import Point


class Cuffs(Pattern):
	"""
	Class to calculate cuff pattern

	styles available: Simple, French
	"""

	def __init__(self, pname = "sophie", gender = 'w', style = 'Gilewska', age = 12, cuff_style = 'Simple',\
		overlap = 2, width = 7, ease = 3 ):

		Pattern.__init__(self,pname, gender)

		self.style = style
		self.Cuff_style = cuff_style
		self.Cuffs_dic = []
		self.Cuffs_vertices = []
		self.Cuffs_segments = {}

		self.calculate_cuffs(overlap, width, ease)

	def calculate_cuffs(self, overlap = 2, width = 5, ease = 3):

		if self.style == 'Gilewska':
			if self.gender in ('M','m'):
				self.calculate_cuffs_gilewska_m(overlap, width, ease)

	def calculate_cuffs_gilewska_m(self, overlap = 2, width = 5, ease = 3):
		"""

		C: Cuff
		O: Overlap
		B: Buttonhole
		l, r : left, right
		u, d, m : up, down, middle

		"""
		if self.Cuff_style == 'Simple':
			Cld = Point([0,0])
			Clm = Cld + [0,width]
			Clu = Cld + [0,2*width]
			Olu = Clu + [self.m["tour_poignet"] + ease, 0]
			Olm = Olu + [0, -width]
			Oru = Olu + [overlap, 0]
			Ord = Oru + [0, -2*width]
			Old = Ord + [-overlap, 0]

			Orm = Oru - [0, width]
			Bru = Orm + [-overlap/2,width/2]
			Brd = Orm + [-overlap/2,-width/2]

			self.Cuffs_dic.append( {'Cld': Cld, 'Clu': Clu, 'Olu': Olu, 'Oru': Oru, 'Ord': Ord, 'Old': Old} )
			self.Cuffs_vertices.append( [Cld.pos(), Clu.pos(), Oru.pos(), Ord.pos(), Cld.pos()] )
			#~ print(self.Cuffs_vertices)
			self.Cuffs_segments = {'Fold': [Clm, Olm], 'Overlap': [Olu, Old], 'Bru': [Bru, Bru - [0,1]],\
			'Brd': [Brd, Brd + [0,1]]}

		elif self.Cuff_style == 'French':

			Cld = Point([0,0])
			Clm = Cld + [0, width+2]
			Clu = Clm + [0, width]
			Olu = Clu + [overlap, 0]
			Oru = Olu + [self.m["tour_poignet"]+ease,0]
			Cru = Oru + [overlap, 0]
			Crm = Cru - [0, width]
			Crd = Crm - [0, (width+2)]
			Ord = Crd - [overlap, 0]
			Old = Ord - [(self.m["tour_poignet"]+ease), 0]

			Blu = Clm + [overlap/2,width/2]
			Bld = Clm + [overlap/2,-width/2]
			Bru = Crm + [-overlap/2,width/2]
			Brd = Crm + [-overlap/2, -width/2]

			self.Cuffs_dic.append( {'Cld': Cld, 'Clu': Clu, 'Olu': Olu, 'Oru': Oru, 'Ord': Ord, 'Old': Old, 'Crd': Crd, 'Cru': Cru } )
			self.Cuffs_vertices.append( [Cld.pos(), Clu.pos(), Cru.pos(), Crd.pos(), Cld.pos()] )
			self.Cuffs_segments = {'Cuff_Fold': [Clm, Crm], 'L_Overlap': [Olu, Old], 'R_Overlap': [Oru, Ord], 'Fabric_Fold': [Cld,Crd],\
			'Blu': [Blu, Blu - [0,1]], 'Bru': [Bru, Bru - [0,1]], 'Bld': [Bld, Bld + [0,1]], 'Brd': [Brd, Brd + [0,1]]}

	def draw_cuffs(self,save = False):

		fig, ax = self.draw_pattern(self.Cuffs_dic,self.Cuffs_vertices)

		for key, val in self.Cuffs_segments.items():
			lbl_pos = self.middle(val[0],val[1])
			kwdic = {'color': 'blue', 'linestyle':'dashed', 'alpha':0.5}
			self.segment(val[0], val[1], ax, kwdic)
			angle = self.segment_angle(val[0],val[1])*180/np.pi
			ax.text(lbl_pos.x, lbl_pos.y, key, rotation = angle)

		if save:

			of = '../patterns/'+ 'cuff_' + self.style + '_' + self.Cuff_style + '_' + self.pname +'_FullSize.pdf'

			plt.savefig(of)


		return fig, ax
