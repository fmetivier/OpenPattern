# -*- coding: utf-8 -*- 
# librairies
from matplotlib.pylab import *
import numpy as np
from scipy.interpolate import splprep,  splev
from matplotlib.patches import Polygon
from matplotlib.backends.backend_pdf import PdfPages
import json


"""
TODO:  20/12

Measurements:
- translate measurement names to english n
- measurement input procedure

Drawing:
- Write drawing routines with lines and comments IN PROGRESS
- olivier suggests adding a scale !


Patterns:
- add darts IN PROGRESS
- Bodice D change names (not mandatory though)
- Add donnanno sleeve for m
- Add donnanno everything for w
- Add Gilewska skirt, trousers for w, m
- Add chiapetta... in a some far future
- Add all basic models.
- Cuffs in progress
- Collars in progress

Modeling:
- define the methods for alterations

GUI:
- Everything !!!

I Use Google convention for doc strings
"""


###############################################################
# Class defining tools to draw patterns
###############################################################

class Pattern:
	"""Defines basic methods needed for pattern drafting
	
	
	Attributes:
		m: dictionnary of size measurements
		pname:  name of size measurements
		gender: gender
	
	"""

	############################################################
	
	def __init__(self, pname="sophie", gender='w'):
		"""
		Initializes class instance
		
		Args:
			pname : measurement file if given
			gender: gender of pattern to be drafted
			
		"""
		if pname:
			self.m  =  self.get_measurements(pname)
			self.pname = pname
		else:
			# in the end it should be able to store new measurements.
			pass # create measures

		self.gender=gender
			
	############################################################
	
	def get_measurements(self, pname="sophie"):
		"""Load stored measurements.
		
		Measurements loaded are dictionnaries stored as json files in the measurements folder
		
		Args:
			pname: name of json file as str
			
		Returns: 
			dic: a dictionnary of size measurments
		"""
		
		with open("../measurements/" + pname + "_data.json", "r") as read_file:
			dic = json.load(read_file)		
				
		return dic

	############################################################

	def save_measurements(self, ofname=None):
		""" Save new measurements
		
		Save new measurements in ofname_data.json file in the mesures folder
		If no output format is given stores the data under the attribute self.pname
		
		Args:
			ofname: output json filename as str
			
		"""
		if ofname:
			with open("../measurements/" + ofname + "_data.json", "w") as write_file:
				json.dump(self.m, write_file)		
		else:
			with open("../measurements/" + self.pname + "_data.json", "w") as write_file:
				json.dump(self.m, write_file)		
	############################################################
		
	def intersec_manches(self, A, B, C, theta):
		""" Intersection calculation
		
		Finds the point of intersection G of the AB line with the line going through C 
		and making an  angle theta with the horizontal axis. 
		Especially useful for sleeve heads.
		Does not work if AB is vertical !!!
				
		Args:
			A,B,C: points given as array([x,y])
			theta: angle in radians
		
		Returns:
			(x,y) tuple of coordinates
		"""
	
		# coefficient de AB
		aD1  =  (B[1]-A[1])/(B[0]-A[0])
		bD1  =  A[1] - aD1*A[0]
		
		#coefficients de CG
		aD2 = np.tan(theta*np.pi/180)
		bD2 = C[1] - aD2*C[0]
		
		#intersection
		x = (bD2-bD1)/(aD1-aD2)
		y = aD1*x+bD1
		
		return (x, y)
		
	############################################################
		
	def segment_angle(self, A, B):
		"""Returns slope of segment [AB]
		
		Args:
			A,B: points given as array([x,y])
		
		
		Returns:
			angle in radians
		"""
		return np.arctan((B[1]-A[1])/(B[0]-A[0]))
		
	############################################################

	def middle(self, A, B):
		"""
		returns the middle point of [AB]
		
		Args:
			A,B: points given as array([x,y])
		
		
		Returns:
			x,y as an array
				"""
		
		return np.array([0.5*(A[0]+B[0]), 0.5*(A[1]+B[1])])
	
	############################################################

	def segment(self, A, B, ax, kwargs={'color':'blue'}):
		"""
		plots [AB] segment on ax

		Args:
			A,B: points given as array([x,y])
			ax: axis on which to plot
			kwargs: dictionnary of drawing porperties			
		"""
		
		ax.plot([A[0], B[0]], [A[1], B[1]],  **kwargs)	
		
	############################################################

	def distance(self, A, B):
		"""
		returns distance [AB]
		
		Args:
			A,B: points given as array([x,y])
		
		
		Returns:
			distance as a float
		"""
		
		return np.sqrt((A[0]-B[0])**2+(A[1]-B[1])**2)
		
	############################################################

	def pistolet(self, points, kval, ax=None, kwargs = {'color':'blue','linestyle':'solid'}, tot=False):
		"""French curve calculation
		
		calculates a spline of order kval from set of given points.
		if ax given draws the result on ax and returns length of Armhole
		if tot returns a list of 30 points to draw the spline curve.
		
		Args:
			points: array of tuples
			kval: int
			ax: matplotlib axis
			kwargs: dictionnary of drawing properties
			tot: boolean deciding whether the entire curve is returned
			
		Returns:
			Total distance if tot = False
			Total distance and list of interpolated points if tot = True 
		"""
		tck, u  =  splprep([points.transpose()[0], points.transpose()[1]], k = kval, s=0)
		us  =  np.linspace(u.min(),  u.max(),  30)
		new_points  =  splev(us,  tck)
		if ax:
			ax.plot(new_points[0],  new_points[1],  **kwargs)
		
		dx = np.diff(new_points[0])
		dy = np.diff(new_points[1])
				
		if tot:
			point_vertices = []
			for i in range(len(new_points[0])):
				point_vertices.append([new_points[0][i], new_points[1][i]])
			return  np.sum(sqrt(dx**2+dy**2)), point_vertices
			
		else:
			return  np.sum(sqrt(dx**2+dy**2))

	############################################################
			
	def draw_pattern(self, dic_list, vertices_list):
		
		"""
		for each dic in dic_list
			plots points given in dic
		for each vertices in vertices_list 
			draws the polygon defined by vertices_list
			
			The figure is a 1:1 scaled pattern ready to print on a
			full size AO printer.
		
		Args:
			dic_list: list of dictionnaries of points to be plotted as points
				with label
			vertices_list: list of vertices_list to be plotted as lines
			
		Returns:
			fig, ax
		"""

		####################################################
		#       Figure size calculation and axes creation
		####################################################

		xmin=0
		ymin=0
		xmax=0
		ymax=0
		
		for vertice in vertices_list:
			for val in vertice:
				if int(val[0]) < xmin:
					xmin = int(val[0])
				if int(val[0]) > xmax:
					xmax = int(val[0])
				if int(val[1]) < ymin:
					ymin = int(val[1])
				if int(val[1]) > ymax:
					ymax = int(val[1])

		for dic in dic_list:
			for key, val in dic.items():
				if int(val[0]) < xmin:
					xmin = int(val[0])
				if int(val[0]) > xmax:
					xmax = int(val[0])
				if int(val[1]) < ymin:
					ymin = int(val[1])
				if int(val[1]) > ymax:
					ymax = int(val[1])

		offset=5
		
		H=ymax-ymin+2*offset
		W=xmax-xmin+2*offset
		
		fig = plt.figure(figsize = (W/2.54, H/2.54))		
		ax = axes([0, 0, 1, 1])
		ax.axis('square')

		####################################################
		#       plot pattern
		####################################################

		for dic in dic_list:
			for key, val in dic.items():
				ax.plot(val[0], val[1], 'ro')
				ax.text(val[0]+0.2, val[1], key, ha = 'left')
		
		for vertices in vertices_list:
			poly  =  Polygon(vertices,  facecolor = '0.9',  edgecolor = '0.5')
			ax.add_patch(poly)
			
		####################################################
		#       Figure parameters before output
		####################################################
		
		
		ax.set_xticks(np.arange(xmin-offset, xmax+offset))
		ax.set_yticks(np.arange(ymin-offset, ymax+offset))
		ax.grid('on')
		
		plt.tick_params(
		axis = 'x',           # changes apply to the x-axis
		which = 'both',       # both major and minor ticks are affected
		bottom = False,       # ticks along the bottom edge are off
		top = False,          # ticks along the top edge are off
		labelbottom = False)
		
		plt.tick_params(
		axis = 'y',           # changes apply to the x-axis
		which = 'both',       # both major and minor ticks are affected
		left = False,       # ticks along the bottom edge are off
		right = False,          # ticks along the top edge are off
		labelleft = False)
		
		#~ fig.set_size_inches(60/2.54, 60/2.54)
		ax.set_xlim(xmin-offset, xmax+offset)
		ax.set_ylim(ymin-offset, ymax+offset)
		
		return fig, ax

	def paper_cut(self, fig, ax, name='patternA4', paper='A4'):	
		"""
		Cuts a pattern according to different paper sizes
		No overlap but the grid should suffice
		
		
		Args:
			fig: the figure on wich to plot
			ax: the axis on which to plot
			name: the output filename
			paper: the paper format for the cut
			
		Returns:
			fig, ax
		"""
		
		paper_dic = {'A4': (19, 27.7), 'A3': (27, 40), 'Legal' : (19.6, 33.6), 'Letter' : (19.6, 25.9), 'Tabloid': (25.9, 41.2), 'Ledger': (25.9, 41.2)}
		from math import ceil
		xmin, xmax = ax.get_xlim()
		ymin, ymax = ax.get_ylim()
		
		w = xmax-xmin
		h = ymax-ymin

		minval, maxval = paper_dic[paper]
		
		n1 = ceil(w/maxval) * ceil(h/minval)
		n2 = ceil(w/minval) * ceil(h/maxval)
		
		if n1 >= n2:
			nx = ceil(w/minval)
			ny = ceil(h/maxval)
			x = minval
			y = maxval	
		else:
			nx = ceil(w/maxval)
			ny = ceil(h/minval)
			x = maxval
			y = minval
			
		fig.set_size_inches(x/2.54, y/2.54)

		fname = '../patterns/' + self.style + '_' + name + '_' + self.pname + '_' + paper + '.pdf'
		with PdfPages(fname) as pdf:
			for i in range(nx):
				for j in range(ny):
					ax.set_xlim(xmin+i*x, min(xmin+(i+1)*x, xmax))
					ax.set_ylim(ymin+j*y, min(ymin+(j+1)*y, ymax))
					fname = 'p%i-%i' % (i, j) 
					
					x1, x2 = ax.get_xlim()
					xpos = 0.5*(x1+x2)

					y1, y2 = ax.get_ylim()
					ypos = 0.5*(y1+y2)

					ax.text(xpos, ypos, fname, fontsize=16, ha='center')
					pdf.savefig()
								
			ax.set_xlim(xmin, xmax)
			ax.set_ylim(ymin, ymax)
			for i in range(nx):
				xpos=min(xmin+(i+1)*x, xmax)
				ax.plot((xpos, xpos), (ymin, ymax), 'k-')
			for j in range(ny):
				ypos=min(ymin+(j+1)*y, ymax)
				ax.plot((xmin, xmax), (ypos, ypos), 'k-')
			
			pdf.savefig()

		fig.set_size_inches((xmax-xmin)/2.54, (ymax-ymin)/2.54)
		return fig, ax

	def print_info(self, ax, model=None):

		"""
		print generic info on each graph.
		
		Args:
			ax: ax on which to print info
			model: a dictionnary of informations to be printed
		
		Returns:
			ax
		
		"""
		xmin, xmax = ax.get_xlim()
		ymin, ymax = ax.get_ylim()
		
		ax.text(xmin+3, ymax-1, "Style: %s" % (self.style))
		ax.text(xmin+3, ymax-2, "Gender: %s" % (self.gender))
		ax.text(xmin+3, ymax-3, "Measurements: %s" % (self.pname))
		y=4
		if model:
			for key, val in model.items():
					ax.text(xmin+3, ymax-y, "%s: %s" % (key, val))
					y+=1
		return ax
		
