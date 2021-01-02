#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append('./..')

from OpenPattern.Pattern import *
from OpenPattern.Points import *

class Placket(Pattern):
	"""
	Sleeve placket and underlap (if wanted)

	"""
	def __init__(self, pname = "sophie", gender = 'w', placket_style = 'Simple', slit_length = 10):

		Pattern.__init__(self,pname, gender)

		self.pl = placket_style
		self.sll = slit_length

		self.Placket_dic = []
		self.Placket_vertices = []
		self.Placket_segments = {}

		self.calculate_plackets()

	def calculate_plackets(self):

		if self.pl == 'SimpleOneSide':

			Pbl = Point([0,0])
			Pbm = Pbl + [2,0]
			Pbr = Pbm + [2,0]
			Pur = Pbr + [0, self.sll]
			Pum = Pbm + [0, self.sll]
			Pul = Pbl + [0, self.sll]
			Ptip = Pul + [1,2]

			self.Placket_dic.append({'Pbl':Pbl, 'Pbm': Pbm, 'Pbr': Pbr, 'Pur': Pur, 'Pum':Pum, 'Pul': Pul, 'Ptip': Ptip})
			self.Placket_vertices.append([Pbl.pos(), Pbr.pos(), Pur.pos(), Pum.pos(), Ptip.pos(), Pul.pos(), Pbl.pos()])

			self.Placket_segments = {'Fold': [Pbm, Pum]}

	def draw_placket(self,save = False):

		fig, ax = self.draw_pattern(self.Placket_dic,self.Placket_vertices)

		for key, val in self.Placket_segments.items():
			lbl_pos = self.middle(val[0],val[1])
			kwdic = {'color': 'blue', 'linestyle':'dashed', 'alpha':0.5}
			self.segment(val[0], val[1], ax, kwdic)
			angle = self.segment_angle(val[0],val[1])*180/np.pi
			ax.text(lbl_pos.x, lbl_pos.y, key, rotation = angle)

		if save:

			of = '../patterns/'+ 'placket_' + self.style + '_' + self.Cuff_style + '_' + self.pname +'_FullSize.pdf'

			plt.savefig(of)
