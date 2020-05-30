#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append('./..')

from OpenPattern.Pattern import *
from OpenPattern.Points import *

###############################################################
# Basic Trousers templates
# from different stylists Donnanno, Gilewska
###############################################################

class Basic_Trousers(Pattern):
	"""
	Class used to calculate the pattern of basic trousers
	Inherits from Pattern

	Attributes:
		# dics used here for points and labels:

		Trousers_Back_points_dic
		Trousers_Front_points_dic

		# lists of vertices to draw pattern curves:

		Trousers_Back_vertices
		Trousers_Front_vertices

		# curves obtained from spline interpolation:
		# SORRY IT'S IN FRENCH
		fourche_arriere
		interieur_arriere
		exterieur_arriere
		fourche_avant
		interieur_avant
		exterieur_avant
		ceinture_avant

	"""
	############################################################
	def __init__(self, pname="gregoire", gender='m', style='Donnanno'):
		"""
		Class initialisator. Launches trouser calculation

		"""
		Pattern.__init__(self, pname, gender)

		if self.gender == "m":
			self.ease = 0
		else:
			self.ease = 2

		self.style=style
		self.Trousers_Back_points_dic  =  {}
		self.Trousers_Front_points_dic  =  {}

		if self.style == 'Donnanno':
			print("style Donnanno selected")
			self.Donnanno_front_trousers()
			self.Donnanno_back_trousers()

		else:
			print("style %s unknown, using Donnanno instead" % (self.style))
			self.Donnanno_front_trousers()
			self.Donnanno_back_trousers()

	############################################################
	def Donnanno_front_trousers(self):
		"""
		Calculate front Trousers' pattern
		essentially the same for women and men with some slight differences
		"""

		#Front frame
		A = Point([0, self.m["longueur_tot"]])
		B = Point([self.m["tour_bassin"]/4, self.m["longueur_tot"]])
		C = Point([0, 0])
		D = Point([B.x, 0])

		#crotch and hip lines
		E = Point([0, A.y - self.m["montant"]])
		F = Point([B.x, E.y])
		G = A - [0, self.m["hauteur_bassin"]]
		H = Point([B.x, G.y] )

		if self.gender=="m":
			E1 = E - [self.m["tour_bassin"]/20, 0]
		else:
			E1 = E - [self.m["tour_bassin"]/16 - 1.5, 0]

		#connect and fold lines
		I = E - [0, self.m["montant"]]
		L = Point([B.x, I.y])

		#fold line
		X = Point([0.5 * (E1.x + F.x), E1.y])
		N = Point([X.x, C.y])
		X1 = Point([X.x, I.y])

		#dart position
		#question origin of the numbers ??
		if self.gender=="m":
			M = Point([X.x, A.y - 0.5])
			M2 = M + [6, 0]
			L1 = X1 + [12.5, 0]
			I1 = X1 - [12.5, 0]
			N1 = N + [0, 1.5]
			A1 = A + [1, 0]
		else:
			M = Point([X.x, A.y - 0.9]) #adaptation pour la femme
			M2 = M + [7,+0.2]
			L1 = X1 + [12, 0]
			I1 = X1 - [12, 0]
			N1 = N + [0, 1]
			A1 = A + [0, -1]
			B1 = B + [-1,0]

		C1 = N - [11, 0]
		D1 = N + [11, 0]

		#knee
		O = Point([X.x, M.y - self.m["hauteur_genou"]])


		# points en plus
		E1G = Point([E.x + (E1.x-E.x)/5, E.y + (G.y-E.y)/3]) # permet une jolie courbe de fourche avant

		ONC1 = C1 + [0, 10] # permettent un tombé droit sous le genou.
		OND1 = D1 + [0, 10]

		dfa, self.fourche_avant = self.pistolet(np.array([E1, E1G, G]), 2, tot = True)
		dia, self.interieur_avant = self.pistolet(np.array([C1, ONC1, I1, E1]), 3, tot = True)

		if self.gender=="m":
			dha, self.ceinture_avant = self.pistolet(np.array([A1, M, M2, B]), 2, tot = True)
			dca, self.exterieur_avant = self.pistolet(np.array([B, H, L1, OND1, D1]), 4, tot = True)
			Front_Points_Names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'E1', 'I', 'L', 'X', 'M', 'N', 'O', 'M2', 'X1', 'L1', 'I1', 'N1', 'C1', 'D1', 'A1']
			Front_Points_List = [A, B, C, D, E, F, G, H, E1, I, L, X, M, N, O, M2, X1, L1, I1, N1, C1, D1, A1]
		else:
			dha, self.ceinture_avant = self.pistolet(np.array([A1, M, M2, B1]), 2, tot = True)
			dca, self.exterieur_avant = self.pistolet(np.array([B1,H, L1, OND1, D1]), 4, tot = True)
			Front_Points_Names = ['A','B', 'B1', 'C', 'D', 'E', 'F', 'G', 'H', 'E1', 'I', 'L', 'X', 'M', 'N', 'O', 'M2', 'X1', 'L1', 'I1', 'N1', 'C1', 'D1', 'A1']
			Front_Points_List = [A, B, B1, C, D, E, F, G, H, E1, I, L, X, M, N, O, M2, X1, L1, I1, N1, C1, D1, A1]



		for i in range(len(Front_Points_Names)):
			self.Trousers_Front_points_dic[Front_Points_Names[i]] = Front_Points_List[i]

		self.Trousers_Front_vertices = self.interieur_avant + self.fourche_avant + self.ceinture_avant + self.exterieur_avant + [N1.pos, C1.pos]

		self.front_width=self.distance(E1, F)
		print(self.front_width)

	############################################################

	def Donnanno_back_trousers(self, delta =10  ):
		"""
		Calculate back Trousers' pattern

		Args:
			delta: distance between patterns as int (or float)
		"""

		dx = self.m["tour_bassin"]/4+ delta

		A = Point([dx + self.m["tour_bassin"]/4 + 2, self.m["longueur_tot"]])
		B = Point([dx, A.y])
		C = Point([A.x, 0])
		D = Point([dx, 0])

		G = A - [0, self.m["hauteur_bassin"]] # hip line
		H = Point([B.x, G.y])

		E = A - [0, self.m["montant"]]  #crotch line
		F = Point([B.x, E.y])

		if self.gender == "m":
			E1 = E + [self.distance(E, F)/3 + 1.5, 0]
			E2 = E1 - [0, 2]
			Es = E2 - [2, 0]
		else:
			E1 = E + [self.m["tour_bassin"]/16 +3, 0]
			E2 = E1 + [0,-1]
			E3 = E + [0,-2]
			E4 = E1 + [0,-2]
			Es = self.middle(E3,E4)

		I = E - [0, self.m["montant"]]
		L = Point([F.x, I.y])

		X = self.middle(E1, F)
		M = Point([X.x, A.y])
		N = Point([X.x, C.y])
		X1 = Point([X.x, I.y])

		O = Point([X.x, M.y - self.m["hauteur_genou"]])
		if self.gender == "m":
			A1 = A - [4.5, 0]
			A2 = A1 + [0, 2.5] # from 2 to 3.5

			B1 = B - [0, 0.5]
		else:
			A1 = A - [3.5, 0]
			A2 = A1 + [0, 2] # from 1 to 3.5
			B1 = B + [1, 0]


		a = self.segment_angle(A2, B1)

		if self.gender == "m":
			waist = self.distance(A, B)
			B3 = A2 - (waist*np.cos(a), waist*np.sin(a))
			B4 = A2 - (2*waist*np.cos(a)/3, 2*waist*np.sin(a)/3)
			I1 = X1 + (14, 0) # thigh originally 14 why ?
			L1 = X1 - (14, 0)
			N1 = N - (0, 1.5)
		else:
			waist = self.distance(A2,B1)
			B2 = B1 + [0.5*waist*np.cos(a),0.5*waist*np.sin(a)]
			I1 = X1 + (13, 0) # thigh originally 13 why ?
			L1 = X1 - (13, 0)
			N1 = N - (0, 1)

		C1 = N + (12, 0) # why 12
		D1 = N - (12, 0)

		# points supplémentaires

		CC1 = C1 + [0, 10]
		DD1 = D1 + [0, 10]


		EG = self.middle(E, G)

		dfa, self.fourche_arriere = self.pistolet(np.array([EG, Es, E2]), 2, tot = True)
		dia, self.interieur_arriere = self.pistolet(np.array([E2, I1, CC1, C1]), 3, tot = True)
		if self.gender == "m":
			dea, self.exterieur_arriere = self.pistolet(np.array([D1, DD1, L1, F, B3]), 4, tot = True)
			Back_Points_Names=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'E1', 'E2', 'I', 'L', 'X', 'M', 'N', 'O', 'A1', 'A2', 'B1', 'B3', 'B4', 'I1', 'L1', 'C1', 'D1', 'N1']
			Back_Points_List=[A, B, C, D, E, F, G, H, E1, E2, I, L, X, M, N, O, A1, A2, B1, B3, B4, I1, L1, C1, D1, N1]
			self.Trousers_Back_vertices = self.exterieur_arriere + [B4.pos, A2.pos] + self.fourche_arriere + self.interieur_arriere + [N1.pos, D1.pos]
			self.back_width=self.distance(B3, A)+self.distance(E, E1)
		else:
			dea1, self.exterieur_arriere1 = self.pistolet(np.array([D1, DD1, L1, F + [0.1,-2], F]), 3, tot = True)
			dea2, self.exterieur_arriere2 = self.pistolet(np.array([F, H, B1]), 2, tot = True)
			Back_Points_Names=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'E1', 'E2', 'E3', 'I', 'L', 'X', 'M', 'N', 'O', 'A1', 'A2', 'B1', 'B2', 'I1', 'L1', 'C1', 'D1', 'N1']
			Back_Points_List=[A, B, C, D, E, F, G, H, E1, E2, E3, I, L, X, M, N, O, A1, A2, B1, B2, I1, L1, C1, D1, N1]
			self.Trousers_Back_vertices = self.exterieur_arriere1 + self.exterieur_arriere2 + [B1.pos, A2.pos] + self.fourche_arriere + self.interieur_arriere + [N1.pos, D1.pos]
			self.back_width=self.distance(B1, A)+self.distance(E, E1)


		for i in range(len(Back_Points_Names)):
			self.Trousers_Back_points_dic[Back_Points_Names[i]] = Back_Points_List[i]


		print(self.back_width)

	############################################################

	def Donnanno_add_darts(self,front_dart_list = [['M',1.5,10],['M2',1.5,10]],back_dart_list=[['B2',2,10]]):

		for dart in front_dart_list:
			keyName=dart[0]
			


	############################################################

	def draw_basic_trousers(self, dic = {"Pattern":"Basic Trousers"}, save = False, fname = None, paper='FullSize'):
		"""
		Draw basic trousers' pattern

		Args:
			dic: information to be written on the pattern as dictionnary
			save: if True save pattern to file
			fname: pattern file name as str
			paper: paper type as str

		Returns:
			ax: instance of axis used for drawing
		"""
		fig, ax = self.draw_pattern([self.Trousers_Front_points_dic, self.Trousers_Back_points_dic], \
		[self.Trousers_Front_vertices, self.Trousers_Back_vertices])

		if self.style == 'Donnanno':
			fpd=self.Trousers_Front_points_dic

			ldic={'color':'black', 'linestyle':'dashed'}
			self.segment(fpd["G"], fpd["H"], ax, ldic)
			self.segment(fpd["E1"], fpd["F"], ax, ldic)
			self.segment(fpd["M"], fpd["N"], ax, ldic)
			self.segment(fpd["A"], fpd["C"], ax, ldic)
			self.segment(fpd["B"], fpd["D"], ax, ldic)
			self.segment(fpd["C1"], fpd["D"], ax, ldic)
			self.segment(fpd["I1"], fpd["L"], ax, ldic)

			bpd=self.Trousers_Back_points_dic
			self.segment(bpd["G"], bpd["H"], ax, ldic)
			self.segment(bpd["E1"], bpd["F"], ax, ldic)
			self.segment(bpd["M"], bpd["N"], ax, ldic)
			self.segment(bpd["A"], bpd["C"], ax, ldic)
			self.segment(bpd["A"], bpd["B"], ax, ldic)
			self.segment(bpd["B"], bpd["D"], ax, ldic)
			self.segment(bpd["C1"], bpd["D"], ax, ldic)
			self.segment(bpd["I1"], bpd["L"], ax, ldic)

		ax = self.print_info(ax, dic)

		if save:
			if fname:
				pass
			else:
				fname = 'Basic_Trousers'

			of = '../patterns/'+ self.style + '_' + fname + '_' + self.pname +'_FullSize.pdf'

			plt.savefig(of)

			if paper != 'FullSize':
				self.paper_cut(fig, ax, name = fname, paper = paper)


		return ax

	############################################################


