#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append('./..')

from OpenPattern.Pattern import *
from OpenPattern.Points import *
from OpenPattern.Bodices import *


class Hospital_Gown(Pattern):
	def __init__(self, style='Adapted from Sabrina Lafon'):

		Pattern.__init__(self)
		pass

		self.style = style
		self.gender='M/W'
		self.pname='~L'

		self.Gown_points_dic = []
		self.Gown_vertices = []
		self.Sleeve_points_dic = []
		self.Sleeve_vertices = []

		self.cal_gown()
		self.cal_sleeves()


	def cal_gown(self):

		dx = 3 #2x1.5 seam

		HipF = Point([0,0])

		HipB = HipF + [65+dx,0]
		HipFoldB = HipB + [-2,0]


		CB = HipB+ [0,108]
		HipFoldC = CB + [-2,0]

		CB2 = CB + [-13,0]
		ShB = CB2 + [-19.5,-3]

		SlB = ShB + [0,-30]
		HipSlB = Point([SlB.x,0])

		ShF = ShB + [-dx,0]
		SlF = SlB + [-dx,0]
		HipSlF = Point([SlF.x,0])


		CF2 = ShF + [-20,+3]
		CF = CF2 + [-13,-8]
		Control = CF + [2,0]
		BeltF = CF + [0,-37]
		BeltB = BeltF + [4,0]

		points_col = [CF2, Control, CF ]
		dbcol, col = self.pistolet(points_col, 2, tot = True)

		self.Gown_points_dic.append({'HipF':HipF, 'HipB': HipB, 'CB': CB, 'CB2':CB2, 'ShB':ShB, 'SlB':SlB, 'ShF':ShF, 'SlF':SlF, 'CF':CF, 'CF2':CF2, 'BF':BeltF, 'BB':BeltB, 'HFB':HipFoldB, 'HFC':HipFoldC, 'HipSlF':HipSlF, 'HipSlB':HipSlB })

		self.Gown_vertices.append([HipSlB.pos,HipB.pos,CB.pos,CB2.pos, ShB.pos])
		self.Gown_vertices.append([HipF.pos, HipSlF.pos, SlF.pos, ShF.pos, CF2.pos] + col + [HipF.pos])


	def cal_sleeves(self):


		a = np.arctan(3/20)

		SC = Point([0,0])
		SF = SC + [30*np.cos(a), 30*np.sin(a)]
		SB = SC + [-30*np.cos(a), 30*np.sin(a)]

		WC= SC + [0,60]
		WF = WC + [20,0]
		WB = WC + [-20,0]

		self.Sleeve_points_dic.append({'SF':SF,'SC':SC, 'SB':SB, 'WC':WC, 'WF':WF, 'WB':WB})
		self.Sleeve_vertices.append([SC.pos,SF.pos,WF.pos,WB.pos,SB.pos,SC.pos])



	def draw_sleeves(self, dic = {"Pattern":"Hospital Gown"}, save = False, fname = None, paper='FullSize'):

		fig, ax = self.draw_pattern(self.Sleeve_points_dic, self.Sleeve_vertices)

		spd = self.Sleeve_points_dic[0]
		self.segment(spd['WC'],spd['SC'],ax,{'color':'blue','linestyle':'dashed','alpha':0.5})
		self.segment(spd['SF'],spd['SB'],ax,{'color':'blue','linestyle':'dashed','alpha':0.5})

		ax.text(spd['WC'].x, spd['WC'].y+1, 'CUFF', ha='center')
		ax.text(spd['SC'].x, spd['SC'].y-2, 'SHOULDER', ha='center')
		if save:
			if fname:
				pass
			else:
				fname = 'Hospital_Gown_Sleeve'

			of = '../patterns/'+ self.style + '_' + fname + '_' + self.pname +'_FullSize.pdf'

			plt.savefig(of)

			if paper != 'FullSize':
				self.paper_cut(fig, ax, name = fname, paper = paper)


		return fig, ax


	def draw_gown(self, dic = {"Pattern":"Hospital Gown"}, save = False, fname = None, paper='FullSize'):

		# 1 draw
		fig, ax = self.draw_pattern(self.Gown_points_dic, self.Gown_vertices)

		# 2 print heading
		ax = self.print_info(ax, dic)


		ax = self.add_legends(ax)

		if save:
			if fname:
				pass
			else:
				fname = 'Hospital_Gown'

			of = '../patterns/'+ self.style + '_' + fname + '_' + self.pname +'_FullSize.pdf'

			plt.savefig(of)

			if paper != 'FullSize':
				self.paper_cut(fig, ax, name = fname, paper = paper)

		return fig, ax

	def add_legends(self, ax):
		"""Adds common legends to the Bodice pattern

		Args:
			ax on which to plot

		Returns:
			ax
		"""

		bpd = self.Gown_points_dic[0]
		fs=14

		pos = self.middle(bpd['HipF'], bpd['CF'])
		ax.text(pos.x- 0.5, pos.y, 'FOLD LINE', fontsize=fs, rotation = 90)


		ldic={'color':'blue', 'alpha':0.4, 'linestyle':'dashed'}

		self.segment(bpd['ShF'], bpd['SlF'], ax, ldic)
		pos = self.middle(bpd['ShF'], bpd['SlF'])
		ax.text(pos.x, pos.y+0.5, 'Armhole', rotation=90, fontsize=fs, ha='center')

		self.segment(bpd['ShB'], bpd['SlB'], ax, ldic)
		pos = self.middle(bpd['ShB'], bpd['SlB'])
		ax.text(pos.x, pos.y+0.5, 'Armhole', rotation=90, fontsize=fs, ha='center')

		self.segment(bpd['BB'], bpd['BF'], ax, ldic)
		pos = self.middle(bpd['BB'], bpd['BF'])
		ax.text(pos.x, pos.y+1.5, 'belt', fontsize=fs, ha='center')

		self.segment(bpd['HFB'], bpd['HFC'], ax, ldic)
		pos = self.middle(bpd['HFB'], bpd['HFC'])
		ax.text(pos.x- 0.5, pos.y, 'Gown Limit', fontsize=fs, rotation = 90)

		ax.text(15,30,'FRONT',fontsize=fs, ha='center')
		ax.text(45,30, 'BACK',fontsize=fs, ha='center')

		return ax