###############################################################
# Basic templates (bodice, skirt, trousers, sleeves) 
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
		"""

		#Front
		A = np.array([0, self.m["longueur_tot"]])
		B = np.array([self.m["tour_bassin"]/4, self.m["longueur_tot"]])
		C = np.array([0, 0])
		D = np.array([B[0], 0])
		E = np.array([0, A[1] - self.m["montant"]])
		F = np.array([B[0], E[1]])
		G = A - [0, self.m["hauteur_bassin"]]
		H = np.array([B[0], G[1]] )
		E1 = E - [self.m["tour_bassin"]/20, 0]
		I = E - [0, self.m["montant"]]
		L = np.array([B[0], I[1]])
		X = np.array([0.5 * (E1[0] + F[0]), E1[1]])
		M = np.array([X[0], A[1] - 0.5])
		N = np.array([X[0], C[1]])
		O = np.array([X[0], M[1] - self.m["hauteur_genou"]])
		M2 = M + [6, 0]
		X1 = np.array([X[0], I[1]])
		L1 = X1 + [self.m["tour_cuisse"]/4 - 1, 0] # Originally 12.5 ?
		I1 = X1 - [self.m["tour_cuisse"]/4 - 1, 0]
		N1 = N + [0, 1.5] # provenance ?
		C1 = N - [self.m["tour_cheville"]*3/8 - 1, 0] # originally 11 ?
		D1 = N + [self.m["tour_cheville"]*3/8 -1, 0]
		A1 = A + [1, 0]
				
		# points en plus
		E1G = np.array([E[0] + (E1[0]-E[0])/5, E[1] + (G[1]-E[1])/3]) # permet une jolie courbe de fourche avant

		ONC1 = C1 + [0, 10] # permettent un tombé droit sous le genou.
		OND1 = D1 + [0, 10]
		
		dfa, self.fourche_avant = self.pistolet(np.array([E1, E1G, G]), 2, tot = True)
		dha, self.ceinture_avant = self.pistolet(np.array([A1, M, M2, B]), 2, tot = True)
		dia, self.interieur_avant = self.pistolet(np.array([C1, ONC1, I1, E1]), 3, tot = True)
		dca, self.exterieur_avant = self.pistolet(np.array([B, H, L1, OND1, D1]), 4, tot = True)
		
		Front_Points_Names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'E1', 'I', 'L', 'X', 'M', 'N', 'O', 'M2', 'X1', 'L1', 'I1', 'N1', 'C1', 'D1', 'A1']
		Front_Points_List = [A, B, C, D, E, F, G, H, E1, I, L, X, M, N, O, M2, X1, L1, I1, N1, C1, D1, A1]
		
		for i in range(len(Front_Points_Names)):
			self.Trousers_Front_points_dic[Front_Points_Names[i]] = Front_Points_List[i]
			
		self.Trousers_Front_vertices = self.interieur_avant + self.fourche_avant + self.ceinture_avant + self.exterieur_avant + [N1, C1]
		
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
		
		A = np.array([dx + self.m["tour_bassin"]/4 + 2, self.m["longueur_tot"]])
		B = np.array([dx, A[1]])
		C = np.array([A[0], 0])
		D = np.array([dx, 0])
		
		E = A - [0, self.m["montant"]]  #crotch line
		F = np.array([B[0], E[1]])
		
		G = A - [0, self.m["hauteur_bassin"]] # hip line
		H = np.array([B[0], G[1]])

		E1 = E + [self.distance(E, F)/3 + 1.5, 0]
		E2 = E1 - [0, 2]
		
		I = E - [0, self.m["montant"]]
		L = np.array([F[0], I[1]])

		X = self.middle(E1, F)
		M = np.array([X[0], A[1]])
		N = np.array([X[0], C[1]])
		X1 = np.array([X[0], I[1]])
		
		O = np.array([X[0], M[1] - self.m["hauteur_genou"]])
		A1 = A - [4.5, 0]
		A2 = A1 + [0, 2] 
		B1 = B - [0, 0.5]
		
		a = self.segment_angle(A2, B1)
		waist = self.distance(A, B)
		B3 = A2 - (waist*np.cos(a), waist*np.sin(a))
		B4 = A2 - (2*waist*np.cos(a)/3, 2*waist*np.sin(a)/3)
		I1 = X1 + (self.m["tour_cuisse"]/4 + 1, 0) # thigh originally 14 ?
		L1 = X1 - (self.m["tour_cuisse"]/4 + 1, 0)
		
		C1 = N + (self.m["tour_cheville"]*3/8 + 1, 0) # orignally 12
		D1 = N - (self.m["tour_cheville"]*3/8 + 1, 0)
		N1 = N - (0, 1.5)
		
		
		# points supplémentaires
		
		CC1 = C1 + (0, 10)
		DD1 = D1 + (0, 10)
		

		E3 = E2 - (2, 0)
		EG = self.middle(E, G)
		
		dfa, self.fourche_arriere = self.pistolet(np.array([EG, E3, E2]), 2, tot = True)
		dia, self.interieur_arriere = self.pistolet(np.array([E2, I1, CC1, C1]), 3, tot = True)
		dea, self.exterieur_arriere = self.pistolet(np.array([D1, DD1, L1, F, B3]), 4, tot = True)	
		
		Back_Points_Names=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'E1', 'E2', 'I', 'L', 'X', 'M', 'N', 'O', 'A1', 'A2', 'B1', 'B3', 'B4', 'I1', 'L1', 'C1', 'D1', 'N1']
		Back_Points_List=[A, B, C, D, E, F, G, H, E1, E2, I, L, X, M, N, O, A1, A2, B1, B3, B4, I1, L1, C1, D1, N1]
		
		for i in range(len(Back_Points_Names)):
			self.Trousers_Back_points_dic[Back_Points_Names[i]] = Back_Points_List[i]
			
		self.Trousers_Back_vertices = self.exterieur_arriere + [B4, A2] + self.fourche_arriere + self.interieur_arriere + [N1, D1]
		
		self.back_width=self.distance(B3, A)+self.distance(E, E1)
		print(self.back_width)
		
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

	
class Basic_Bodice(Pattern):
	"""
	Class to calculate and draw a basic Bodice pattern.
	For male its more a shirt than a Bodice.
	Inherits from Pattern
	
	Attributes
	
		style: style used to draw the pattern as string (Gilewska, Donnanno, Chiappetta for now)
		
		# Attributes that control the dictionnaries used for size measurements
		age: ade og the kid in Chiapetta's patterns
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
	
	def __init__(self, pname="sophie", gender='m', style='Donnanno', age=12):
		"""
		Initilizes parent class &  attributes
		launches the calculation of bodice and sleeve
		saves measurements performed like armscye depth in the json measurements file for further processing in other classes
		
		Args:
			pname: size measurements
			gender: ..
			style: style to be used for drafting
			age: used if for a child and style = Chiappetta.
			
		"""
		Pattern.__init__(self, pname, gender)
		
		self.style=style
		self.age=age
		
		self.Bodice_points_dic = {}
		self.Bodice_Front_points_dic = {}
		self.Bodice_Back_points_dic = {}
		self.Sleeve_points_dic = {}

		self.Front_Bodice_vertices = []
		self.Back_Bodice_vertices = []
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
		
		self.save_measurements()
		
	############################################################


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
	
		# 1 draw
		fig, ax = self.draw_pattern([self.Bodice_points_dic], [self.Bodice_Front_vertices, self.Bodice_Back_vertices])
			
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
		
		self.segment(spd['A'], [0, 0], ax, bl_dic)
		
		if self.gender=='w':
			x, y = self.middle(spd['W'], spd['W1'])
			ax.text(x, y, 'FRONT', ha='center')

			x, y = self.middle(spd['W'], spd['W0'])
			ax.text(x, y, 'BACK', ha='center')
		
		else:
			x = spd['B'][0]
			y = spd['B'][1]/2
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
		ax = self.print_info(ax, {"Sleeve length": round(spd['A'][1],1), "Sleeve width": round(width,1)})

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
		ax.text(pos[0]- 0.5, pos[1], 'FOLD LINE', fontsize=fs, rotation = 90)

		pos = self.middle(bpd['WF'], bpd['SlF'])
		ax.text(pos[0]+ 0.5, pos[1], 'FOLD LINE', fontsize=fs, rotation = 90)
		
		ldic={'color':'blue', 'alpha':0.4, 'linestyle':'dashed'}
		
		self.segment(bpd['WF'], bpd['WB'], ax, ldic)
		pos = self.middle(bpd['WF'], bpd['WB'])
		ax.text(pos[0], pos[1]+0.5, 'WAIST LINE', fontsize=fs, ha='center')

		self.segment(bpd['SlF'], bpd['SlB'], ax, ldic)
		pos = self.middle(bpd['SlF'], bpd['SlB'])
		ax.text(pos[0], pos[1]+0.5, 'SLEEVE LINE', fontsize=fs, ha='center')

		self.segment(bpd['BF'], bpd['BB'], ax, ldic)
		pos = self.middle(bpd['BF'], bpd['BB'])
		ax.text(pos[0], pos[1]+0.5, 'BUST LINE', fontsize=fs, ha='center')
		
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
		A = [0, m["longueur_devant"]]
		B = [0, 0]
		C = [(m["tour_poitrine"]+bust_ease)/2, 0]
		D = [(m["tour_poitrine"]+bust_ease)/2, m["longueur_dos"]]
		E = [(m["tour_poitrine"]+bust_ease)/4, 0]
		F = [(m["tour_poitrine"]+bust_ease)/4, m["longueur_devant"]]
		
				
		#################################################
		# Bust line
		#################################################
		H = [(m["tour_poitrine"]+bust_ease)/2, m["longueur_dos"]/2]
		I = [0, m["longueur_dos"]/2]
		Q = [E[0], H[1]]
		
		
		G = [3*(m["tour_poitrine"]+bust_ease)/10, m["longueur_dos"]]
		H1 = [3*(m["tour_poitrine"]+bust_ease)/10, m["longueur_dos"]/2]
		
		I1 = [2*(m["tour_poitrine"]+bust_ease)/10-1.5, m["longueur_dos"]/2]
		J1 = [I1[0], A[1]]
		
		
		#################################################
		# Torso or shoulder line
		#################################################
		L = [H[0], H[1]+(D[1]-H[1])/3]
		M = [0, L[1]]
		
		
		L1 = [H1[0], L[1]]
		J = [I1[0], L[1]]
		
		
		O = [G[0], G[1]-1.5]
		
		
		shoulder_width = (D[0]-G[0]-1)
		N  =  [D[0]-(shoulder_width/2 - 2), D[1]]
		P  =  [N[0], N[1]+2.5]
		
		controle_1  =  [D[0]-1, D[1]]
		controle_2  =  [N[0]+1, N[1]+1]
		points_col_dos = np.array([D, controle_1, controle_2, P])
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
			P1 = [O[0]+dOP1*np.cos(a+np.pi), O[1]+dOP1*np.sin(a+np.pi)]
		print("[PP1]", self.distance(P, P1))
	
		# Front
		U = [shoulder_width/2-2, A[1]]
		U1 = [0, A[1]-U[0]]
		U2 = [A[0]+U[0]*np.cos(-np.pi/4), A[1]+U[0]*np.sin(-np.pi/4)]		
		dfcol, col_devant = self.pistolet(np.array([U1, U2, U]), 2, tot=True)
		
		Z = [J1[0], J1[1]-5]
		a = self.segment_angle(U, Z)
		if m["longueur_epaule"] == 0:
			Z2 = Z
		else: 
			Z2  =  [U[0]+m["longueur_epaule"]*np.cos(a), U[1]+m["longueur_epaule"]*np.sin(a)]		
		print("[UZ2]", self.distance(U, Z2))
		
		#################################################
		# Armhole or Armscye
		#################################################
		# Back
		bd = 1.5
		controle = [H1[0] - bd, H1[1] + bd]
		
		m["longueur_emmanchure_dos"], emmanchure_dos = self.pistolet(np.array([P1, L1, controle, Q]), 2, tot=True)
		print("Longueur emmanchure dos: %4.0f" % (m["longueur_emmanchure_dos"]))

		#front
		fd = 1.8
		controle = [I1[0] + fd, I1[1] + fd]
		
		
		
		m["longueur_emmanchure_devant"], emmanchure_devant = self.pistolet(np.array([Z2, J, controle, Q]), 2, tot=True)
		print("Longueur emmanchure devant: %4.0f" % (m["longueur_emmanchure_devant"]))

		#################################################
		# Dictionnaries and vertices
		#################################################
		self.Bodice_points_dic={}
		Bodice_Points_Names=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'L', 'M', 'N', 'O', 'P', 'P1', 'Q', 'U', 'Z', 'H1', 'I1', 'J1', 'L1', 'U1', 'U2', 'Z2']
		Bodice_Points_List=[A, B, C, D, E, F, G, H, I, J, L, M, N, O, P, P1, Q, U, Z, H1, I1, J1, L1, U1, U2, Z2]
		
		for i in range(len(Bodice_Points_Names)):
			self.Bodice_points_dic[Bodice_Points_Names[i]] = Bodice_Points_List[i]
			
		self.Bodice_Front_vertices = [B, U1] + col_devant + [Z] + emmanchure_devant + [Q, E]
		self.Bodice_Back_vertices = [C, D] + col_dos + [O] + emmanchure_dos + [Q, E]
		
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
		A = np.array([0, m["longueur_devant"]])
		B = np.array([0, 0])
		C = np.array([(m["tour_poitrine"]+bust_ease)/2, 0])
		D = np.array([(m["tour_poitrine"]+bust_ease)/2, m["longueur_dos"]])
		E = np.array([(m["tour_poitrine"]+bust_ease)/4, 0])
		F = np.array([(m["tour_poitrine"]+bust_ease)/4, m["longueur_devant"]])
		
				
		#################################################
		# Bust line
		#################################################
		H = np.array([(m["tour_poitrine"]+bust_ease)/2, m["longueur_dos"]/2])
		I = np.array([0, m["longueur_dos"]/2])
		Q = np.array([E[0], H[1]])
		
		
		G = D - [m["largeur_epaule"]/2 +1, 0] # ca merde dans les "grandes" largeurs... j'utilise donc la méthode pour les femmes
		#~ G = D - [(m["tour_poitrine"]+bust_ease)/5 +1, 0]
		H1 = H - [m["largeur_epaule"]/2 +1, 0]
		#~ H1 = H - [(m["tour_poitrine"]+bust_ease)/5 +1, 0]
		
		I1 = H1 - [(m["tour_poitrine"]+bust_ease)/10 + 2, 0]
		J1 = np.array([I1[0], A[1]])
		
		#################################################
		# Torso or shoulder line
		#################################################
		L = H + [0, (D[1]-H[1])/3]
		M = np.array([0, L[1]])
		
		
		L1 = np.array([H1[0], L[1]])
		J = np.array([I1[0], L[1]])
		
		
		O = G -[0, 2.5]
		
		shoulder_width = (D[0]-G[0])
		N  =  D - [(shoulder_width/3 + 0.6), 0]
		P  =  N + [0, 2.5]
		
		controle_1  =  [D[0]-1, D[1]]
		controle_2  =  [N[0]+1, N[1]+1]
		points_col_dos = np.array([D, controle_1, controle_2, P])
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
		U1 = A - [0, U[0]]
		U2 = [A[0]+U[0]*np.cos(-np.pi/4), A[1]+U[0]*np.sin(-np.pi/4)]		
		dfcol, col_devant = self.pistolet(np.array([U1, U2, U]), 2, tot=True)
		
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
		controle = [H1[0] - bd, H1[1] + bd]
		
		m["longueur_emmanchure_dos"], emmanchure_dos = self.pistolet(np.array([P1, L1, controle, Q]), 2, tot=True)
		#~ m["longueur_emmanchure_dos"], emmanchure_dos = self.pistolet(np.array([P1, L1, Q]), 2, tot=True)
		print("Longueur emmanchure dos: %4.0f" % (m["longueur_emmanchure_dos"]))

		#front
		fd = 1.8
		controle = [I1[0] + fd, I1[1] + fd]
		
		
		
		m["longueur_emmanchure_devant"], emmanchure_devant = self.pistolet(np.array([Z2, J, controle, Q]), 2, tot=True)
		#~ m["longueur_emmanchure_devant"], emmanchure_devant = self.pistolet(np.array([Z2, J, Q]), 2, tot=True)
		print("Longueur emmanchure devant: %4.0f" % (m["longueur_emmanchure_devant"]))

		#################################################
		# Basic Shirt Base and Dart
		#################################################
		
		Y = B - [0, m["hauteur_bassin"]]
		X = C - [0, m["hauteur_bassin"]]
		E1 = self.middle(X, Y)
		
		dXC1 = 75 - self.distance(D, X)
		C1 = X - [0, dXC1]
		B1 = np.array([Y[0], C1[1]+2])
		E3 = np.array([E1[0], B1[1]])
		E2 = np.array([E1[0], C1[1]])
		
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
		l_base_back, base_back = self.pistolet(np.array([E1, rE1, rC12, rC11, rC10]), 3, tot=True)
		
		#################################################
		# Dictionnaries and vertices
		#################################################
		self.Bodice_points_dic={}
		Bodice_Points_Names=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'L', 'M', 'N', 'O', 'P', 'P1', 'Q', 'U', 'Z', 'H1', 'I1', 'J1', 'L1', 'U1', 'U2', 'Z2', 'Y', 'E1', 'X', 'B1', 'E3', 'E2', 'C1']
		Bodice_Points_List=[A, B, C, D, E, F, G, H, I, J, L, M, N, O, P, P1, Q, U, Z, H1, I1, J1, L1, U1, U2, Z2, Y, E1, X, B1, E3, E2, C1]
		
		for i in range(len(Bodice_Points_Names)):
			self.Bodice_points_dic[Bodice_Points_Names[i]] = Bodice_Points_List[i]
			
		self.Bodice_Front_vertices = [B, U1] + col_devant + [Z] + emmanchure_devant + [Q, W1, E1] + base_front + [B1]
		self.Bodice_Back_vertices = [C, D] + col_dos + [O] + emmanchure_dos + [Q, W, E1] + base_back + [C1]


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
			WB = np.array([self.m['tour_poitrine']/2 + d_FB, 0])
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
			collar_back_points = np.array([HB, ClCB2, ClCB, CB2])
			self.m['longueur_col_dos'], back_collar_curve = self.pistolet(collar_back_points, 2, tot = True)
			#armhole			
			self.m["longueur_emmanchure_dos"], back_sleeve_curve =  self.pistolet(np.array([ShB1, BB1, SlB1]), 2, tot=True)
			
			# Front bodice
			WF = np.array([0, 0])
			WF1 = WF + [self.m["tour_poitrine"]/4, 0]
			
			HF = WF + [0, CB2[1]]
			
			SlF = WF + [0, SlB[1]]
			SlF1 = SlF + WF1
			
			BF = WF + [0, BB[1]]
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
			ClCF = [CF2[0]+lcf*np.cos(3*np.pi/4), CF1[1]+lcf*np.sin(3*np.pi/4)]
			
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

			self.Bodice_Back_vertices = [WB, HB] + back_collar_curve + [ShB1] + back_sleeve_curve + [SlB1, WB1]
			self.Bodice_Front_vertices = [WF, CF1] + front_collar_curve + [ShF1] +  front_sleeve_curve + [SlF1, WF1]



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
		WB = np.array([0, 0]) #A
		WB1 = np.array([self.m["tour_poitrine"]/4, 0]) #A1
		#3
		HB = np.array([0, self.m["longueur_dos"]]) #B
		HB1 = np.array([self.m["largeur_epaule"]/2, HB[1]]) #B1
		#4
		SlB = np.array([0, HB[1]/2+1]) # ligne d'emmanchure C
		SlB1 = np.array([WB1[0], SlB[1]]) # C1
		#5
		BB = np.array([0, SlB[1] + (HB[1] - SlB[1])/3 +1]) # ligne de carrure D
		BB1 = np.array([self.m["carrure_dos"]/2, BB[1]]) # D1
		#6
		B2 =  np.array([self.m["tour_encolure"]/6+1, HB[1]]) # keep it B2
		
		#################################################
		# Front Frame
		#################################################
		#7
		x_dev = WB1[0]+BF_space
		#8
		WF = np.array([x_dev+self.m["tour_poitrine"]/4, 0]) #E
		WF1 = np.array([x_dev, 0]) #E1
		#10
		HF = np.array([WF[0], self.m["longueur_devant"]]) #F
		HF1 = HF + [-self.m["largeur_epaule"]/2, 0] #F1
		#11
		SlF = np.array([WF[0], SlB[1]]) #G
		SlF1 = np.array([x_dev, SlF[1]]) #G1
		#12
		BF = np.array([WF[0], BB[1]]) #H
		BF1 = BF + [-self.m["carrure_devant"]/2, 0] #H1
		#13
		CF1 = HF + [-self.m["tour_encolure"]/6 -1, 0] #F2

		#################################################
		# Add Hip
		#################################################
		HiB = np.array([0, -self.m['hauteur_bassin']])
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
			ShB1 = [ShB1[0]+delta*np.cos(a), ShB1[1]+delta*np.sin(a)] #add length difference
			
			dShB = self.distance(CB1,  ShB1)	# recalculate and check				
		print("longueur épaule dos\n\t mesurée:%4.0f\n\t calculée: %4.0f" % (self.m["longueur_epaule"], dShB))
		
		
		###### ###########################################
		# Back Sleeve
		#################################################
		#18
		b_length=2.5 # max 3cm
		CPSlB = [BB1[0] + np.cos(np.pi/4)*b_length, SlB1[1] + np.sin(np.pi/4)*b_length]
		#~ CPSlB1 = SlB1 - [0.5, 0]
		# This test is necessary because in some cases the carrue dos is close to the
		# bust width so the control point abcissa is larger then the sleeve point
		 
		if CPSlB[0] < SlB1[0]: 
			self.m["longueur_emmanchure_dos"], sleeve_back_points =  self.pistolet(np.array([ShB1, BB1, CPSlB, SlB1]), 2, tot=True)
		else:
			self.m["longueur_emmanchure_dos"], sleeve_back_points =  self.pistolet(np.array([ShB1, BB1, SlB1]), 2, tot=True)
		print("Longueur emmanchure dos: %4.0f" % (self.m["longueur_emmanchure_dos"]))

		#################################################
		# Front Collar
		#################################################
		#17
		CF = [HF[0], HF[1]-self.m["tour_encolure"]/6 -1]
		CPCF = [CF[0]-1, CF[1]] # slightly different from Gilewska
		self.m['longueur_col_devant'], collar_front_points = self.pistolet(np.array([CF, CPCF, CF1]), 2, tot=True)
		
		
		#################################################
		# Front Shoulder
		#################################################
		#16
		#~ ShF1 = [HF1[0], HF1[1]-7] #valeur Gilewska je la trouve très élevée et les longueurs d'épaules ne coincident pas
		ShF1 = [HF1[0], HF1[1]-5] # valeur Donnanno  et là les  longueurs d'épaules coincident...
		
		dShF = self.distance(CF1,  ShF1)	
		if self.m["longueur_epaule"]>0:
			a = self.segment_angle(CF1, ShF1) # shoulder line angle
			delta = self.m["longueur_epaule"] - dShF # calculate length differnce
			print("delta", delta)
			ShF1 = [ShF1[0]+delta*np.cos(a+np.pi), ShF1[1]+delta*np.sin(a+np.pi)] #add length difference
					
			dShF=self.distance(CF1, ShF1) 	# recalculate and check				
		print("longueur épaule devant\n\t mesurée:%4.0f\n\t calculée: %4.0f" % (self.m["longueur_epaule"], dShF))		
		
		
		#################################################
		# Front Sleeve
		#################################################
		#19
		f_length = 2 #max 2.2
		CPSlF = [ BF1[0]-np.cos(np.pi/4)*f_length, SlF1[1]+np.sin(np.pi/4)*f_length] 
		CPSlF1 = SlF1 + [0.5, 0] #point added to ensure correct tangents.
		#~ CPSlF2 = BF1 + [0, -1] #point added to ensure correct tangents.
		#~ CPSlF3 = self.middle(BF1, ShF1) #point added to ensure correct tangents.
		
		self.m["longueur_emmanchure_devant"], sleeve_front_points  =   self.pistolet(np.array([ShF1, BF1,  CPSlF, CPSlF1, SlF1]), 2, tot=True)
		#~ self.m["longueur_emmanchure_devant"], sleeve_front_points  =   self.pistolet(np.array([ShF1, BF1, SlF1]), 2, tot=True)
		print("Longueur emmanchure devant: %4.0f" % (self.m["longueur_emmanchure_devant"]))

		
		#################################################
		# Sleeve depth
		#################################################
		xYP = (WB1[0]+x_dev)/2		
		YP_emmanchure  =  self.segment_angle(ShB1, ShF1)*(xYP - ShB1[0]) + ShB1[1]
		DS = [xYP, YP_emmanchure]
		self.m["profondeur_emmanchure"]  =  YP_emmanchure - SlB1[1]
		print("Profondeur d'emmanchure: %4.0f" % (self.m["profondeur_emmanchure"]))
	
		########################################
		#Create points dictionnary
		########################################		

		Back_Points_list  =  [HiB, HiB1, WB,  SlB,  BB,  HB, HB1, CB1,  ShB1,  BB1,  CPSlB,  SlB1,  WB1, DS, B2]
		Back_Points_Names  =  ['HiB', 'HiB1', 'WB', 'SlB', 'BB', 'HB', 'HB1', 'CB1', 'ShB1', 'BB1', 'CPSlB', 'SlB1', 'WB1', 'DS', 'B2']
		
		for i in range(len(Back_Points_Names)):
			self.Bodice_points_dic[Back_Points_Names[i]] = Back_Points_list[i]

		Front_Points_list  =  [HiF, HiF1, WF,  SlF,  BF, CF,  CPCF,  CF1,  ShF1,  BF1,  CPSlF,  SlF1,  WF1, HF, HF1]
		Front_Points_Names  =  ['HiF', 'HiF1', 'WF', 'SlF', 'BF', 'CF', 'CPCF', 'CF1', 'ShF1', 'BF1', 'CPSlF', 'SlF1', 'WF1', 'HF', 'HF1']
		for i in range(len(Front_Points_Names)):
			self.Bodice_points_dic[Front_Points_Names[i]] = Front_Points_list[i]
			
		
		#########################################
		#Create Vertices 
		#for polygon representation
		#########################################	

		self.Bodice_Back_vertices  =  [HiB,  WB,  HB ] + collar_back_points +  sleeve_back_points + [SlB1, HiB1]		
		self.Bodice_Front_vertices  =  [HiF,  SlF,  BF ] + collar_front_points +  sleeve_front_points + [SlF1,  HiF1]

		self.curves_dic = {'Back_Collar': collar_back_points, 'Back_Sleeve': sleeve_back_points, 'Front_Collar': collar_front_points, 'Front_Sleeve': sleeve_front_points}
		
	
	def Gilewska_basic_sleeve_m(self):
		""" Calculation of basic sleeve
			for Men using Gilewska technique			
		"""
						
		#########################################
		#squeleton
		#########################################
		O = np.array([0,  0])
		A = np.array([0,  self.m["longueur_manche"]])
		B = A + [0, - self.m["profondeur_emmanchure"]*4/5]
		
		C = np.array([-(self.m["longueur_emmanchure_dos"]*3/4 + 1),  B[1]])
		D = np.array([self.m["longueur_emmanchure_devant"]*3/4 + 1,  B[1]])

		
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
		Kb1 = np.array([Kb[0]+0.5*np.cos(a-np.pi/2), Kb[1]+0.5*np.sin(a-np.pi/2)])
		Kh1 = np.array([Kh[0]+1.5*np.cos(a+np.pi/2), Kh[1]+1.5*np.sin(a+np.pi/2)])
		
		points = np.array([C1, Kb1, K, Kh1, E, A])
		dbc, back_curve_points =  self.pistolet(points, 4, tot=True)
				
		#########################################
		#curve for the front
		#########################################
		
		G = self.middle(D1, F)
		Gb = self.middle(D1, G)
		Gh = self.middle(G, F)
		
		a = self.segment_angle(D1, F)
		print(a)
		Gb1 = np.array([Gb[0]+0.8*np.cos(a-np.pi/2), Gb[1]+0.8*np.sin(a-np.pi/2)])
		Gh1 = np.array([Gh[0]+1.8*np.cos(a+np.pi/2), Gh[1]+1.8*np.sin(a+np.pi/2)])
		#~ points = np.array([D1, Gb1, G, Gh1, F, A])
		points = np.array([A, F, Gh1, G, Gb1, D1])
		dfc, front_curve_points = self.pistolet(points, 4, tot=True)

		
		#########################################
		# wrist
		#########################################

		S = np.array([self.m["tour_poignet"]/2, 0])
		V = np.array([-self.m["tour_poignet"]/2, 0])
			
		self.Sleeve_points_dic = {'A':A, 'B':B, 'C':C, 'D':D, 'E':E, 'F':F, 'C1':C1, 'D1':D1, 'K':K, 'Kb1':Kb1, 'Kh1': Kh1, 'G':G, 'Gb':Gb, 'Gh':Gh, 'Gb1':Gb1, 'Gh1':Gh1, 'V':V, 'S':S}
		self.Sleeve_vertices = [V, C] + back_curve_points + [A] + front_curve_points + [D, S]

		
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
				
		WB = [0, 0]
		WB1 = [self.m["tour_poitrine"]/4 - 1, 0]
		HB = [0, self.m["longueur_dos"]]
		HB1 = [WB[0], HB[1]]
		
		xdev = WB1[0] + sep
		
		WF = [xdev + self.m["tour_poitrine"]/4 + 1, 0]
		WF1 = [xdev, 0]
		HF = [WF[0], self.m["longueur_devant"]]
		HF1 = [WF1[0], HF[1]]
		
		########################################				
		#Collars
		########################################
				
		self.m["profondeur_encolure_dos"]  =  self.m["tour_encolure"]/16
		self.m["largeur_encolure"]  =  self.m["tour_encolure"]/6
		self.m["profondeur_encolure_devant"]  =  self.m["tour_encolure"]/6 + 2

		
		CPCB = [self.m["largeur_encolure"]-1.5*np.cos(np.pi/4), self.m["longueur_dos"]-self.m["profondeur_encolure_dos"]+1.5*np.sin(np.pi/4)]
		CPCF  =  [HF[0]-self.m["largeur_encolure"]+2.5*np.cos(np.pi/4), HF[1]-self.m["profondeur_encolure_devant"]+2.5*np.sin(np.pi/4)] 
	
		CB = [0,  self.m["longueur_dos"] - self.m["profondeur_encolure_dos"]]
		CB1 = [self.m["largeur_encolure"],  self.m["longueur_dos"]]
		
		CF = [HF[0],  HF[1]-self.m["profondeur_encolure_devant"] ]
		CF1 = [HF[0]-self.m["largeur_encolure"],  HF[1]]
		
		# fit for collar points
		pos_encolure_dos = np.array([CB, CPCB, CB1])
		dcb, collar_back_points = self.pistolet(pos_encolure_dos, 2, tot=True)
		self.m['longueur_col_dos'] = round(dcb,1)
		
		pos_encolure_devant = np.array([CF, CPCF, CF1])
		dcf, collar_front_points = self.pistolet(pos_encolure_devant, 2, tot=True)
		self.m['longueur_col_devant'] = round(dcf,1)
		
		########################################		
		#Sleeve and Bust lines
		########################################
			
		self.m["hauteur_emmanchure"]  =  self.m["longueur_dos"]/2 + 1
		self.m["hauteur_carrure"]  =  (self.m["longueur_dos"] - self.m["hauteur_emmanchure"] - self.m["profondeur_encolure_dos"])/3 +1
		
		SlB = [0, self.m["hauteur_emmanchure"]]
		SlF = [WF[0], SlB[1]]
		BB = [0, self.m["hauteur_emmanchure"]+self.m["hauteur_carrure"]]
		BF = [WF[0], BB[1]]
		
		########################################		
		#Shoulders
		########################################
				
		x_epaule_dos  =  self.m["longueur_epaule"] * np.cos(14*np.pi/180)
		y_epaule_dos  =  self.m["longueur_epaule"] * np.sin(14*np.pi/180)
		x_epaule_devant  =  self.m["longueur_epaule"] * np.cos(26*np.pi/180)
		y_epaule_devant  =  self.m["longueur_epaule"] * np.sin(26*np.pi/180)
		
		
		ShB1 = [self.m["largeur_encolure"] + x_epaule_dos,  self.m["longueur_dos"] - y_epaule_dos]	
		ShF1 = [HF[0] - self.m["largeur_encolure"] - x_epaule_devant,  self.m["longueur_devant"] - y_epaule_devant]
		
		########################################
		#Sleeve points
		########################################		
		
		BB1  =  [self.m["carrure_dos"]/2,  BB[1]]
		SlB1 =  [WB1[0],  SlB[1]]
		
		b_length = 2 # max 3 I think
		CPSlB  =  [self.m["carrure_dos"]/2 + b_length*np.cos(np.pi/4),  self.m["hauteur_emmanchure"] + b_length*np.sin(np.pi/4)] 
		CPSlB1 = self.middle(ShB1, BB1)

		BF1  =  [BF[0] - self.m["carrure_devant"]/2,  BF[1]]
		SlF1  =  [xdev,  SlF[1]]
		
		f_length = 2.3
		CPSlF  =  [SlF[0] - self.m["carrure_devant"]/2 - f_length*np.cos(np.pi/4),  self.m["hauteur_emmanchure"] + f_length*np.sin(np.pi/4)]
		
		YP_emmanchure  =  self.segment_angle(ShB1, ShF1)*(xdev - ShB1[0]) + ShB1[1]
		self.m["profondeur_emmanchure"]  =  YP_emmanchure-self.m["hauteur_emmanchure"]
		print("Profondeur d'emmanchure: %4.0f" % (self.m["profondeur_emmanchure"]))
		DSl1 = [xdev, YP_emmanchure]
					
		#~ points_emmanchure_dos = np.array([ShB1, BB1, CPSlB, SlB1])
		#~ dsb, sleeve_back_points = self.pistolet(points_emmanchure_dos, 3, tot=True)
		points_emmanchure_dos = np.array([ShB1, BB1, CPSlB, SlB1])
		dsb, sleeve_back_points = self.pistolet(points_emmanchure_dos, 2, tot=True)
		print("Longueur emmanchure dos: %4.0f" % (dsb))
		self.m["longueur_emmanchure_dos"] = dsb
		
		points_emmanchure_devant = np.array([ShF1, BF1, CPSlF, SlF1])
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
		#Create Vertices 
		#for polygon representation
		#########################################	
		
		
		self.Bodice_Back_vertices  =  [WB, CB ] + collar_back_points +  sleeve_back_points + [SlB1, WB1]		
		self.Bodice_Front_vertices  =  [WF,  CF ] + collar_front_points +  sleeve_front_points + [SlF1, WF1]
		
		self.curves_dic = {'Back_Collar': collar_back_points, 'Back_Sleeve': sleeve_back_points, 'Front_Collar': collar_front_points, 'Front_Sleeve': sleeve_front_points}
		
	
	def add_bust_dart(self):
		""" Add darts to dartless Bodice
		"""
		bfd  = self.Bodice_points_dic
		
		if self.style == 'Gilewska':
			# Apex of dart
			OP = np.array([bfd['WF'][0] - self.m["ecart_poitrine"]/2, bfd['CF1'][1] - self.m["hauteur_poitrine"]])
			
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
			K2 = np.dot(A, K) + OP
			S = bfd['ShF1']- OP
			ShF2 = np.dot(A, S) + OP

			# Extension of the bust 
			""" Here, in comments and as a reminder, 
			I've place  the strict method of Gilewska...
			
			a = self.segment_angle(MShF, OP)*180/np.pi
			B = self.intersec_manches(bfd['BF'], bfd['BF1'], MShF, a)
			r2 = self.distance(OP, B)
			dx=2*r2*np.sin(theta/2)
			F2 = bfd['BF1'] - np.array([dx, 0])
			
			... But I prefer the two lines below because 
			logically point F should be rotated as well 
			 and not just translated."""			 
			
			F1 = bfd['BF1'] - OP
			F2 = np.dot(A, F1) + OP # here the point is rotated around OP with the exact angle of the dart. :=)

			#redraw the arm curve
			dsf, new_sleeve_front_points = self.pistolet(np.array([ShF2, F2, bfd['CPSlF'], bfd['SlF1']]), 2, tot = True)
			self.curves_dic['Front_Sleeve'] = new_sleeve_front_points # I change the armhole curve to the new one.
			self.m["longueur_emmanchure_devant"] = dsf
			print("longueur emmanchure devant avec pince de buste %4.0f" % (dsf))
			
			key=['MShF', 'K2', 'ShF2', 'F2', 'OP']
			val=[MShF, K2, ShF2, F2, OP]
					
			for i in range(len(key)): # add new points to the dictionnary
				self.Bodice_points_dic[key[i]] = val[i]
			
			#redraw the front bodice with the added dart
			self.Bodice_Front_vertices = [bfd['WF'],  bfd['CF'] ] + self.curves_dic['Front_Collar'] +  [MShF, OP, K2, ShF2] + new_sleeve_front_points + [bfd['SlF1'], bfd['WF1']]
			
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
			CBD=np.array(sbp['WB']) + [1, 0]
			
			# Back Dart BD
			BDc = np.array(sbp['WB'])+ [self.m["carrure_dos"]/4, 0]
			BD0 = BDc - [pinces/2, 0]
			BD1 = BDc + [pinces/2, 0]
			BDs = BDc + [0, sbp['SlB'][1]]
			
			#Side Back Dart SBD
			SBD = np.array(sbp['WB1']) - [pinces, 0]

			
			key = ['CBD', 'BD0', 'BD1', 'BDs', 'SBD']
			val = [CBD, BD0, BD1, BDs, SBD]
			for k, v in zip(key, val):
				self.Bodice_points_dic[k]=v
				
			self.Bodice_Back_vertices  =  [CBD, sbp['SlB'], sbp['CB'] ] + self.curves_dic['Back_Collar'] +  self.curves_dic['Back_Sleeve'] + [sbp['SlB1'], SBD, BD1, BDs, BD0]		
			#~ print(self.Bodice_Back_vertices)
			
			# The Front
			# Apex of dart
			if 'OP' not in sbp.keys():
				OP = np.array([sbp['WF'][0] - self.m["ecart_poitrine"]/2, sbp['CF1'][1] - self.m["hauteur_poitrine"]])
				bust_dart = False
			else:
				OP = sbp['OP']
				bust_dart = True
			
			#Front dart FD
			WMF = np.array([OP[0], 0]) 
			FD0 = WMF - [pinces/2, 0]
			FD1 = WMF + [pinces/2, 0]
			
			#Side Front Dart SFD
			SFD = np.array(sbp['WF1']) + [pinces, 0]
			
			
			key = ['FD0', 'FD1', 'SFD', 'OP']
			val= [FD0, FD1, SFD, OP]
			for k, v in zip(key, val):
				self.Bodice_points_dic[k]=v
			
			if bust_dart:
				self.Bodice_Front_vertices = [sbp['WF'],  sbp['CF'] ] + self.curves_dic['Front_Collar'] +  [sbp['MShF'], sbp['OP'], sbp['K2'], sbp['ShF2']] + self.curves_dic['Front_Sleeve'] + [sbp['SlF1'], SFD, FD0, OP, FD1]
			else:
				self.Bodice_Front_vertices = [sbp['WF'],  sbp['CF'] ] + self.curves_dic['Front_Collar'] + self.curves_dic['Front_Sleeve'] + [sbp['SlF1'], SFD.tolist(), FD0.tolist(), OP.tolist(), FD1.tolist()]
			
			
		else:
			pass
		
	def Gilewska_basic_sleeve_w(self):
		"""Basic sleeve for Women
		using Gilewska technique
		"""
		
		#########################################
		# squeleton
		#########################################
				
		A = [0,  self.m["longueur_manche"]]

		C = [0,  self.m["longueur_manche"] - 4*self.m["profondeur_emmanchure"]/5]
				
		E = [3*self.m["longueur_emmanchure_devant"]/4,  C[1]]
		D = [-3*self.m["longueur_emmanchure_dos"]/4,  C[1]]
		

		F  =  [0,  0.5*(A[1] + C[1])]
		J  =  self.intersec_manches(A, D, F, -45)
		J1  =  self.intersec_manches(A, E, F, 45)

		
		CDos1  =  [J[0]+2*np.cos(3*np.pi/4), J[1]+2*np.sin(3*np.pi/4)]
		CDevant1  =  [J1[0]+1.8*np.cos(np.pi/4), J1[1]+1.8*np.sin(np.pi/4)]
		
		G  =  self.intersec_manches(A, D, C, -45)
		G1  =  self.intersec_manches(A, E, C, 45)
		
		CDos2  =  [G[0]+1.5*np.cos(3*np.pi/4), G[1]+1.5*np.sin(3*np.pi/4)]
		CDevant2  =  [G1[0]+1*np.cos(np.pi/4), G1[1]+1*np.sin(np.pi/4)]
				
		K = self.middle(D, G)
		KK = self.middle(D, K)
		K1 = self.middle(E, G1)
		KK1 = self.middle(E, K1)
		
		CDos4 = [KK[0]+0.5*np.cos(self.segment_angle(D, K)-np.pi/2), KK[1]+0.5*np.sin(self.segment_angle(D, K)-np.pi/2)]
		CDevant4 = [KK1[0]+0.8*np.cos(self.segment_angle(E, K1)-np.pi/2), KK1[1]+0.8*np.sin(self.segment_angle(E, K1)-np.pi/2)]
		
		Controle_dos  =  np.array([A, CDos1,  CDos2,  K,  CDos4, D])
		Controle_devant  =  np.array([E, CDevant4, K1,  CDevant2, CDevant1, A])
		
		
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

		
		W = [0, self.m["longueur_manche"] - self.m["hauteur_coude"]]
		
		#########################################
		# bas de manche
		#########################################
		S = [self.m["tour_poignet"]/2, 0]
		V = [-self.m["tour_poignet"]/2, 0]
		
		W0 = self.intersec_manches(S, E, W, 0)
		W1 = self.intersec_manches(V, D, W, 0)
		
		self.Sleeve_points_dic = {'A':A, 'C':C, 'D':D, 'E':E, 'F':F, 'J':J, 'J1':J1, \
		 'K':K, 'K1':K1, 'G':G, 'G1':G1, 'V':V, 'S':S, 'W':W, 'W0':W0, 'W1':W1, \
		 'CDos1':CDos1, 'CDos2':CDos2, 'CDos4':CDos4, 'CDevant1':CDevant1, \
		 'CDevant2':CDevant2, 'CDevant4':CDevant4} 
		self.Sleeve_vertices = [S, W0, E] + front_curve_points + [A] + back_curve_points + [D, W1, V]

