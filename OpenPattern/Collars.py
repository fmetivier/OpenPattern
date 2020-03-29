import sys
sys.path.append('./..')

from OpenPattern.Pattern import *
from OpenPattern.Points import *

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
		self.Collar_dic = []
		self.Collar_vertices = []
		self.Collar_segments = {}
		self.Collar_polylines = []
		
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
			self.pied_de_col_gilewska_m(overlap, collar_height, front_height=4) 			
			
		if self.Collar_style == 'OnePiece':
			print('OnePiece Collar')
			curve_dic = self.pied_de_col_gilewska_m(overlap, collar_height)
			
			upper_curve = []
			for p in curve_dic['fcu'][5:]:
				upper_curve.append(p + np.array([0,5]))
			for p in curve_dic['bcu']:
				upper_curve.append(p + np.array([0,5]))
				
			self.Collar_vertices.append( curve_dic['bcd'] + curve_dic['fcd'] + curve_dic['fcc'] + upper_curve )
			self.Collar_polylines.append(  curve_dic['fcu'] + curve_dic['bcu'] )


				
	def pied_de_col_gilewska_m(self, overlap=0, collar_height=3, front_height=2):					
			
			Cld = Point([0,0.5])
			C1 = Cld + [2,0]
			Cmd = Cld + [self.m['longueur_col_dos']+0.5,-0.5]
			C2 = Cmd - [1,0]
			Crd = Cmd + [self.m['longueur_col_devant']+0.5 + overlap, front_height]
			
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

			
			A =	Point([self.m['longueur_col_dos']+self.m['longueur_col_devant']+1,0])		
			if overlap == 0:
				C7 = Cmu + [0.6*dcf*np.cos(a),0.6*dcf*np.sin(a)]
			else:
				# find the (C7) points at the overlap
				ad = self.segment_angle(Cmd,Crd)
				C7d = Point( [A.x, np.tan(ad)*(A.x-Cmd.x) + Cmd.y] )		
				
				C7 = C7d + [np.cos(ad+np.pi/2)*collar_height, np.sin(ad+np.pi/2)*collar_height]
				b = self.segment_angle(Cru,Crd)
				print('b =',b)
			
				C7bis = self.intersec_manches(Cmd,Crd,C7,b*180/np.pi)
			
			C8 = Cmu + 0.5*self.distance(Cmu,C6)*np.array([np.cos(a-2*np.pi/180),np.sin(a-2*np.pi/180)])
			
			d, front_collar_curve = self.pistolet(np.array([Crd, C6, C7]), 2, tot=True)
			d, back_curve_d = self.pistolet(np.array([Cld, C1, C2, Cmd]), 3, tot=True)
			d, back_curve_u = self.pistolet(np.array([Cmu, C5, C4, Clu]), 3, tot=True)
			d, front_curve_d = self.pistolet(np.array([Cmd, C3, Crd]), 2, tot=True)
			d, front_curve_u = self.pistolet(np.array([C7, C8, Cmu]), 2, tot=True)

			self.Collar_dic.append( {'Cld': Cld, 'Cmd': Cmd, 'Crd': Crd, 'Cmu': Cmu, 'Clu': Clu, 'Cru': Cru, 'C7': C7, 'C8': C8, 'C3': C3, 'C6': C6} )
			self.Collar_vertices.append( back_curve_d + front_curve_d + front_collar_curve+ front_curve_u + back_curve_u )
			
			self.Collar_segments = {'Middle Back': [Point([0,0]), Point([0,10])],\
				'Shoulder': [Cmd,Cmd+[0,10]], 'Middle Front': [A,A+[0,10]]}
				
			if overlap != 0:
				self.Collar_segments['Overlap Line'] = [C7,C7bis]
			
			cdic = {'fcc': front_collar_curve, 'bcd' : back_curve_d, 'bcu': back_curve_u, 'fcd': front_curve_d, 'fcu': front_curve_u}
			return cdic
			
	def draw_collar(self,save = False):
		
		fig, ax = self.draw_pattern(self.Collar_dic,self.Collar_vertices,self.Collar_polylines)
		
		for key, val in self.Collar_segments.items():
			lbl_pos = self.middle(val[0],val[1])
			#~ lbl_pos = val[1]
			kwdic = {'color': 'blue', 'linestyle':'dashed', 'alpha':0.5}
			self.segment(val[0], val[1], ax, kwdic)
			a = self.segment_angle(val[0],val[1])
			angle = a*180/np.pi
			#~ ax.text(lbl_pos.x+0.2*np.cos(a+np.pi/2), lbl_pos.y +0.2*np.sin(a+np.pi/2), key, rotation = angle, ha='center')
			ax.text(lbl_pos.x+0.2*np.cos(a+np.pi/2), val[1].y, key, rotation = angle, ha='center')
			
		if save:
				
			of = '../patterns/'+ 'collar_' + self.style + '_' + self.Collar_style + '_' + self.pname +'_FullSize.pdf'
				
			plt.savefig(of)
			
		return fig, ax			
