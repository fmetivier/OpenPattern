# -*- coding: utf-8 -*- 
# librairies

import matplotlib.pyplot as plt
import numpy as np
import json

from scipy.interpolate import splprep,  splev
from matplotlib.patches import Polygon, PathPatch
from matplotlib.path import Path
from matplotlib.backends.backend_pdf import PdfPages
from  copy import copy, deepcopy

class Point(object):
	"""Generic  point class
	
	2D implementation for now
	
	Attributes:
		x,y : floats and pos [x,y] for position
		point_type : str  generic type of point for seaches
		comment : str comments on the point
		pname_ori : str original point name in cas of pattern points. Not really used for now.
	
	"""

	def __init__(self, pos = [0,0], point_type='Pattern', comment=None, pname_ori=None):
		"""Initialize
		
		Args:
			# one mandatory arg
			pos : its position
		
			#
		"""
				
		# coordinates
		self.x = pos[0]
		self.y = pos[1]
		self.pos = [self.x, self.y]
		
		self.point_type = point_type
		
		self.track=[(pos[0],pos[1])] # recods all changes made si they can be cancelled on demand

		self.track_changes=True # by default record changes
		
		if comment:
			self.comment = comment
		else:
			self.comment=""
			
		
		if pname_ori:
			self.pname_ori=pname_ori
		else:
			self.pname_ori=""
			
	
	def copy(self):
		"""Deepcopy point to a newly named one
		"""
		return deepcopy( self )
		
		 
	##################################################################
	# Define + += - -= and *
	##################################################################

	
	def __add__(self,*args):
		"""
		A = self + Y
		A = self + array ou list
		"""
		
		a = args[0]
		if isinstance(a, Point):
			P = Point( [ self.x + a.x, self.y + a.y ]  )
			return P
			
		elif isinstance(a, np.ndarray) or isinstance(a, list)  or isinstance(a, tuple):
			P = Point( [ self.x + a[0], self.y + a[1]]  ) 
			return P
		
	##################################################################
	
	def __iadd__(self,*args):
		"""
		self += Y
		self += array ou list
		"""
		
		a = args[0]
		if isinstance(a, Point):
			self.x += a.x
			self.y += a.y
			
		elif isinstance(a, np.ndarray) or isinstance(a, list) or isinstance(a, tuple):
			self.x += a[0]
			self.y += a[1] 
		
		if self.track_changes:
			self.track.append((self.x,self.y))
		return self
				
	##################################################################

	def __sub__(self,*args):
		"""
		A = self - Y
		A = self - array ou list
		"""
		
		a = args[0]
		if isinstance(a, Point):
			P = Point( [ self.x - a.x, self.y - a.y ]  )
			return P
			
		elif isinstance(a, np.ndarray) or isinstance(a, list) or isinstance(a, tuple):
			P = Point( [ self.x - a[0], self.y - a[1]]  ) 
			return P
	
	##################################################################

	def __isub__(self,*args):
		"""
		self -= Y
		self -= array ou list
		"""
		
		a = args[0]
		if isinstance(a, Point):
			self.x -= a.x
			self.y -= a.y
			
		elif isinstance(a, np.ndarray) or isinstance(a, list) or isinstance(a, tuple):
			self.x -= a[0]
			self.y -= a[1] 
		
		if self.track_changes:
			self.track.append((self.x,self.y))
		return self
		
	##################################################################
	
	def __mul__(self, *args):
		"""Scalar product a P
		
			Args:
				An int a => a*x, a*y 
		"""
		if len(args) == 1:
			a=args[0]
			if (isinstance(a, int) or isinstance(a,float)):
				nx = a * self.x
				ny = a * self.y
				P =  Point( [nx,ny] )
				return P
				
			else:
				print("*: bad type nothing done")
		else:
			print("*: arg format error nothing done")
			
			
	##################################################################
	# Arithmetics and calculus
	##################################################################
	
		
	def add(self,*args):
		""" Addition
		
		Args: two possible types
			a point, an array , a list => add(p)
			two points => add(x,y)
		
		"""
		
		change=True
		if len(args) == 1:
			p=args[0]
			if isinstance(p,Point):
				#~ print("a point !")
				self.x += p.x
				self.y += p.y
				
			elif isinstance(p, np.ndarray) or isinstance(p, list) or isinstance(a, tuple):
				#~ print("A matrix or a list !")
				self.x += p[0]
				self.y += p[1]
								
			else:
				print("add: type unknown, nothing done")
				pass
						
		elif len(args)==2:
			x = args[0]
			y = args[1]
			if (isinstance(x, int) or isinstance(x,float)) and (isinstance(y, int) or isinstance(y, float)):
				#~ print("two numbers !")
				self.x += x
				self.y += y
		
		else:
			print("add: arg format error nothing done")
			change=False
		
		#track change
		if change and self.track_changes:
			self.track.append((self.x,self.y))

	##################################################################

	def sub(self,*args):
		""" Substraction
		
		Args: two possible types
			a point, an array , a list => add(p)
			two points => add(x,y)
		
		"""
		
		change=True
		if len(args) == 1:
			p=args[0]
			if isinstance(p,Point):
				#~ print("a point !")
				self.x -= p.x
				self.y -= p.y
				
			elif isinstance(p, np.ndarray) or isinstance(p, list) or isinstance(a, tuple):
				#~ print("A matrix or a list !")
				self.x -= p[0]
				self.y -= p[1]
								
			else:
				print("sub: type not understood, nothing done")
				pass
						
		elif len(args)==2:
			x = args[0]
			y = args[1]
			if (isinstance(x, int) or isinstance(x,float)) and (isinstance(y, int) or isinstance(y, float)):
				#~ print("two numbers !")
				self.x -= x
				self.y -= y
		
		else:
			print("sub: arg format error nothing done")
			change=False
		
		#track change
		if change and self.track_changes:
			self.track.append((self.x,self.y))

	##################################################################

	def scal(self, *args):
		"""Scalar product 
		   Different from * because it can also be a scalar product of vectors
		
			Args:
				An int a => a*x, a*y 
				A Point or a 2x1 array or list => Dot product in that case returns x1x2 + y1y2
		"""

		change=True
		if len(args) == 1:
			a=args[0]
			if (isinstance(a, int) or isinstance(a,float)):
				self.x *= a
				self.y *= a
			
			elif isinstance(a, Point):
				change=False
				return self.x*a.x + self.y*a.y
			
			elif isinstance(a, np.ndarray) or isinstance(a, list) or isinstance(a, tuple):
				change=False
				return self.x*a[0] + self.y*a[1]
		else:
			print("scal: arg format error nothing done")
			change=False
			
		#track change
		if change and self.track_changes:
			self.track.append((self.x,self.y))

	##################################################################

	def vec(self, *args):
		"""Vector product
		
			Args: 
				A point, an array or a list of two values
			
			Returns:
				The vector product as a number
		"""
		
		if len(args) == 1:
			p=args[0]
			if isinstance(p, Point):
				return self.x*p.y - self.y*p.x
				
			elif isinstance(a, np.ndarray) or isinstance(a, list) or isinstance(a, tuple):
				return self.x*p[1] - self.y*p[0]
			
			else:
				print("vec: Type unknown")
				pass
		else:
			print("vec: Arg format error")

	##################################################################
		
	def mat(self, *args):
		"""Matrix product 
		
			Args:
				A 2x2 matrix or list of ints of floats
		"""
		change=True
		if len(args) == 1:
			p=args[0]
			if isinstance(p, np.ndarray) or isinstance(p, list) or isinstance(a, tuple):
				if np.shape(p) == (2,2):
					x = p[0,0]*self.x + p[0,1]*self.y
					y = p[1,0]*self.x + p[1,1]*self.y
					self.x = x
					self.y = y
					
			else:
				print("Type non understood, nothing done")
				change=False
		
		else:
			print("mat: arg format error")
			change=False
			
		#track change
		if change and self.track_changes:
			self.track.append((self.x,self.y))

	##################################################################

	def mat_out(self, *args):
		"""Matrix product of self with A -> new point
		
			Args:
				A 2x2 matrix or list of ints of floats
		"""
		if len(args) == 1:
			p=args[0]
			if isinstance(p, np.ndarray) or isinstance(p, list) or isinstance(a, tuple):
				if np.shape(p) == (2,2):
					x = p[0,0]*self.x + p[0,1]*self.y
					y = p[1,0]*self.x + p[1,1]*self.y
					return Point([x,y])
					
			else:
				print("Type non understood, nothing done")
				change=False
		
		else:
			print("mat: arg format error")
			change=False
			
			
	##################################################################
	# Geometry
	##################################################################
			

	def moveto(self, *args):
		"""move point to a certain location
		
		Args: can be
			Point => move to the location of the Point given
			Position 2x1 list or array
			position x,y
		""" 
		
		change=True
		if len(args) == 1:
			p=args[0]
			if isinstance(p,Point):
				#~ print("a point !")
				self.x = p.x
				self.y = p.y
				
			elif isinstance(p, np.ndarray) or isinstance(p, list) or isinstance(a, tuple):
				#~ print("A matrix or a list !")
				self.x = p[0]
				self.y = p[1]
								
			else:
				print("type no good, nothing done chap")
				pass
						
		elif len(args)==2:
			x = args[0]
			y = args[1]
			if (isinstance(x, int) or isinstance(x,float)) and (isinstance(y, int) or isinstance(y, float)):
				#~ print("two numbers !")
				self.x = x
				self.y = y
		
		else:
			print("moveto: Argument format error nothing done")
			change=False
		
		#track change
		if change and self.track_changes:
			self.track.append((self.x,self.y))
			
	##################################################################

	def move(self, mlist = [0,0], mtype='dxdy', unit='deg'):
		"""Move point by  a certain amount
		
		Can either be done in cartesian coordinates 
			 mtype = 'dxdy' and mlist = [dx, dy]
		or polar coordinates
			 mtype = 'pol' and mlist = [theta, d], theta  !
		Args:
			mtype: str type of translations 
			mlist: 2x1 list of float or int
			deg: tells the unit of theta deg: degrees, rad: radians
			
		"""
		change=True
		if mtype == 'dxdy':
			self.x += mlist[0]
			self.y += mlist[1]
			
			
		elif mtype == 'pol':
			theta = mlist[0]			
			d = mlist[1]
			
			if unit == 'rad':
				self.x += np.cos(theta)*d
				self.y += np.sin(theta)*d
				
			elif unit == 'deg':
				self.x += np.cos(theta*np.pi/180)*d
				self.y += np.sin(theta*np.pi/180)*d

		else:
			print("move: movement type must be dxdy or pol")
			change=False
		
		#track change
		if change and self.track_changes:
			self.track.append((self.x,self.y))
			
	##################################################################

	def rotate(self, rot_center=[0,0], theta = 0, unit = 'deg' ):
		"""rotate a point from theta around rot_center
		
			Args: 
				rot_center: can a Point, a 2x1 matrix or list
				theta: angle of rotation 
				unit: unit of angle of rotation  deg for degrees and rad for radians 
				
		"""
		
		#change coordinate reference
		self.track_changes=False
		self.sub(rot_center)
		
		# rotation	
		if unit == 'deg':
			theta *= np.pi/180
		
		M = np.array([[np.cos(theta), -np.sin(theta)],[np.sin(theta), np.cos(theta)]])
		self.mat(M)
		
		#back to original reference
		self.track_changes=True
		self.add(rot_center)

			
	##################################################################

	def angle_to(self, B):
		"""Returns slope of segment to B
		
		Args:
			B: Point
		
		Returns:
			angle in radians
		"""

		if isinstance(B, Point):
			if B.x-self.x == 0:
				return(np.pi/2)
			else:
				return np.arctan((B.y-self.y)/(B.x-self.x))		
		else:
			print("segment_angle: arg must be a Point")

	##################################################################

	def middle(self, B):
		"""
		returns the middle point of [self B]
		
		Args:
			B: point 
		
		
		Returns:
			Point([x,y])
				"""
		if isinstance(B, Point):
			return Point([0.5*(self.x + B.x), 0.5*(self.y + B.y)])
		else:
			print("Middle: arg must be a Point. Nothing done")

	##################################################################

	def distance_to(self,B):
		"""
		returns distance to B
		
		Args:
			B: point		
		
		Returns:
			distance as a float
		"""
		
		if  isinstance(B, Point):
			return np.sqrt((self.x-B.x)**2+(self.y-B.y)**2)
	
	##################################################################
	# Record changes 
	##################################################################
		
	def get_track(self, for_plot = True):
		"""Returns the track 
		
			Args:
				for_plot: if True returns the transposed track (for plot)
		"""
		if for_plot:
			return np.array(self.track).transpose()
		else:
			return self.track
			
	##################################################################

	def reset(self):
		"""Go back to original
		"""
		
		self.x, self.y = self.track[0]

		#track change
		if self.track_changes:
			self.track.append((self.x,self.y))
	
	##################################################################
	# Plotting
	##################################################################
				
	def plot(self, ax, name=None, kwargs = {'marker':'o', 'color':'blue'} ):
		"""
		plot point
		"""
		offset = 0.2
		ax.plot(self.x, self.y, **kwargs)
		if name:
			ax.text(self.x + offset,self.y,name)

	##################################################################

	def segment_to(self, B, ax, kwargs={'color':'blue'}):
		"""
		plots [self B] segment on ax

		Args:
			B: Point([x,y])
			ax: axis on which to plot
			kwargs: dictionnary of drawing porperties			
		"""
		
		if  isinstance(B, Point):
			ax.plot([self.x, B.x], [self.y, B.y],  **kwargs)	
		else:
			plot("segment_to: args error") 

		
	
if __name__ == '__main__':
	pass
	