class shirt(Basic_Bodice):
	

	def __init__(self, collar_ease = 1, sleeve_lowering = 4, side_ease=4):
		pass
		
	def shirt_bodice(self):
		pass
		
	def shirt_sleeve_m(self,ease=3,Slit_length=12, fold_number=3, fold_length=1):
		pass

		#~ if fold_number > 0:
			#~ S = np.array([self.m["tour_poignet"]/2 + ease/2 + 0.5, 0])
			#~ V = np.array([-(self.m["tour_poignet"]/2 + ease/2 + fold_number*fold_length - 0.5), 0])

		# slit 
		# Stb Slit bottom
		#~ Stb = self.middle(np.array([0,0]),V)
		#~ #Stt Slit top
		#~ Stt = Stb + [0,Slit_length]


		#~ if fold_number >= 1:
			#~ f1 = np.array([0,0])+[0.5,0]
			#~ self.Sleeve_points_dic['f1']=f1
		#~ if fold_number >= 2:
			#~ f2 = self.middle(np.array([0,0]),Stb)
			#~ self.Sleeve_points_dic['f2']=f2
		#~ if fold_number >= 3:
			#~ f3 = self.middle(V,Stb)
			#~ self.Sleeve_points_dic['f3']=f3

		#~ self.Sleeve_segments = [[Stt,Stb],[f1,f1-[1,0]],[f2,f2-[1,0]],[f3,f3+[1,0]]]
			
		# draw method
		#~ for seg in self.Sleeve_segments:
		#~ self.segment(seg[0],seg[1],ax,{'color':'0.1','linestyle':'solid'})
	
	
