# -*- coding: utf-8 -*-
# librairies
import sys
sys.path.append('./..')

import matplotlib.pyplot as plt
import numpy as np
import json
import sqlite3

from scipy.interpolate import splprep,  splev
from matplotlib.patches import Polygon, PathPatch
from matplotlib.path import Path
from matplotlib.backends.backend_pdf import PdfPages

from OpenPattern.Points import Point

"""
TODO:  02/01/21

Measurements:
- translate measurement names to english n
- measurement input procedure

Drawing:
- Write drawing routines with lines and comments IN PROGRESS
- olivier suggests adding a scale !


Patterns:
- add darts IN PROGRESS
- Bodice D change names (not mandatory though)

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

	Notes:
	- Pattern methods originally  used arrays or lists of values for points as arguments for calculations.
	- Since the development of the Point class I've progressively turned them to use it. I no longer use arrays for new methods.

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
			self.m  =  self.get_measurements_sql(pname)
			self.pname = pname
		else:
			# in the end it should be able to store new measurements.
			pass # create measures

		self.gender=gender

		# initialize dics and vertices
		self.Pattern_Front_dic = {}
		self.Pattern_Back_dic = {}
		self.Pattern_Front_vertices = []
		self.Pattern_Back_vertices = []



	############################################################
	#				add points or curves to dics
	#				and get them back
	############################################################

	def add_point(name = 'A', coords = [0,0], dic = 'front'):
		"""
		adds a point to the corresponding dic

		Args:
			name: str,  point name
			coords: list of floats, x and y coordinates
			dic: 'front' or 'back' dics to store the point
		"""

		if dic == 'front':
			self.Pattern_Front_dic[name] = Point(pos = coords, pname_ori = name)
		if dic == 'back':
			self.Pattern_Back_dic[name] = Point(pos = coords, pname_ori = name)
		else:
			print("choose back fo front for the dictionnary that stores the points")

	def add_curve(name = 'front_curve', coords = [0,0], dic = 'front'):
		"""
		adds a curve to the corresponding dic

		Args:
			name: str,  curve name
			coords: list of floats, x and y coordinates
			dic: 'front' or 'back' dics to store the point
		"""
		if dic == 'front':
			self.Pattern_Front_dic[name] = coords
		if dic == 'back':
			self.Pattern_Back_dic[name] = coords
		else:
			print("choose back fo front for the dictionnary that stores the points")

	def get(pname='A', dic='front'):
		"""
		returns the point/curve pname from the corresponding dic

		Args:
			pname: str point/curve name
			dic: 'front' or back' dictionnary from which to extrac the point

		returns:
			type Point : the chosen point
			or type list: list of coordinates of a curve
		"""
		if dic == 'front':
			return self.Pattern_Front_dic[pname]
		if dic == 'back':
			return self.Pattern_Back_dic[pname]
		else:
			print("choose back fo front for the dictionnary that stores the points")
			return 1

	############################################################
	# get and store measurements
	############################################################


	def get_measurements_json(self, pname="sophie"):
		"""Load stored measurements.

		Measurements loaded are dictionnaries stored as json files in the measurements folder
		23/12/2020: This is the original version now i use sqlite
		Args:
			pname: name of json file as str

		Returns:
			dic: a dictionnary of size measurments
		"""

		with open("../measurements/" + pname + "_data.json", "r") as read_file:
			dic = json.load(read_file)

		return dic

	def get_measurements_sql(self, pname="sophie"):
		"""Load stored measurements.

		Measurements loaded are dictionnaries stored as json files in the measurements folder

		Args:
			pname: name of pattern measurement code string

		Returns:
			dic: a dictionnary of size measurments
		"""

		conn = sqlite3.connect('../OpenPattern/measurements.db')
		c = conn.cursor()

		dic = {}
		for row in c.execute("select * from measurements where wkey = ?", (pname,)):
			dic[row[1]] = row[2]

		conn.close()

		return dic

	def save_measurements_json(self, ofname=None):
		""" Save new measurements

		Save new measurements in ofname_data.json file in the mesures folder
		If no output format is given stores the data under the attribute self.pname
		20/12/2020 changed to sql
		Args:
			ofname: output json filename as str

		"""
		if ofname:
			with open("../measurements/" + ofname + "_data.json", "w") as write_file:
				json.dump(self.m, write_file)
		else:
			with open("../measurements/" + self.pname + "_data.json", "w") as write_file:
				json.dump(self.m, write_file)

	def save_measurements_sql(self, ofname=None):
		""" Save new measurements

		Save new measurements under ofname key in the mesurement database
		If no output format is given stores the data under the attribute self.pname
		! beware of the final path.

		Args:
			ofname: str output wkey for measurements.db database

		"""
		conn = sqlite3.connect('../OpenPattern/measurements.db')
		c = conn.cursor()

		if ofname:
			if ofname != self.pname:
				pass
			else:
				c.execute("delete from measurements where wkey = ?", (ofname,))
		else:
			ofname = self.pname
			c.execute("delete from measurements where wkey = ?", (ofname,))

		for key, val in self.m.items():
			c.execute("insert into measurements values (?,?,?)", (ofname,key,val))


		conn.commit()
		conn.close()
	############################################################
	#				Calculations
	############################################################

	def distance(self, A, B):
		"""
		returns distance [AB]

		Args:
			A,B: points given as Points or array([x,y])


		Returns:
			distance as a float
		"""

		if isinstance(A, Point) and isinstance(B, Point):
			return np.sqrt((A.x-B.x)**2+(A.y-B.y)**2)
		else:
			return np.sqrt((A[0]-B[0])**2+(A[1]-B[1])**2)

	############################################################

	def intersec_lines(self, A,B,C,D):
		"""
		finds the instersection between , lines AB and CD
		Args:
			A,B,C, D: points given as Points or  array([x,y])

		Returns:
			Point([x,y]) or	(x,y) tuple of coordinates
		"""
		if isinstance(A, Point) and isinstance(B, Point) and isinstance(C, Point):
			# coefficient de AB
			aD1  =  (B.y-A.y)/(B.x-A.x)
			bD1  =  A.y - aD1*A.x

			#coefficients de CD
			aD2 = (C.y-D.y)/(C.x-D.x)
			bD2 = C.y - aD2*C.x

			xi = (bD2-bD1)/(aD1-aD2)
			yi = aD1*xi + bD1

			return Point([xi,yi])
		else:
			aD1  =  (B[1]-A[1])/(B[0]-A[0])
			bD1  =  A[1] - aD1*A[0]

			#coefficients de CD
			aD2 = (C[1]-D[1])/(C[0]-D[0])
			bD2 = C[1] - aD2*C[0]

			xi = (aD1-aD2)/(bD2-bD1)
			yi = aD1*xi + bD1

			return (xi,yi)



	def intersec_manches(self, A, B, C, theta):
		""" Intersection calculation

		Finds the point of intersection G of the AB line with the line going through C
		and making an  angle theta with the horizontal axis.
		Especially useful for sleeve heads.
		Does not work if AB is vertical !!!

		Args:
			A,B,C: points given as Points or  array([x,y])
			theta: angle in degrees

		Returns:
			Point([x,y]) or	(x,y) tuple of coordinates
		"""

		if isinstance(A, Point) and isinstance(B, Point) and isinstance(C, Point):
			# coefficient de AB
			aD1  =  (B.y-A.y)/(B.x-A.x)
			bD1  =  A.y - aD1*A.x

			#coefficients de CG
			aD2 = np.tan(theta*np.pi/180)
			bD2 = C.y - aD2*C.x

			#intersection
			x = (bD2-bD1)/(aD1-aD2)
			y = aD1*x+bD1

			return Point([x, y])

		else:
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

	def middle(self, A, B):
		"""
		returns the middle point of [AB]

		Args:
			A,B: points given as array([x,y])


		Returns:
			x,y as an array
				"""
		if isinstance(A, Point) and isinstance(B, Point):
			return Point([0.5*(A.x+B.x), 0.5*(A.y+B.y)])
		else:
			return np.array([0.5*(A[0]+B[0]), 0.5*(A[1]+B[1])])

	############################################################

	def segment_angle(self, A, B):
		"""Returns slope of segment [AB]

		Args:
			A,B: points given as array([x,y])


		Returns:
			angle in radians
		"""

		if isinstance(A, Point) and isinstance(B, Point):
			if B.x-A.x == 0:
				return(np.pi/2)
			else:
				return np.arctan((B.y-A.y)/(B.x-A.x))
		else:
			if B[0]-A[0] == 0:
				return(np.pi/2)
			else:
				return np.arctan((B[1]-A[1])/(B[0]-A[0]))

	############################################################

	def segment_offset(self, A, B, alpha, d):
		"""translates segment AB by a vector of length d making an angle alpha  with AB

		Args:
			A,B: Points
			alpha : real angle in radians
			d: offset distance in m

		Returns:
			Ap, Bp the offset points
		"""

		if isinstance(A. Point) and isiisinstance(B, Point):
			a = self.segment_angle(A, B)
			beta = a + alpha

			Ap =  Point([A.x + np.cos(beta)*d, A.y+ np.sin(beta)*d])
			Bp =  Point([B.x + np.cos(beta)*d, B.y+ np.sin(beta)*d])

			return Ap, Bp
		else:
			print("Points needed for this method")
			return 1

	############################################################

	def curve_offset(self, plist, alpha, d):
		"""translates a curve by a vector of length d making an angle alpha  with the local tangent

		Args:
			plist: list of [x,y] points positions
			alpha : real angle in radians
			d: offset distance in m

		Returns:
			olist : list of [x,y] offset points positions
		"""

		olist = []
		N = len(plist)
		for i in range(N-1):
			a = self.segment_angle(plist[i], plist[i+1])
			beta = a + alpha
			x = plist[i][0] + np.cos(beta)*d
			y = plist[i][1] + np.sin(beta)*d
			olist.append([x,y])

		# use the last value of beta for the last point
		x = plist[N-1][0] + np.cos(beta)*d
		y = plist[N-1][1] + np.sin(beta)*d
		olist.append([x,y])

		return olist


	############################################################

	def pistolet(self, points, kval, ax=None, kwargs = {'color':'blue','linestyle':'solid'}, tot=False):
		"""French curve calculation

		calculates a spline of order kval from set of given points.
		if ax given draws the result on ax and returns length of Armhole
		if tot returns a list of 30 points to draw the spline curve.

		Args:
			points: array of tuples or list of points
			kval: int
			ax: matplotlib axis
			kwargs: dictionnary of drawing properties
			tot: boolean deciding whether the entire curve is returned

		Returns:
			Total distance if tot = False
			Total distance and list of interpolated points if tot = True
		"""
		if isinstance(points[0], Point): # test on the first point of the list
			xlist, ylist = [], []
			for p in points:
				xlist.append(p.x)
				ylist.append(p.y)
			tck, u  =  splprep([xlist, ylist], k = kval, s=0)

		else:
			tck, u  =  splprep([points.transpose()[0], points.transpose()[1]], k = kval, s=0)

		us  =  np.linspace(u.min(),  u.max(),  100)
		new_points  =  splev(us,  tck)
		if ax:
			ax.plot(new_points[0],  new_points[1],  **kwargs)

		dx = np.diff(new_points[0])
		dy = np.diff(new_points[1])

		if tot:
			point_vertices = []
			for i in range(len(new_points[0])):
				point_vertices.append([new_points[0][i], new_points[1][i]])
			return  np.sum(np.sqrt(dx**2+dy**2)), point_vertices

		else:
			return  np.sum(np.sqrt(dx**2+dy**2))

	############################################################

	def add_dart(self,center = Point(),A = Point() , B = Point(), opening = 0, draw_curves = False, order = 'lr', rotate_end = 'none'):
		"""adds a dart to a pattern
		if draw_curves = True: draws the curve when the dart is closed then rotates when opening the dart
		if rotate = none: rotation of the curves or segment decreases linearly to reach 0 at the end points.
		if rotate =  left or right or both: also rotates the end points. The angle of rotation remains constant in this case NOT IMPLEMENTED YET

		Args:
		    center: Point position of the dart edge and center of rotation
		    A, B: Points segment to cut
		    opening: float width of the dart

		returns:
		    dart1, dart2 : points of the dart.
		"""

		# angle of the segment to cut
		theta = self.segment_angle(A, B)+np.pi/2

		# point of intersection
		I = self.intersec_manches(A, B, center, theta*180/np.pi)

		if draw_curves == True:

		    control_points = [A, I, B]
		    db, curve_points = self.pistolet(control_points, 2, tot = True)

		    if rotate_end == 'none':
		        # find the place of I and separate the curve into two subcurves
		        list_1 = []
		        list_2 = []
		        dval = 1000
		        for p in curve_points:
		            d = self.distance(I, Point(p))
		            dd = d-dval
		            if d < dval and dd < 0:
		                list_1.append(Point(p))
		            elif d > dval and dd > 0:
		                list_2.append(Point(p))
		            dval = d

		        # rotate lists
		        rotated_curve_1 = []
		        N = len(list_1)

		        if order == 'lr':
		            theta_N = opening/(2*self.distance(center, I)*N)
		            theta = 0
		            dtheta = theta_N
		        elif order == 'rl':
		            theta_N = opening/(2*self.distance(center, I)*N)
		            theta = 0
		            dtheta = -theta_N

		        for p in list_1:
		            p.rotate(center,theta, unit='rad')
		            theta += dtheta
		            rotated_curve_1.append(p.pos())


		        rotated_curve_2 = []
		        N = len(list_2)

		        if order == 'rl':
		            theta_N = opening/(2*self.distance(center, I)*N)
		            theta = N*theta_N
		            dthetat = -theta_N
		        elif order == 'lr':
		            theta_N = opening/(2*self.distance(center, I)*N)
		            theta = -N*theta_N
		            dtheta = theta_N

		        for p in list_2:
		            p.rotate(center, theta, unit='rad')
		            theta += dtheta
		            rotated_curve_2.append(p.pos())

		        return rotated_curve_1, rotated_curve_2

		    elif rotate_end == 'left':
		        pass
		    elif rotate_end == 'right':
		        pass
		    elif rotate_end == 'both':
		        pass
		    else:
		        pass

		else:
		    theta = opening/(2*self.distance(center, I))
		    I1 = I.copy()
		    I1.rotate(center,theta, unit='rad')
		    I2 = I.copy()
		    I2.rotate(center,-theta, unit='rad')

		    return I1, I2

	############################################################
	#				Drawings
	############################################################


	def segment(self, A, B, ax, kwargs={'color':'blue'}):
		"""
		plots [AB] segment on ax

		Args:
			A,B: points given as array([x,y])
			ax: axis on which to plot
			kwargs: dictionnary of drawing porperties
		"""

		if isinstance(A, Point) and isinstance(B, Point):
			ax.plot([A.x, B.x], [A.y, B.y],  **kwargs)
		else:
			ax.plot([A[0], B[0]], [A[1], B[1]],  **kwargs)

	def draw_pattern(self, dic_list, vertices_list, polyline_list=[]):

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

		for polyline in polyline_list:
			for val in polyline:
				if int(val[0]) < xmin:
					xmin = int(val[0])
				if int(val[0]) > xmax:
					xmax = int(val[0])
				if int(val[1]) < ymin:
					ymin = int(val[1])
				if int(val[1]) > ymax:
					ymax = int(val[1])

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
				if isinstance(val, Point):
					if int(val.x) < xmin:
						xmin = int(val.x)
					if int(val.x) > xmax:
						xmax = int(val.x)
					if int(val.y) < ymin:
						ymin = int(val.y)
					if int(val.y) > ymax:
						ymax = int(val.y)
				else:
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
		ax = plt.axes([0, 0, 1, 1])
		ax.axis('square')

		####################################################
		#       plot pattern
		####################################################

		for dic in dic_list:
			for key, val in dic.items():
				if isinstance(val, Point):
					ax.plot(val.x, val.y, 'ro')
					ax.text(val.x + 0.2, val.y, key, ha = 'left')
				else:
					ax.plot(val[0], val[1], 'ro')
					ax.text(val[0] + 0.2, val[1], key, ha = 'left')


		for vertices in vertices_list:
			poly  =  Polygon(vertices,  facecolor = '0.9',  edgecolor = '0.5')
			ax.add_patch(poly)

		for polyline in polyline_list:
			path = Path(polyline, codes = None, closed=False)
			patch = PathPatch(path, linestyle='--', edgecolor='grey', facecolor='None')
			ax.add_patch(patch)

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
