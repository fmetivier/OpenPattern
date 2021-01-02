#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append('./..')

from OpenPattern.Pattern import *
from OpenPattern.Points import *

class Basic_Bodice(Pattern):
	"""
	Class to calculate and draw a basic Bodice pattern.
	For male its more a shirt than a Bodice.
	Inherits from Pattern

	Attributes

		style: style used to draw the pattern as string (Gilewska, Donnanno, Chiappetta for now)

		# Attributes that control the dictionnaries used for size measurements
		age: ade of the kid in Chiapetta's patterns
		gender: gender
		pname: measurements used corresponding to a json file

		# Variables obtained from the basic calculations for Bodices
		# dics used here:

		Bodice_points_dic
		curves_dic

		# lists of vertices:

		Bodice_Back_vertices
		Bodice_Front_vertices

	"""

	def __init__(self, pname="M44G", gender='m', style='Gilewska', age=12, ease=8, hip=True):
		"""
		Initilizes parent class &  attributes
		launches the calculation of bodice and sleeve
		saves measurements performed like armscye depth in the json measurements file for further processing in other classes

		Args:
			pname: size measurements
			gender: ..
			style: style to be used for drafting
			age: used if for a child and style = Chiappetta.
			ease: ease in cm; used in Donnanno patterns
			hip: True/False use to decide for men whether to draw a fullbodice
		"""
		Pattern.__init__(self, pname, gender)

		self.style=style
		self.age=age
		self.hip=hip

		self.dic_list=[]
		self.vertices_list=[]

		self.Bodice_points_dic = {}
		self.Bodice_Front_points_dic = {}
		self.Bodice_Back_points_dic = {}
		self.Sleeve_points_dic = {}

		self.Bodice_Front_vertices = []
		self.Bodice_Back_vertices = []
		self.Sleeve_vertices = []


		# calculate Basic bodice and sleeve
		if self.style == 'Donnanno':
			print("style Donnanno selected")
			if self.gender == 'm':
				self.Donnanno_bodice_without_dart_m(bust_ease = ease)

			elif self.gender == 'w':
				self.Donnanno_bodice_without_dart_w(bust_ease = ease)

		elif self.style == 'Gilewska':
			print("style Gilewska selected")

			if self.gender == 'm':
				self.Gilewska_basic_bodice_m()
				self.Gilewska_basic_sleeve_m()

			elif self.gender == 'w':
				self.Gilewska_basic_bodice_w()
				self.Gilewska_basic_sleeve_w()

		elif self.style == 'Chiappetta':
			print("style Chiappetta selected")
			self.chiappetta_basic_bodice(self.age)

		else:
			print("style %s unknown, using Donnanno instead" % (self.style))
			self.Donnanno_bodice_without_dart()

		self.save_measurements_sql()

	############################################################

	def generate_lists(self):
		"""
		generates a list of point vertices and a list of point dictionnaries for drawing
		this method can only be called by children classes but is common to them

		"""

		vl = [self.Bodice_Front_vertices, self.Bodice_Back_vertices]
		dl = [self.Bodice_points_dic]

		return dl, vl

	def draw_bodice(self, dic = {"Pattern":"Dartless bodice"}, save = False, fname = None, paper='FullSize'):
		""" Draws Basic Bodice with legends and save it if asked for

		Args:
			dic: dictionnary of informations to be printed
			save: if true save to file
			fname: filename
			paper: paper size on which to save (for cuts)

		Returns:
			fig, ax
		"""

		dl, vl = self.generate_lists()

		# 1 draw
		fig, ax = self.draw_pattern(dl, vl)

		# 2 print heading
		ax = self.print_info(ax, dic)

		# 3 print specific drawings
		if self.style == 'Donnanno':
			print("to be done")
		else:
			ax = self.add_legends(ax)

		if save:
			if fname:
				pass
			else:
				fname = 'Basic_Bodice'

			of = '../patterns/'+ self.style + '_' + fname + '_' + self.pname +'_FullSize.pdf'

			plt.savefig(of)

			if paper != 'FullSize':
				self.paper_cut(fig, ax, name = fname, paper = paper)

		return fig, ax

	def draw_sleeves(self, save=False, fname=None, paper='FullSize'):
		"""draws the basic sleeve

		Args:
			save: if true save to file
			fname: filename
			paper: paper size on which to save (for cuts)

		Returns:
			fig, ax
		"""

		#1 draw
		fig, ax = self.draw_pattern([self.Sleeve_points_dic], [self.Sleeve_vertices])

		bl_dic={'color':'blue','linestyle':'dashed','alpha':0.5}

		spd = self.Sleeve_points_dic

		self.segment(spd['A'], Point([0, 0]), ax, bl_dic)

		if self.gender=='w':
			PF = self.middle(spd['W'], spd['W1'])
			ax.text(PF.x, PF.y, 'FRONT', ha='center')

			PB = self.middle(spd['W'], spd['W0'])
			ax.text(PB.x, PB.y, 'BACK', ha='center')

		else:
			x = spd['B'].x
			y = spd['B'].y/2
			ax.text(x+5, y, 'FRONT', ha='left')
			ax.text(x-5, y, 'BACK', ha='right')



		#2 add specific info
		if self.style == 'Gilewska':
			if self.gender == 'm':
				width=self.distance(spd['C'], spd['D'])
				self.segment(spd['C'], spd['D'], ax, bl_dic)
				self.segment(spd['C1'], spd['E'], ax, bl_dic)
				self.segment(spd['F'], spd['D1'], ax, bl_dic)
			elif self.gender == 'w':
				width=self.distance(spd['E'], spd['D'])
				self.segment(spd['E'], spd['D'], ax, bl_dic)
				self.segment(spd['E'], spd['A'], ax, bl_dic)
				self.segment(spd['A'], spd['D'], ax, bl_dic)
		elif self.style == 'Donnanno':
			pass

		#3 add Heading
		ax = self.print_info(ax, {"Sleeve length": round(spd['A'].y,1), "Sleeve width": round(width,1)})

		if save:
			if fname:
				pass
			else:
				fname = 'Basic_Sleeve'

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

		bpd = self.Bodice_points_dic
		fs=14

		pos = self.middle(bpd['WB'], bpd['SlB'])
		ax.text(pos.x- 0.5, pos.y, 'FOLD LINE', fontsize=fs, rotation = 90)

		pos = self.middle(bpd['WF'], bpd['SlF'])
		ax.text(pos.x+ 0.5, pos.y, 'MIDDLE FRONT', fontsize=fs, rotation = 90)

		ldic={'color':'blue', 'alpha':0.4, 'linestyle':'dashed'}

		self.segment(bpd['WF'], bpd['WB'], ax, ldic)
		pos = self.middle(bpd['WF'], bpd['WB'])
		ax.text(pos.x, pos.y+0.5, 'WAIST LINE', fontsize=fs, ha='center')

		self.segment(bpd['SlF'], bpd['SlB'], ax, ldic)
		pos = self.middle(bpd['SlF'], bpd['SlB'])
		ax.text(pos.x, pos.y+0.5, 'SLEEVE LINE', fontsize=fs, ha='center')

		self.segment(bpd['BF'], bpd['BB'], ax, ldic)
		pos = self.middle(bpd['BF'], bpd['BB'])
		ax.text(pos.x, pos.y+0.5, 'BUST LINE', fontsize=fs, ha='center')

		return ax

	def Donnanno_bodice_without_dart_w(self, bust_ease=8):
		""" Calculation of bodice with no dart
			for Women using Donnanno technique
			This Bodice comes with ease applied

		Args:
			ease: ease to be applied.
		"""


		m=self.m

		#################################################
		# Frame
		#################################################
		A = Point([0, m["longueur_devant"]])
		B = Point([0, 0])
		C = Point([(m["tour_poitrine"]+bust_ease)/2, 0])
		D = Point([(m["tour_poitrine"]+bust_ease)/2, m["longueur_dos"]])
		E = Point([(m["tour_poitrine"]+bust_ease)/4, 0])
		F = Point([(m["tour_poitrine"]+bust_ease)/4, m["longueur_devant"]])


		#################################################
		# Bust line
		#################################################
		H = Point([(m["tour_poitrine"]+bust_ease)/2, m["longueur_dos"]/2])
		I = Point([0, m["longueur_dos"]/2])
		Q = Point([E.x, H.y])


		G = Point([3*(m["tour_poitrine"]+bust_ease)/10, m["longueur_dos"]])
		H1 = Point([3*(m["tour_poitrine"]+bust_ease)/10, m["longueur_dos"]/2])

		I1 = Point([2*(m["tour_poitrine"]+bust_ease)/10-1.5, m["longueur_dos"]/2])
		J1 = Point([I1.x, A.y])


		#################################################
		# Torso or shoulder line
		#################################################
		L = Point([H.x, H.y+(D.y-H.y)/3])
		M = Point([0, L.y])


		L1 = Point([H1.x, L.y])
		J = Point([I1.x, L.y])


		O = Point([G.x, G.y-1.5])


		shoulder_width = (D.x-G.x-1)
		N  =  Point([D.x-(shoulder_width/2 - 2), D.y])
		P  =  Point([N.x, N.y+2.5])

		controle_1  =  Point([D.x-1, D.y])
		controle_2  =  Point([N.x+1, N.y+1])
		points_col_dos = [D, controle_1, controle_2, P]
		dbcol, col_dos = self.pistolet(points_col_dos, 3, tot = True)

		#################################################
		# Shoulder
		#################################################
		# Back
		if m["longueur_epaule"] == 0:
			P1 = O
		else:
			a = self.segment_angle(P, O)
			dPO = self.distance(P, O)
			print("[PO]", dPO)
			dOP1 = m["longueur_epaule"]-dPO
			P1 = Point([O.x+dOP1*np.cos(a+np.pi), O.y+dOP1*np.sin(a+np.pi)])
		print("[PP1]", self.distance(P, P1))

		# Front
		U = Point([shoulder_width/2-2, A.y])
		U1 = Point([0, A.y-U.x])
		U2 = Point([A.x+U.x*np.cos(-np.pi/4), A.y+U.x*np.sin(-np.pi/4)]) ### CHECK !
		dfcol, col_devant = self.pistolet([U1, U2, U], 2, tot=True)

		Z = Point([J1.x, J1.y-5])
		a = self.segment_angle(U, Z)
		if m["longueur_epaule"] == 0:
			Z2 = Z
		else:
			Z2  =  Point([U.x+m["longueur_epaule"]*np.cos(a), U.y+m["longueur_epaule"]*np.sin(a)] )
		print("[UZ2]", self.distance(U, Z2))

		#################################################
		# Armhole or Armscye
		#################################################
		# Back
		bd = 1.5
		controle = Point([H1.x - bd, H1.y + bd])

		m["longueur_emmanchure_dos"], emmanchure_dos = self.pistolet([P1, L1, controle, Q], 2, tot=True)
		print("Longueur emmanchure dos: %4.0f" % (m["longueur_emmanchure_dos"]))

		#front
		fd = 1.8
		controle = Point([I1.x + fd, I1.y + fd])



		m["longueur_emmanchure_devant"], emmanchure_devant = self.pistolet([Z2, J, controle, Q], 2, tot=True)
		print("Longueur emmanchure devant: %4.0f" % (m["longueur_emmanchure_devant"]))

		#################################################
		# Dictionnaries and vertices
		#################################################
		self.Bodice_points_dic={}
		Bodice_Points_Names=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'L', 'M', 'N', 'O', 'P', 'P1', 'Q', 'U', 'Z', 'H1', 'I1', 'J1', 'L1', 'U1', 'U2', 'Z2']
		Bodice_Points_List=[A, B, C, D, E, F, G, H, I, J, L, M, N, O, P, P1, Q, U, Z, H1, I1, J1, L1, U1, U2, Z2]

		for i in range(len(Bodice_Points_Names)):
			self.Bodice_points_dic[Bodice_Points_Names[i]] = Bodice_Points_List[i]

		self.Bodice_Front_vertices = [B.pos(), U1.pos()] + col_devant + [Z.pos()] + emmanchure_devant + [Q.pos(), E.pos()]
		self.Bodice_Back_vertices = [C.pos(), D.pos()] + col_dos + [O.pos()] + emmanchure_dos + [Q.pos(), E.pos()]

	def Donnanno_bodice_without_dart_m(self, bust_ease=8):
		""" Calculation of bodice with no dart
			for Men using Donnanno technique
			This Bodice comes with ease applied

		Args:
			ease: ease to be applied.
		"""
		m=self.m


		#################################################
		# Frame
		#################################################
		A = Point([0, m["longueur_devant"]])
		B = Point([0, 0])
		C = Point([(m["tour_poitrine"]+bust_ease)/2, 0])
		D = Point([(m["tour_poitrine"]+bust_ease)/2, m["longueur_dos"]])
		E = Point([(m["tour_poitrine"]+bust_ease)/4, 0])
		F = Point([(m["tour_poitrine"]+bust_ease)/4, m["longueur_devant"]])


		#################################################
		# Bust line
		#################################################
		H = Point([(m["tour_poitrine"]+bust_ease)/2, m["longueur_dos"]/2])
		I = Point([0, m["longueur_dos"]/2])
		Q = Point([E.x, H.y])


		G = D - [m["largeur_epaule"]/2 +1, 0] # ca merde dans les "grandes" largeurs... j'utilise donc la méthode pour les femmes
		#~ G = D - [(m["tour_poitrine"]+bust_ease)/5 +1, 0]
		H1 = H - [m["largeur_epaule"]/2 +1, 0]
		#~ H1 = H - [(m["tour_poitrine"]+bust_ease)/5 +1, 0]

		I1 = H1 - [(m["tour_poitrine"]+bust_ease)/10 + 2, 0]
		J1 = Point([I1.x, A.y])

		#################################################
		# Torso or shoulder line
		#################################################
		L = H + [0, (D.y-H.y)/3]
		M = Point([0, L.y])


		L1 = Point([H1.x, L.y])
		J = Point([I1.x, L.y])


		O = G -[0, 2.5]

		shoulder_width = (D.x-G.x)
		N  =  D - [(shoulder_width/3 + 0.6), 0]
		P  =  N + [0, 2.5]

		controle_1  =  Point([D.x-1, D.y])
		controle_2  =  Point([N.x+1, N.y+1])
		points_col_dos = [D, controle_1, controle_2, P]
		dbcol, col_dos = self.pistolet(points_col_dos, 3, tot = True)

		#################################################
		# Shoulder
		#################################################
		# Back
		if m["longueur_epaule"]==0:
			P1 = O
			le=self.distance(P, P1)

		else:
			a = self.segment_angle(P, O)
			dPO = self.distance(P, O)
			print("[PO]", dPO)
			dOP1 = m["longueur_epaule"]-dPO + 1
			P1 = O + [dOP1*np.cos(a+np.pi), dOP1*np.sin(a+np.pi)]
			print("[PP1]", self.distance(P, P1))

		# Front
		U = A + [shoulder_width/3 + 0.6, 0]
		U1 = A - [0, U.x]
		U2 = A + [U.x*np.cos(-np.pi/4), U.x*np.sin(-np.pi/4)]
		dfcol, col_devant = self.pistolet([U1, U2, U], 2, tot=True)

		Z = J1  - [0, 5]
		a = self.segment_angle(U, Z)
		if m["longueur_epaule"]==0:
			Z2  = U + [le*np.cos(a), le*np.sin(a)]
		else:
			Z2  = U + [(m["longueur_epaule"]+1)*np.cos(a), (m["longueur_epaule"]+1)*np.sin(a)]
			print("[UZ2]", self.distance(U, Z2))

		#################################################
		# Armhole or Armscye
		#################################################
		# Back
		# I add control points as in gilewska to ensure that the curve is flat around the sleeve line
		bd = 1.5
		controle = H1 + [ -bd,  bd ]

		m["longueur_emmanchure_dos"], emmanchure_dos = self.pistolet([P1, L1, controle, Q], 2, tot=True)
		#~ m["longueur_emmanchure_dos"], emmanchure_dos = self.pistolet([P1, L1, Q], 2, tot=True)
		print("Longueur emmanchure dos: %4.0f" % (m["longueur_emmanchure_dos"]))

		#front
		fd = 1.8
		controle = I1 + [fd,fd]



		m["longueur_emmanchure_devant"], emmanchure_devant = self.pistolet([Z2, J, controle, Q], 2, tot=True)
		#~ m["longueur_emmanchure_devant"], emmanchure_devant = self.pistolet([Z2, J, Q], 2, tot=True)
		print("Longueur emmanchure devant: %4.0f" % (m["longueur_emmanchure_devant"]))

		#################################################
		# Basic Shirt Base and Dart
		#################################################

		Y = B - [0, m["hauteur_bassin"]]
		X = C - [0, m["hauteur_bassin"]]
		E1 = self.middle(X, Y)

		dXC1 = 75 - self.distance(D, X)
		C1 = X - [0, dXC1]
		B1 = Point([Y.x, C1.y+2])
		E3 = Point([E1.x, B1.y])
		E2 = Point([E1.x, C1.y])

		# side dart
		W = E +[1.5, 0]
		W1 = E - [1.5, 0]

		lE1 = E1 - [1, 0]
		rB10 = B1 + [0.2*self.distance(B1, E3), 0]
		rB11 = B1 + [0.25*self.distance(B1, E3), 0]
		rB12 = B1 + [0.3*self.distance(B1, E3), 0]
		l_base_front, base_front = self.pistolet(np.array([E1, lE1, rB12, rB11, rB10]), 3, tot=True)

		rE1 = E1 + [1, 0]
		rC10 = C1 - [0.2*self.distance(C1, E2), 0]
		rC11 = C1 - [0.25*self.distance(C1, E2), 0]
		rC12 = C1 - [0.3*self.distance(C1, E2), 0]
		l_base_back, base_back = self.pistolet([E1, rE1, rC12, rC11, rC10], 3, tot=True)

		#################################################
		# Dictionnaries and vertices
		#################################################
		self.Bodice_points_dic={}
		Bodice_Points_Names=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'L', 'M', 'N', 'O', 'P', 'P1', 'Q', 'U', 'Z', 'H1', 'I1', 'J1', 'L1', 'U1', 'U2', 'Z2', 'Y', 'E1', 'X', 'B1', 'E3', 'E2', 'C1']
		Bodice_Points_List=[A, B, C, D, E, F, G, H, I, J, L, M, N, O, P, P1, Q, U, Z, H1, I1, J1, L1, U1, U2, Z2, Y, E1, X, B1, E3, E2, C1]

		for i in range(len(Bodice_Points_Names)):
			self.Bodice_points_dic[Bodice_Points_Names[i]] = Bodice_Points_List[i]

		self.Bodice_Front_vertices = [B.pos(), U1.pos()] + col_devant + [Z.pos()] + emmanchure_devant + [Q.pos(), W1.pos(), E1.pos()] + base_front + [B1.pos()]
		self.Bodice_Back_vertices = [C.pos(), D.pos()] + col_dos + [O.pos()] + emmanchure_dos + [Q.pos(), W.pos(), E1.pos()] + base_back + [C1.pos()]


	def chiappetta_basic_bodice(self, age=14, d_FB = 5):
		""" Calculation of bodice with no dart
			for children using Chiapetta technique


		Args:
			age: age of the child, the pattern drafting depends on the age
			d_FB: distance between front and back patterns on the draft

		"""

		if age >=2 and age <= 16:
			# front on the left back on the right
			# Back Bodice
			WB = Point([self.m['tour_poitrine']/2 + d_FB, 0])
			WB1 = WB - [self.m['tour_poitrine']/4, 0]

			HB = WB + [0, self.m['longueur_dos']]

			SlB = HB - [0, self.m['longueur_dos']/2 + 1]
			SlB1 = SlB - [self.m['tour_poitrine']/4, 0]

			BB = HB - [0, 2*(self.m['longueur_dos']/2 + 1)/3]
			BB1 = BB - [self.m['carrure_dos']/2, 0]

			CB1 = HB - [self.m['tour_encolure']/6 + 1, 0]
			CB2 = CB1 + [0, self.m['tour_encolure']/17]
			if age < 10:
				l = 1.2
			else:
				l = (1.2 + 0.05*(age-10))
			ClCB = CB1 + [l*np.cos(np.pi/4), l*np.sin(np.pi/4)]
			ClCB2 = HB - [2, 0]

			if age <10:
				sa = 25 # shoulder angle
			else:
				sa = 22
			ShB1 = CB2 + [self.m['longueur_epaule']*np.cos(np.pi*(1 + sa/180)), \
			self.m['longueur_epaule']*np.sin(np.pi*(1 + sa/180))]

			#collar
			collar_back_points = [HB, ClCB2, ClCB, CB2]
			self.m['longueur_col_dos'], back_collar_curve = self.pistolet(collar_back_points, 2, tot = True)
			#armhole
			self.m["longueur_emmanchure_dos"], back_sleeve_curve =  self.pistolet([ShB1, BB1, SlB1], 2, tot=True)

			# Front bodice
			WF = Point([0, 0])
			WF1 = WF + [self.m["tour_poitrine"]/4, 0]

			HF = WF + [0, CB2.y]

			SlF = WF + [0, SlB.y]
			SlF1 = SlF + WF1

			BF = WF + [0, BB.y]
			# Chiappetta only use one carrure, the back one, and applied on the front too
			if age < 10:
				BF1 = BF + [self.m["carrure_dos"]/2, 0]
			else:
				BF1 = BF + [self.m["carrure_dos"]/2 - 1, 0]


			CF1 = HF - [0, self.m["tour_encolure"]/6+1.5]
			CF2 = HF + [self.m["tour_encolure"]/6 + 1, 0]
			if age < 10:
				lcf = 2.2
			else:
				lcf = 3
			ClCF = [CF2.x+lcf*np.cos(3*np.pi/4), CF1.y+lcf*np.sin(3*np.pi/4)]

			collar_front_points = np.array([CF1, ClCF, CF2])
			self.m['longueur_col_devant'], front_collar_curve = self.pistolet(collar_front_points, 2, tot=True)

			ShF1 = CF2 + [self.m['longueur_epaule']*np.cos(-25*np.pi/180), \
			self.m['longueur_epaule']*np.sin(-25*np.pi/180)]

			sleeve_front_points = np.array([ShF1, BF1, SlF1])
			self.m["longueur_emmanchure_devant"], front_sleeve_curve = self.pistolet(sleeve_front_points, 2, tot=True)

			bodice_points_keys=['WF', 'WF1', 'SlF', 'SlF1', 'BF', 'BF1', 'CF1', 'CF2', 'HF', 'ShF1', 'ClCF', \
			'WB', 'WB1', 'SlB', 'SlB1', 'BB', 'BB1', 'HB', 'CB2', 'ShB1', 'ClCB']
			bodice_points_val=[WF, WF1, SlF, SlF1, BF, BF1, CF1, CF2, HF, ShF1, ClCF, \
			WB, WB1, SlB, SlB1, BB, BB1, HB, CB2, ShB1, ClCB]

			for key, val in zip(bodice_points_keys, bodice_points_val):
				self.Bodice_points_dic[key] = val

			self.Bodice_Back_vertices = [WB.pos(), HB.pos()] + back_collar_curve + [ShB1.pos()] + back_sleeve_curve + [SlB1.pos(), WB1.pos()]
			self.Bodice_Front_vertices = [WF.pos(), CF1.pos()] + front_collar_curve + [ShF1.pos()] +  front_sleeve_curve + [SlF1.pos(), WF1.pos()]


	def Gilewska_basic_bodice_m(self, BF_space=10):
		""" Calculation of bodice with no dart
			for Men using Gilewska technique

		Args:
			BF_space: distance between front and back patterns on the draft
		"""

		#################################################
		# Back Frame
		#################################################
		#2
		WB = Point([0, 0]) #A
		WB1 = Point([self.m["tour_poitrine"]/4, 0]) #A1
		#3
		HB = Point([0, self.m["longueur_dos"]]) #B
		HB1 = Point([self.m["largeur_epaule"]/2, HB.y]) #B1
		#4
		SlB = Point([0, HB.y/2 + 1]) # ligne d'emmanchure C
		SlB1 = Point([WB1.x, SlB.y]) # C1
		#5
		BB = Point([0, SlB.y + (HB.y - SlB.y)/3 +1]) # ligne de carrure D
		BB1 = Point([self.m["carrure_dos"]/2, BB.y]) # D1
		#6
		B2 =  Point([self.m["tour_encolure"]/6+1, HB.y]) # keep it B2

		#################################################
		# Front Frame
		#################################################
		#7
		x_dev = WB1.x+BF_space
		#8
		WF = Point([x_dev+self.m["tour_poitrine"]/4, 0]) #E
		WF1 = Point([x_dev, 0]) #E1
		#10
		HF = Point([WF.x, self.m["longueur_devant"]]) #F
		HF1 = HF + [-self.m["largeur_epaule"]/2, 0] #F1
		#11
		SlF = Point([WF.x, SlB.y]) #G
		SlF1 = Point([x_dev, SlF.y]) #G1
		#12
		BF = Point([WF.x, BB.y]) #H
		BF1 = BF + [-self.m["carrure_devant"]/2, 0] #H1
		#13
		CF1 = HF + [-self.m["tour_encolure"]/6 -1, 0] #F2

		#################################################
		# Add Hip
		#################################################
		HiB = Point([0, -self.m['hauteur_bassin']])
		HiB1 = HiB + [self.m["tour_bassin"]/4, 0]
		HiF = WF + HiB
		HiF1 = HiF - [self.m["tour_bassin"]/4, 0]

		#################################################
		# Back Collar
		#################################################
		#14
		CB1 = B2 + [0, self.m["tour_encolure"]/16]
		CB2 = HB + [1, 0]
		self.m['longueur_col_dos'], collar_back_points = self.pistolet(np.array([HB, CB2, CB1]), 2, tot=True)

		#################################################
		# Back Shoulder
		#################################################
		#15
		ShB1 = HB1 + [0, -3]

		#
		# This is added so that the shoulder length IF MEASURED is respected because
		# Gilewska's way of proceeding leeds to lengths that are 1 to 2 cm larger
		#
		#
		dShB = self.distance(CB1,  ShB1)
		if self.m["longueur_epaule"]>0:
			a = self.segment_angle(CB1, ShB1) # shoulder line angle
			delta = self.m["longueur_epaule"] - dShB # calculate length differnce
			print("delta", delta)
			ShB1 = ShB1 + [delta*np.cos(a), delta*np.sin(a)] #add length difference

			dShB = self.distance(CB1,  ShB1)	# recalculate and check
		print("longueur épaule dos\n\t mesurée:%4.0f\n\t calculée: %4.0f" % (self.m["longueur_epaule"], dShB))


		###### ###########################################
		# Back Sleeve
		#################################################
		#18
		b_length=2.5 # max 3cm
		CPSlB = Point([BB1.x + np.cos(np.pi/4)*b_length, SlB1.y + np.sin(np.pi/4)*b_length])
		#~ CPSlB1 = SlB1 - [0.5, 0]
		# This test is necessary because in some cases the carrue dos is close to the
		# bust width so the control point abcissa is larger then the sleeve point

		if CPSlB.x < SlB1.x:
			self.m["longueur_emmanchure_dos"], sleeve_back_points =  self.pistolet([ShB1, BB1, CPSlB, SlB1], 2, tot=True)
		else:
			self.m["longueur_emmanchure_dos"], sleeve_back_points =  self.pistolet([ShB1, BB1, SlB1], 2, tot=True)
		print("Longueur emmanchure dos: %4.0f" % (self.m["longueur_emmanchure_dos"]))

		#################################################
		# Front Collar
		#################################################
		#17
		CF = HF + [0, -self.m["tour_encolure"]/6 -1]
		CPCF = CF + [-1, 0] # slightly different from Gilewska
		self.m['longueur_col_devant'], collar_front_points = self.pistolet([CF, CPCF, CF1], 2, tot=True)


		#################################################
		# Front Shoulder
		#################################################
		#16
		#~ ShF1 = [HF1.x, HF1.y-7] #valeur Gilewska je la trouve très élevée et les longueurs d'épaules ne coincident pas
		ShF1 = HF1 + [0, -5] # valeur Donnanno  et là les  longueurs d'épaules coincident...

		dShF = self.distance(CF1,  ShF1)
		if self.m["longueur_epaule"]>0:
			a = self.segment_angle(CF1, ShF1) # shoulder line angle
			delta = self.m["longueur_epaule"] - dShF # calculate length differnce
			print("delta", delta)
			ShF1 = ShF1 + [ delta*np.cos(a+np.pi), delta*np.sin(a+np.pi)] #add length difference

			dShF=self.distance(CF1, ShF1) 	# recalculate and check
		print("longueur épaule devant\n\t mesurée:%4.0f\n\t calculée: %4.0f" % (self.m["longueur_epaule"], dShF))


		#################################################
		# Front Sleeve
		#################################################
		#19
		f_length = 2 #min 2 max 2.2
		CPSlF = Point([ BF1.x-np.cos(np.pi/4)*f_length, SlF1.y+np.sin(np.pi/4)*f_length])
		CPSlF1 = SlF1 + [0.5, 0] #point added to ensure correct tangents.
		#~ CPSlF2 = BF1 + [0, -1] #point added to ensure correct tangents.
		#~ CPSlF3 = self.middle(BF1, ShF1) #point added to ensure correct tangents.

		self.m["longueur_emmanchure_devant"], sleeve_front_points  =   self.pistolet( [ShF1, BF1,  CPSlF, CPSlF1, SlF1], 2, tot=True)
		#~ self.m["longueur_emmanchure_devant"], sleeve_front_points  =   self.pistolet([ShF1, BF1, SlF1], 2, tot=True)
		print("Longueur emmanchure devant: %4.0f" % (self.m["longueur_emmanchure_devant"]))


		#################################################
		# Sleeve depth
		#################################################
		xYP = (WB1.x+x_dev)/2
		YP_emmanchure  =  self.segment_angle(ShB1, ShF1)*(xYP - ShB1.x) + ShB1.y
		DS = [xYP, YP_emmanchure]
		self.m["profondeur_emmanchure"]  =  YP_emmanchure - SlB1.y
		print("Profondeur d'emmanchure: %4.0f" % (self.m["profondeur_emmanchure"]))

		########################################
		#Create points dictionnary
		########################################

		if self.hip:
			Back_Points_list  =  [HiB, HiB1, WB,  SlB,  BB,  HB, HB1, CB1,  ShB1,  BB1,  CPSlB,  SlB1,  WB1, DS, B2]
			Back_Points_Names  =  ['HiB', 'HiB1', 'WB', 'SlB', 'BB', 'HB', 'HB1', 'CB1', 'ShB1', 'BB1', 'CPSlB', 'SlB1', 'WB1', 'DS', 'B2']

			Front_Points_list  =  [HiF, HiF1, WF,  SlF,  BF, CF,  CPCF,  CF1,  ShF1,  BF1,  CPSlF,  SlF1,  WF1, HF, HF1]
			Front_Points_Names  =  ['HiF', 'HiF1', 'WF', 'SlF', 'BF', 'CF', 'CPCF', 'CF1', 'ShF1', 'BF1', 'CPSlF', 'SlF1', 'WF1', 'HF', 'HF1']

		else:
			Back_Points_list  =  [WB,  SlB,  BB,  HB, HB1, CB1,  ShB1,  BB1,  CPSlB,  SlB1,  WB1, DS, B2]
			Back_Points_Names  =  ['WB', 'SlB', 'BB', 'HB', 'HB1', 'CB1', 'ShB1', 'BB1', 'CPSlB', 'SlB1', 'WB1', 'DS', 'B2']

			Front_Points_list  =  [WF,  SlF,  BF, CF,  CPCF,  CF1,  ShF1,  BF1,  CPSlF,  SlF1,  WF1, HF, HF1]
			Front_Points_Names  =  ['WF', 'SlF', 'BF', 'CF', 'CPCF', 'CF1', 'ShF1', 'BF1', 'CPSlF', 'SlF1', 'WF1', 'HF', 'HF1']

		for i in range(len(Back_Points_Names)):
			self.Bodice_points_dic[Back_Points_Names[i]] = Back_Points_list[i]

		for i in range(len(Front_Points_Names)):
			self.Bodice_points_dic[Front_Points_Names[i]] = Front_Points_list[i]


		#########################################
		#Create Vertices
		#for polygon representation
		#########################################

		if self.hip:

			self.Bodice_Back_vertices  =  [HiB.pos(),  WB.pos(),  HB.pos() ] + collar_back_points +  sleeve_back_points + [SlB1.pos(), HiB1.pos()]
			self.Bodice_Front_vertices  =  [HiF.pos(),  SlF.pos(),  BF.pos() ] + collar_front_points +  sleeve_front_points + [SlF1.pos(),  HiF1.pos()]

		else:
			self.Bodice_Back_vertices  =  [WB.pos(),  HB.pos() ] + collar_back_points +  sleeve_back_points + [SlB1.pos(), WB1.pos()]
			self.Bodice_Front_vertices  =  [WF.pos(),  SlF.pos(),  BF.pos() ] + collar_front_points +  sleeve_front_points + [SlF1.pos(),  WF1.pos()]

		self.curves_dic = {'Back_Collar': collar_back_points, 'Back_Sleeve': sleeve_back_points, 'Front_Collar': collar_front_points, 'Front_Sleeve': sleeve_front_points}



	def Gilewska_basic_sleeve_m(self):
		""" Calculation of basic sleeve
			for Men using Gilewska technique
		"""

		#########################################
		#squeleton
		#########################################
		O = Point([0,  0])
		A = Point([0,  self.m["longueur_manche"]])
		B = A + [0, - self.m["profondeur_emmanchure"]*4/5]

		C = Point([-(self.m["longueur_emmanchure_dos"]*3/4 + 1),  B.y])
		D = Point([self.m["longueur_emmanchure_devant"]*3/4 + 1,  B.y])


		C1 = C + [1, 0]
		D1 = D + [-1, 0]

		E = A + [-1.5, 0] # There's an uncertainty in the  book because on fig 3 p 81 it's 1cm but in the text it's 1.5
		F = A + [0.5, 0]

		#########################################
		# Curve for the back
		#########################################

		K = self.middle(C1, E)
		Kb = self.middle(C1, K)
		Kh = self.middle(K, E)

		a = self.segment_angle(C1, E)
		Kb1 = Kb + [0.5*np.cos(a-np.pi/2),  0.5*np.sin(a-np.pi/2)]
		Kh1 = Kh + [1.5*np.cos(a+np.pi/2), 1.5*np.sin(a+np.pi/2)]

		points = [C1, Kb1, K, Kh1, E, A]
		dbc, back_curve_points =  self.pistolet(points, 4, tot=True)

		#########################################
		#curve for the front
		#########################################

		G = self.middle(D1, F)
		Gb = self.middle(D1, G)
		Gh = self.middle(G, F)

		a = self.segment_angle(D1, F)
		print(a)
		Gb1 = Point([Gb.x+0.8*np.cos(a-np.pi/2), Gb.y+0.8*np.sin(a-np.pi/2)])
		Gh1 = Point([Gh.x+1.8*np.cos(a+np.pi/2), Gh.y+1.8*np.sin(a+np.pi/2)])
		#~ points = np.array([D1, Gb1, G, Gh1, F, A])
		points = [A, F, Gh1, G, Gb1, D1]
		dfc, front_curve_points = self.pistolet(points, 4, tot=True)


		#########################################
		# wrist
		#########################################

		S = Point([self.m["tour_poignet"]/2, 0])
		V = Point([-self.m["tour_poignet"]/2, 0])

		self.Sleeve_points_dic = {'A':A, 'B':B, 'C':C, 'D':D, 'E':E, 'F':F, 'C1':C1, 'D1':D1, 'K':K, 'Kb1':Kb1, 'Kh1': Kh1, 'G':G, 'Gb':Gb, 'Gh':Gh, 'Gb1':Gb1, 'Gh1':Gh1, 'V':V, 'S':S}
		self.Sleeve_vertices = [V.pos(), C.pos()] + back_curve_points + [A.pos()] + front_curve_points + [D.pos(), S.pos()]


	def Gilewska_basic_bodice_w(self, sep=10):
		"""Basic Bodice for woment
		using Gilewska technique

		Trying to get standard
		first letter Caps [then minor]
		W: waist
		Sl: sleeve
		B: bust
		H: height
		C: collar
		Sh: shoulder
		DSl: depth of sleeve

		Last Letter
		B: Back
		F: Front

		no numbering when on the fold line
		numbering when on the sleeve side

		CP: Control Point

		Args:
			sep: distance between front and back patterns on draft
		"""

		########################################
		#Back and Front Frames
		########################################

		WB = Point([0, 0])
		WB1 = Point([self.m["tour_poitrine"]/4 - 1, 0])
		HB = Point([0, self.m["longueur_dos"]])
		HB1 = Point([WB.x, HB.y])

		xdev = WB1.x + sep

		WF = Point([xdev + self.m["tour_poitrine"]/4 + 1, 0])
		WF1 = Point([xdev, 0])
		HF = Point([WF.x, self.m["longueur_devant"]])
		HF1 = Point([WF1.x, HF.y])

		########################################
		#Collars
		########################################

		self.m["profondeur_encolure_dos"]  =  self.m["tour_encolure"]/16
		self.m["largeur_encolure"]  =  self.m["tour_encolure"]/6
		self.m["profondeur_encolure_devant"]  =  self.m["tour_encolure"]/6 + 2


		CPCB = Point([self.m["largeur_encolure"]-1.5*np.cos(np.pi/4), self.m["longueur_dos"]-self.m["profondeur_encolure_dos"]+1.5*np.sin(np.pi/4)])
		CPCF  =  HF + [-self.m["largeur_encolure"]+2.5*np.cos(np.pi/4), -self.m["profondeur_encolure_devant"]+2.5*np.sin(np.pi/4)]

		CB = Point([0,  self.m["longueur_dos"] - self.m["profondeur_encolure_dos"]])
		CB1 = Point([self.m["largeur_encolure"],  self.m["longueur_dos"]])

		CF = HF + [0,  -self.m["profondeur_encolure_devant"] ]
		CF1 = HF + [-self.m["largeur_encolure"],  0]

		# fit for collar points
		pos_encolure_dos = [CB, CPCB, CB1]
		dcb, collar_back_points = self.pistolet(pos_encolure_dos, 2, tot=True)
		self.m['longueur_col_dos'] = round(dcb,1)

		pos_encolure_devant = [CF, CPCF, CF1]
		dcf, collar_front_points = self.pistolet(pos_encolure_devant, 2, tot=True)
		self.m['longueur_col_devant'] = round(dcf,1)

		########################################
		#Sleeve and Bust lines
		########################################

		self.m["hauteur_emmanchure"]  =  self.m["longueur_dos"]/2 + 1
		self.m["hauteur_carrure"]  =  (self.m["longueur_dos"] - self.m["hauteur_emmanchure"] - self.m["profondeur_encolure_dos"])/3 +1

		SlB = Point([0, self.m["hauteur_emmanchure"]])
		SlF = Point([WF.x, SlB.y])
		BB = Point([0, self.m["hauteur_emmanchure"]+self.m["hauteur_carrure"]])
		BF = Point([WF.x, BB.y])

		########################################
		#Shoulders
		########################################

		x_epaule_dos  =  self.m["longueur_epaule"] * np.cos(14*np.pi/180)
		y_epaule_dos  =  self.m["longueur_epaule"] * np.sin(14*np.pi/180)
		x_epaule_devant  =  self.m["longueur_epaule"] * np.cos(26*np.pi/180)
		y_epaule_devant  =  self.m["longueur_epaule"] * np.sin(26*np.pi/180)


		ShB1 = Point([self.m["largeur_encolure"] + x_epaule_dos,  self.m["longueur_dos"] - y_epaule_dos])
		ShF1 = Point([HF.x - self.m["largeur_encolure"] - x_epaule_devant,  self.m["longueur_devant"] - y_epaule_devant])

		########################################
		#Sleeve points
		########################################

		BB1  =  Point([self.m["carrure_dos"]/2,  BB.y])
		SlB1 =  Point([WB1.x,  SlB.y])

		b_length = 2 # max 3 I think
		CPSlB  =  Point([self.m["carrure_dos"]/2 + b_length*np.cos(np.pi/4),  self.m["hauteur_emmanchure"] + b_length*np.sin(np.pi/4)])
		CPSlB1 = self.middle(ShB1, BB1)

		BF1  =  BF + [ - self.m["carrure_devant"]/2,  0]
		SlF1  =  Point([xdev,  SlF.y])

		f_length = 2.3
		CPSlF  =  Point([SlF.x - self.m["carrure_devant"]/2 - f_length*np.cos(np.pi/4),  self.m["hauteur_emmanchure"] + f_length*np.sin(np.pi/4)])

		YP_emmanchure  =  self.segment_angle(ShB1, ShF1)*(xdev - ShB1.x) + ShB1.y
		self.m["profondeur_emmanchure"]  =  YP_emmanchure-self.m["hauteur_emmanchure"]
		print("Profondeur d'emmanchure: %4.0f" % (self.m["profondeur_emmanchure"]))
		DSl1 = Point([xdev, YP_emmanchure])

		#~ points_emmanchure_dos = np.array([ShB1, BB1, CPSlB, SlB1])
		#~ dsb, sleeve_back_points = self.pistolet(points_emmanchure_dos, 3, tot=True)
		points_emmanchure_dos = [ShB1, BB1, CPSlB, SlB1]
		dsb, sleeve_back_points = self.pistolet(points_emmanchure_dos, 2, tot=True)
		print("Longueur emmanchure dos: %4.0f" % (dsb))
		self.m["longueur_emmanchure_dos"] = dsb

		points_emmanchure_devant = [ShF1, BF1, CPSlF, SlF1]
		dsf, sleeve_front_points = self.pistolet(points_emmanchure_devant, 2, tot=True)
		print("Longueur emmanchure devant: %4.0f" % (dsf))
		self.m["longueur_emmanchure_devant"] = dsf

		########################################
		#Create points dictionnary
		########################################

		Back_Points_list  =  [WB,  SlB,  BB, CB,  CPCB,  CB1,  ShB1,  BB1,  CPSlB,  SlB1,  WB1]
		Back_Points_Names  =  ['WB', 'SlB', 'BB', 'CB', 'CPCB', 'CB1', 'ShB1', 'BB1', 'CPSlB', 'SlB1', 'WB1']

		for i in range(len(Back_Points_Names)):
			self.Bodice_points_dic[Back_Points_Names[i]] = Back_Points_list[i]

		Front_Points_list  =  [WF,  SlF,  BF, CF,  CPCF,  CF1,  ShF1,  BF1,  CPSlF,  SlF1,  WF1]
		Front_Points_Names  =  ['WF', 'SlF', 'BF', 'CF', 'CPCF', 'CF1', 'ShF1', 'BF1', 'CPSlF', 'SlF1', 'WF1']
		for i in range(len(Front_Points_Names)):
			self.Bodice_points_dic[Front_Points_Names[i]] = Front_Points_list[i]


		#########################################
		#	Create Vertices
		#	for polygon representation
		#########################################


		self.Bodice_Back_vertices  =  [WB.pos(), CB.pos() ] + collar_back_points +  sleeve_back_points + [SlB1.pos(), WB1.pos()]
		self.Bodice_Front_vertices  =  [WF.pos(),  CF.pos() ] + collar_front_points +  sleeve_front_points + [SlF1.pos(), WF1.pos()]

		self.curves_dic = {'Back_Collar': collar_back_points, 'Back_Sleeve': sleeve_back_points, 'Front_Collar': collar_front_points, 'Front_Sleeve': sleeve_front_points}



	def add_bust_dart(self):
		""" Add darts to dartless Bodice
		"""
		bfd  = self.Bodice_points_dic

		if self.style == 'Gilewska':
			# Apex of dart
			OP = Point([bfd['WF'].x - self.m["ecart_poitrine"]/2, bfd['CF1'].y - self.m["hauteur_poitrine"]])

			# Cut point on the middle of the shoulder
			MShF = self.middle(bfd["ShF1"], bfd["CF1"])

			# Dart width
			dw = self.m["tour_poitrine"]/20

			# Radius of dart
			r = self.distance(OP, MShF)

			# Angle of rotation
			theta = 2*np.arcsin(dw/(2*r))
			print(dw, r, theta)

			#rotation of points
			A = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
			K = MShF - OP
			K2 = K.mat_out(A) + OP

			S = bfd['ShF1']- OP
			ShF2 = S.mat_out(A) + OP


			# Extension of the bust
			""" Here, in comments and as a reminder,
			I've placed  the strict method of Gilewska...

			a = self.segment_angle(MShF, OP)*180/np.pi
			B = self.intersec_manches(bfd['BF'], bfd['BF1'], MShF, a)
			r2 = self.distance(OP, B)
			dx=2*r2*np.sin(theta/2)
			F2 = bfd['BF1'] - np.array([dx, 0])

			... But I prefer the two lines below because
			logically point F should be rotated as well
			 and not just translated."""

			F1 = bfd['BF1'] - OP
			F2 = F1.mat_out(A) + OP # here the point is rotated around OP with the exact angle of the dart. :=)

			#redraw the arm curve
			dsf, new_sleeve_front_points = self.pistolet([ShF2, F2, bfd['CPSlF'], bfd['SlF1']], 2, tot = True)
			self.curves_dic['Front_Sleeve'] = new_sleeve_front_points # I change the armhole curve to the new one.
			self.m["longueur_emmanchure_devant"] = dsf
			print("longueur emmanchure devant avec pince de buste %4.0f" % (dsf))

			key=['MShF', 'K2', 'ShF2', 'F2', 'OP']
			val=[MShF, K2, ShF2, F2, OP]

			for i in range(len(key)): # add new points to the dictionnary
				self.Bodice_points_dic[key[i]] = val[i]

			#redraw the front bodice with the added dart
			self.Bodice_Front_vertices = [bfd['WF'].pos(),  bfd['CF'].pos() ] + self.curves_dic['Front_Collar'] +  [MShF.pos(), OP.pos(), K2.pos(), ShF2.pos()] + new_sleeve_front_points + [bfd['SlF1'].pos(), bfd['WF1'].pos()]

			#recalculate the sleeve
			self.Gilewska_basic_sleeve_w()

		else:
			pass

	def add_waist_dart(self):
		"""Add waist darts to basic Bodice
		"""

		sbp = self.Bodice_points_dic


		if self.style == 'Gilewska':
			pince_dos = 1
			ecart = self.m["tour_poitrine"]-self.m["tour_taille"]
			pinces = (ecart/2-1)/4

			#start with the back
			# central back dart CBD
			CBD= sbp['WB'] + [1, 0]

			# Back Dart BD
			BDc = sbp['WB'] + [self.m["carrure_dos"]/4, 0]
			BD0 = BDc - [pinces/2, 0]
			BD1 = BDc + [pinces/2, 0]
			BDs = BDc + [0, sbp['SlB'].y]

			#Side Back Dart SBD
			SBD = sbp['WB1'] - [pinces, 0]


			key = ['CBD', 'BD0', 'BD1', 'BDs', 'SBD']
			val = [CBD, BD0, BD1, BDs, SBD]
			for k, v in zip(key, val):
				self.Bodice_points_dic[k]=v

			self.Bodice_Back_vertices  =  [CBD.pos(), sbp['SlB'].pos(), sbp['CB'].pos() ] + self.curves_dic['Back_Collar'] +  self.curves_dic['Back_Sleeve'] + [sbp['SlB1'].pos(), SBD.pos(), BD1.pos(), BDs.pos(), BD0.pos()]
			#~ print(self.Bodice_Back_vertices)

			# The Front
			# Apex of dart
			if 'OP' not in sbp.keys():
				OP = Point([sbp['WF'].x - self.m["ecart_poitrine"]/2, sbp['CF1'].y - self.m["hauteur_poitrine"]])
				bust_dart = False
			else:
				OP = sbp['OP']
				bust_dart = True

			#Front dart FD
			WMF = Point([OP.x, 0])
			FD0 = WMF - [pinces/2, 0]
			FD1 = WMF + [pinces/2, 0]

			#Side Front Dart SFD
			SFD = sbp['WF1'] + [pinces, 0]


			key = ['FD0', 'FD1', 'SFD', 'OP']
			val= [FD0, FD1, SFD, OP]
			for k, v in zip(key, val):
				self.Bodice_points_dic[k]=v

			if bust_dart:
				self.Bodice_Front_vertices = [sbp['WF'].pos(),  sbp['CF'].pos() ] + self.curves_dic['Front_Collar'] +  [sbp['MShF'].pos(), sbp['OP'].pos(), sbp['K2'].pos(), sbp['ShF2'].pos()] + self.curves_dic['Front_Sleeve'] + [sbp['SlF1'].pos(), SFD.pos(), FD0.pos(), OP.pos(), FD1.pos()]
			else:
				self.Bodice_Front_vertices = [sbp['WF'].pos(),  sbp['CF'].pos() ] + self.curves_dic['Front_Collar'] + self.curves_dic['Front_Sleeve'] + [sbp['SlF1'].pos(), SFD.pos(), FD0.pos(), OP.pos(), FD1.pos()]


		else:
			pass

	def Gilewska_basic_sleeve_w(self):
		"""Basic sleeve for Women
		using Gilewska technique
		"""

		#########################################
		# squeleton
		#########################################

		A = Point([0,  self.m["longueur_manche"]])

		C = Point([0,  self.m["longueur_manche"] - 4*self.m["profondeur_emmanchure"]/5])

		E = Point([3*self.m["longueur_emmanchure_devant"]/4,  C.y])
		D = Point([-3*self.m["longueur_emmanchure_dos"]/4,  C.y])


		F  =  Point([0,  0.5*(A.y + C.y)])
		J  =  self.intersec_manches(A, D, F, -45)
		J1  =  self.intersec_manches(A, E, F, 45)


		CDos1  = J + [ 2*np.cos(3*np.pi/4), 2*np.sin(3*np.pi/4)]
		CDevant1  =  J1 + [ 1.8*np.cos(np.pi/4),  1.8*np.sin(np.pi/4)]

		G  =  self.intersec_manches(A, D, C, -45)
		G1  =  self.intersec_manches(A, E, C, 45)

		CDos2  = G + [ 1.5*np.cos(3*np.pi/4),  1.5*np.sin(3*np.pi/4) ]
		CDevant2  = G1 + [ 1*np.cos(np.pi/4),  1*np.sin(np.pi/4) ]

		K = self.middle(D, G)
		KK = self.middle(D, K)
		K1 = self.middle(E, G1)
		KK1 = self.middle(E, K1)

		CDos4 = KK + [ 0.5*np.cos(self.segment_angle(D, K)-np.pi/2),  0.5*np.sin(self.segment_angle(D, K)-np.pi/2) ]
		CDevant4 = KK1 + [ 0.8*np.cos(self.segment_angle(E, K1)-np.pi/2),  0.8*np.sin(self.segment_angle(E, K1)-np.pi/2) ]

		Controle_dos  =  [A, CDos1,  CDos2,  K,  CDos4, D]
		Controle_devant  =  [E, CDevant4, K1,  CDevant2, CDevant1, A]


		#########################################
		# Sleeve head curve for the back
		#########################################

		#~ dcb_1, sleeve_back_points_1 = self.pistolet(np.array([A, CDos1,  CDos2,  K]), 3, tot=True)
		#~ dcb_2, sleeve_back_points_2 = self.pistolet(np.array([K,  CDos4, D]), 2, tot=True)

		dcb, back_curve_points =  self.pistolet(Controle_dos, 4, tot=True)
		#########################################
		# tracé de courbe de tête de manche devant
		#########################################

		dcf, front_curve_points = self.pistolet(Controle_devant, 3, tot=True)


		W = Point([0, self.m["longueur_manche"] - self.m["hauteur_coude"]])

		#########################################
		# bas de manche
		#########################################
		S = Point([self.m["tour_poignet"]/2, 0])
		V = Point([-self.m["tour_poignet"]/2, 0])

		W0 = self.intersec_manches(S, E, W, 0)
		W1 = self.intersec_manches(V, D, W, 0)

		self.Sleeve_points_dic = {'A':A, 'C':C, 'D':D, 'E':E, 'F':F, 'J':J, 'J1':J1, \
		 'K':K, 'K1':K1, 'G':G, 'G1':G1, 'V':V, 'S':S, 'W':W, 'W0':W0, 'W1':W1, \
		 'CDos1':CDos1, 'CDos2':CDos2, 'CDos4':CDos4, 'CDevant1':CDevant1, \
		 'CDevant2':CDevant2, 'CDevant4':CDevant4}
		self.Sleeve_vertices = [S.pos(), W0.pos(), E.pos()] + front_curve_points + [A.pos()] + back_curve_points + [D.pos(), W1.pos(), V.pos()]