class Cuffs(Pattern):
	"""
	Class to calculate cuff pattern
	
	styles available: Simple, French
	"""
	
	def __init__(self, pname = "sophie", gender = 'w', style = 'Donnanno', age = 12, cuff_style = 'Simple',\
		overlap = 2, width = 5, ease = 3 ):
		
		Pattern.__init__(self,pname, gender)

		self.style = style		
		self.Cuff_style = cuff_style
		self.Cuffs_dic = {}
		self.Cuffs_vertices = []
		self.Cuffs_segments = {}
		
		self.calculate_cuffs(overlap, width, ease)
		
	def calculate_cuffs(self, overlap = 2, width = 5, ease = 3):
		
		if self.style == 'Gilewska':
			if self.gender == 'm':
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
			Cld = np.array([0,0])
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
			
			self.Cuffs_dic = {'Cld': Cld, 'Clu': Clu, 'Olu': Olu, 'Oru': Oru, 'Ord': Ord, 'Old': Old}
			self.Cuffs_vertices = [Cld, Clu, Oru, Ord, Cld]
			print(self.Cuffs_vertices)
			self.Cuffs_segments = {'Fold': [Clm, Olm], 'Overlap': [Olu, Old], 'Bru': [Bru, Bru - [0,1]],\
			'Brd': [Brd, Brd + [0,1]]}

		elif self.Cuff_style == 'French':
			
			Cld = np.array([0,0])
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
			
			self.Cuffs_dic = {'Cld': Cld, 'Clu': Clu, 'Olu': Olu, 'Oru': Oru, 'Ord': Ord, 'Old': Old, 'Crd': Crd, 'Cru': Cru }
			self.Cuffs_vertices = [Cld, Clu, Cru, Crd, Cld]
			self.Cuffs_segments = {'Cuff_Fold': [Clm, Crm], 'L_Overlap': [Olu, Old], 'R_Overlap': [Oru, Ord], 'Fabric_Fold': [Cld,Crd],\
			'Blu': [Blu, Blu - [0,1]], 'Bru': [Bru, Bru - [0,1]], 'Bld': [Bld, Bld + [0,1]], 'Brd': [Brd, Brd + [0,1]]}

	def draw_cuffs(self,save = False):
		
		fig, ax = self.draw_pattern([self.Cuffs_dic],[self.Cuffs_vertices])
		
		for key, val in self.Cuffs_segments.items():
			lbl_pos = self.middle(val[0],val[1])
			kwdic = {'color': 'blue', 'linestyle':'dashed', 'alpha':0.5}
			self.segment(val[0], val[1], ax, kwdic)
			angle = self.segment_angle(val[0],val[1])*180/np.pi
			ax.text(lbl_pos[0], lbl_pos[1], key, rotation = angle)
			
		if save:
				
			of = '../patterns/'+ 'cuff_' + self.style + '_' + self.Cuff_style + '_' + self.pname +'_FullSize.pdf'
				
			plt.savefig(of)
			
			
		return fig, ax
		
