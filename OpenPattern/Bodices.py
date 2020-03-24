from OpenPattern.Pattern import *

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

	
	
