import sys
sys.path.append('./..')

import matplotlib.pyplot as plt
#~ from OpenPattern.Points import Point
from OpenPattern.Points import Point
import numpy as np
import matplotlib.pyplot as plt
import random

class movingPoint(Point):
	
	def __init__(self, pos = [0,0], point_type='soulard', comment=None, pname_ori=None):
		
		Point.__init__(self,pos, point_type, comment, pname_ori)
		

##################################################################

	def wants(self, mlist = [0,0], mtype='dxdy',  unit='deg'):
		"""self wants to move by  a certain amount
		
		Can either be done in cartesian coordinates 
			 mtype = 'dxdy' and mlist = [dx, dy]
		or polar coordinates
			 mtype = 'pol' and mlist = [theta, d], theta  !
		Args:
			mtype: str type of translations 
			mlist: 2x1 list of float or int
			deg: tells the unit of theta deg: degrees, rad: radians
			
		"""
		if mtype == 'dxdy':
			self.wx = self.x + mlist[0]
			self.wy = self.y + mlist[1]
			
			
		elif mtype == 'pol':
			theta = mlist[0]			
			d = mlist[1]
			
			if unit == 'rad':
				self.wx = self.x +  np.cos(theta)*d
				self.wy = self.y + np.sin(theta)*d
				
			elif unit == 'deg':
				self.wx = self.x + np.cos(theta*np.pi/180)*d
				self.wy = self.y + np.sin(theta*np.pi/180)*d

		else:
			print("wants: movement type must be dxdy or pol")
			change=False

	def canmove(self):
		
		self.x = self.wx
		self.y = self.wy
		
		#track change
		if self.track_changes:
			self.track.append((self.x,self.y))
	
		


fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

lp=[]
ipos=[[0,0]]
for i in range(500):
	pos = [np.random.randint(0,100), np.random.randint(0,100)]
	while pos in ipos:
		print("position déjà prise")
		pos = [np.random.randint(0,100), np.random.randint(0,100)]
	
	ipos.append(pos)
	p=movingPoint(pos, pname_ori = i) 
	
	lp.append( p )
	p.plot(ax1)


blocage_count = []
c=0
for i in range(1000):

	wish_list=[]
	random.shuffle(lp)
	for p in lp:
		p.wants([np.random.randint(0,3)-1, np.random.randint(0,3)-1])
		if [p.wx,p.wy] not in wish_list:
			wish_list.append([p.wx,p.wy])
			p.canmove()
		else:
			c+=1
	blocage_count.append(c)
		
for p in lp:
	x,y = p.get_track()
	try:
		ax2.plot(x,y,'--')
	except:
		print(x,y)

f2 = plt.figure()
plt.plot(blocage_count, '-')

plt.show()