class Collars(Pattern):
	"""
	Class to calculate collar pattern
	
	Collars must be called or instanciated after shirt or bodice instances so that 
	the back and front collar lengths are stored on a json measurement file.
	
	styles available : Officer, OnePiece
	 
	"""
	
	def __init__(self, pname="sophie", gender='w', style='Gilewska', collar_style = 'Officer', overlap=0, collar_height=3):

		Pattern.__init__(self,pname, gender)

		self.style = style		
		self.Collar_style = collar_style
		self.Collar_dic = {}
		self.Collar_vertices = []
		self.Collar_segments = {}
		
		self.calculate_collar(overlap, collar_height)
		
	def calculate_collar(self, overlap, collar_height):
		
		if self.style == 'Gilewska':
			print('Style Gilewska')
			if self.gender == 'm':
				print("Men's collar")
				self.calculate_collar_gilewska_m(overlap, collar_height)
				
	def calculate_collar_gilewska_m(self, overlap=0, collar_height=3):
		"""
		C: collar angle points
		l,r,m: left, right, middle
		u,d: up, down 
		"""
		
		if self.Collar_style == 'Officer':
			print('Officer Collar')
			Cld = np.array([0,0.5])
			C1 = Cld + [2,0]
			Cmd = Cld + [self.m['longueur_col_dos']+0.5,-0.5]
			C2 = Cmd - [1,0]
			Crd = Cmd + [self.m['longueur_col_devant']+0.5,4]
			dcf = self.distance(Cmd, Crd)
			a = self.segment_angle(Cmd, Crd)
	
			C3 = Cmd + 0.5*dcf*np.array([np.cos(a-2*np.pi/180),np.sin(a-2*np.pi/180)])
	
			Clu = Cld + [0, collar_height]
			C4 = Clu + [2,0]
			
			Cmu = Cmd + [0, collar_height]
			C5 = Cmu - [1,0]
			
	
			Cru = Crd + [collar_height*np.cos(a+np.pi/2),collar_height*np.sin(a+np.pi/2)]
			if collar_height > 5:
				C6 = Cru - [np.sqrt(2),np.sqrt(2)] # 2 cm of offset from Cru.
			elif collar_height > 3 and collar_height <= 5:
				C6 = Cru - [np.sqrt(1.5),np.sqrt(1.5)] # sqrt(3) cm of offset from Cru.				
			else:
				C6 = Cru - [np.sqrt(0.5),np.sqrt(0.5)] # 1.5 cm of offset from Cru.
				
			C7 = Cmu + [0.6*dcf*np.cos(a),0.6*dcf*np.sin(a)]
			
			C8 = Cmu + 0.5*self.distance(Cmu,C6)*np.array([np.cos(a-2*np.pi/180),np.sin(a-2*np.pi/180)])
			
			d, front_collar_curve = self.pistolet(np.array([Crd, C6, C7]), 2, tot=True)
			d, back_curve_d = self.pistolet(np.array([Cld, C1, C2, Cmd]), 3, tot=True)
			d, back_curve_u = self.pistolet(np.array([Cmu, C5, C4, Clu]), 3, tot=True)
			d, front_curve_d = self.pistolet(np.array([Cmd, C3, Crd]), 2, tot=True)
			d, front_curve_u = self.pistolet(np.array([C7, C8, Cmu]), 2, tot=True)
			
			self.Collar_dic = {'Cld': Cld, 'Cmd': Cmd, 'Crd': Crd, 'Cmu': Cmu, 'Clu': Clu, 'Cru': Cru, 'C7': C7, 'C8': C8, 'C3': C3, 'C6': C6}
			self.Collar_vertices = back_curve_d + front_curve_d + front_collar_curve + front_curve_u  + back_curve_u
			
			self.Collar_segments = {'Middle Back': [np.array([0,0]),np.array([0,10])],\
				'Shoulder': [Cmd,Cmd+[0,10]], 'Middle Front': [Crd-[0,4],Crd+[0,6]], 'Overlap Line': [Crd,Cru]}

			
		if self.Collar_style == 'OnePiece':
			Cld = np.array([0,0.5])
			C1 = Cld + [2,0]
			Cmd = Cld + [self.m['longueur_col_dos']+0.5,-0.5]
			C2 = Cmd - [1,0]
			Crd = Cmd + [self.m['longueur_col_devant']+0.5 + overlap,3]
			dcf = self.distance(Cmd, Crd)
			a = self.segment_angle(Cmd, Crd)
			print('a = ', a)
	
			C3 = Cmd + 0.5*dcf*np.array([np.cos(a-2*np.pi/180),np.sin(a-2*np.pi/180)])
	
			Clu = Cld + [0, collar_height]
			C4 = Clu + [2,0]
			
			Cmu = Cmd + [0, collar_height]
			C5 = Cmu - [1,0]
			
	
			Cru = Crd + [collar_height*np.cos(a+np.pi/2),collar_height*np.sin(a+np.pi/2)]
			C6 = Cru - [np.sqrt(0.3),np.sqrt(0.3)] # 1.5 cm of offset from Cru.
			
			A =	np.array([self.m['longueur_col_dos']+self.m['longueur_col_devant']+1,0])			
			C7 = A+[0, 3+ collar_height]
			C7 = C7 - [0, np.tan(a)*self.distance(C7,Cru)]
			b = self.segment_angle(Cru,Crd)
			print('b =',b)
			
			C7bis = self.intersec_manches(Cmd,Crd,C7,b*180/np.pi)
			
			C8 = Cmu + 0.5*self.distance(Cmu,C6)*np.array([np.cos(a-2*np.pi/180),np.sin(a-2*np.pi/180)])
			
			d, front_collar_curve = self.pistolet(np.array([Crd, C6, C7]), 2, tot=True)
			d, back_curve_d = self.pistolet(np.array([Cld, C1, C2, Cmd]), 3, tot=True)
			d, back_curve_u = self.pistolet(np.array([Cmu, C5, C4, Clu]), 3, tot=True)
			d, front_curve_d = self.pistolet(np.array([Cmd, C3, Crd]), 2, tot=True)
			d, front_curve_u = self.pistolet(np.array([C7, C8, Cmu]), 2, tot=True)
			
			upper_curve = []
			for p in front_curve_u[5:]:
				p = p + np.array([0,5])
				upper_curve.append(p)
			for p in back_curve_u:
				p = p + np.array([0,5])
				upper_curve.append(p)
				
			
			self.Collar_dic = {'Cld': Cld, 'Cmd': Cmd, 'Crd': Crd, 'Cmu': Cmu, 'Clu': Clu, 'Cru': Cru, 'C7': C7, 'C8': C8, 'C3': C3, 'C6': C6}
			self.Collar_vertices = back_curve_d + front_curve_d + front_collar_curve + upper_curve
			
			self.Collar_segments = {'Middle Back': [np.array([0,0]),np.array([0,10])],\
				'Shoulder': [Cmd,Cmd+[0,10]], 'Middle Front': [A,A+[0,10]],\
				'Overlap Line': [C7,C7bis]}

				
						
			
	def draw_collar(self,save = False):
		
		fig, ax = self.draw_pattern([self.Collar_dic],[self.Collar_vertices])
		
		for key, val in self.Collar_segments.items():
			lbl_pos = self.middle(val[0],val[1])
			#~ lbl_pos = val[1]
			kwdic = {'color': 'blue', 'linestyle':'dashed', 'alpha':0.5}
			self.segment(val[0], val[1], ax, kwdic)
			a = self.segment_angle(val[0],val[1])
			angle = a*180/np.pi
			ax.text(lbl_pos[0]+0.2*np.cos(a+np.pi/2), lbl_pos[1]+0.2*np.sin(a+np.pi/2), key, rotation = angle, ha='center')

		if save:
				
			of = '../patterns/'+ 'collar_' + self.style + '_' + self.Collar_style + '_' + self.pname +'_FullSize.pdf'
				
			plt.savefig(of)
			
		return fig, ax			