class Pants_block(Basic_Trousers):
		"""
		Adapted from Pants_block for things like jogging or pyjamas.
		Donnanno. I used it to make baggy pyjamas to my teenage son...

		the front and back measurements at the bottom are calculated on the
		basis of the ankle measurement.

		"""
		def __init__(self, pname = "gregoire", gender = 'm', save=False, paper='FullSize'):

			style='Donnanno'
			Basic_Trousers.__init__(self, pname, gender, style)

			self.Donnanno_back_trousers(delta=6)

			pbf=self.Trousers_Front_points_dic
			pbb=self.Trousers_Back_points_dic

			AF = pbf['A'] + [0, 6]
			AB = pbb['A'] + [0, 6]


			V = self.middle(AF, AB)
			Z = V + [0, -V.y]
			B1 = Z - [self.m["tour_cheville"] * 3/4 -2, 0]
			C1 = Z + [self.m["tour_cheville"] * 3/4 +2, 0]

			print('front leg:', self.distance(pbf['E1'], B1) )
			print('back leg:', self.distance(pbb['E2'], C1) )

			pants_points_dic={'B1':B1, 'E1':pbf['E1'], 'AF':AF, 'V':V, 'AB':AB, 'E2':pbb['E2'], 'C1':C1, 'Z':Z}

			pants_bloc_vertices = [B1.pos, pbf['E1'].pos] + self.fourche_avant + [AF.pos, AB.pos] + self.fourche_arriere + [C1.pos, B1.pos]


			fig, ax=self.draw_pattern([pants_points_dic], [pants_bloc_vertices])

			# Dictionnary for plot kwargs
			ldic={'color':'black', 'linestyle':'dashed'}

			self.segment(V, Z, ax, ldic)
			self.segment(pbf['A'], pbb['A'], ax, ldic)

			#Fold line
			Fof = self.middle(AF, pbf['A'])
			Fob = self.middle(AB, pbb['A'])


			ldic={'color':'blue', 'marker':'s', 'linestyle':'dashed'}
			self.segment(Fof, Fob, ax, ldic)
			mfold = self.middle(Fof, Fob)
			ax.text(mfold.x, mfold.y + 0.1, 'Fold Line')

			d=np.abs(pbf['E1'].x-pbb['E1'].x)
			ankle=self.distance(B1, C1)

			ax = self.print_info(ax, {"Pattern":"Pyjama", "Max width":d, "Height": V.y, "Ankle": ankle})


			fname='../patterns/' + self.style + '_Block_pants_' + self.pname + '.pdf'


			if save:
				plt.savefig(fname)

				if paper != 'FullSize':
					self.paper_cut(fig, ax, name='Block_pants', paper=paper)