###############################################################
# Specific class templates (trousers, shirts etc...) 
# from different stylists Donnanno, Gilewska 
# all classes inherit from the two main parent classes
# Basic_templates and Pattern
###############################################################
		
class Pyjama(Basic_Trousers):
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
			
			AF = np.array(pbf['A']) + [0, 6]
			AB = np.array(pbb['A']) + [0, 6]
			
			
			V = np.array(self.middle(AF, AB))
			Z = V + [0, -V[1]]
			B1 = Z - [self.m["tour_cheville"] * 3/4 -2, 0]
			C1 = Z + [self.m["tour_cheville"] * 3/4 +2, 0]

			print('front leg:', self.distance(pbf['E1'], B1) )
			print('back leg:', self.distance(pbb['E2'], C1) )
			
			pants_points_dic={'B1':B1, 'E1':pbf['E1'], 'AF':AF, 'V':V, 'AB':AB, 'E2':pbb['E2'], 'C1':C1, 'Z':Z}
			
			pants_bloc_vertices = [B1, pbf['E1']] + self.fourche_avant + [AF, AB] + self.fourche_arriere + [C1, B1]
			
			
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
			ax.text(mfold[0], mfold[1]+0.1, 'Fold Line')

			d=np.abs(pbf['E1'][0]-pbb['E1'][0])
			ankle=self.distance(B1, C1)
			
			ax = self.print_info(ax, {"Pattern":"Pyjama", "Max width":d, "Height": V[1], "Ankle": ankle})
			
			
			fname='../patterns/' + self.style + '_Block_pants_' + self.pname + '.pdf'
			
			
			if save:
				plt.savefig(fname)
				
				if paper != 'FullSize':
					self.paper_cut(fig, ax, name='Block_pants', paper=paper)
				
