#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append('./..')
import sqlite3
import numpy as np


from OpenPattern.Pattern import *
from OpenPattern.Points import *

class Basic_Skirt(Pattern):
    """
	Class to calculate and draw a basic Skirt pattern.
	Inherits from Pattern

	Attributes

		style: style used to draw the pattern as string (Gilewska, Donnanno, Chiappetta for now)

		# Attributes that control the dictionnaries used for size measurements
		age: ade of the kid in Chiapetta's patterns
		pname: measurements used corresponding to a json file

		# Variables obtained from the basic calculations for Skirts
		# dics used here:

		Skirt_points_dic
		curves_dic

		# lists of vertices:

		Skirt_Back_vertices
		Skirt_Front_vertices

	"""

    def __init__(self, pname="W6C", style='Chiappetta', gender = 'G', ease=8):
        """
		Initilizes parent class &  attributes
		launches the calculation of skirt

		Args:
			pname: size measurements
			style: style to be used for drafting
			age: used if for a child and style = Chiappetta.

		"""
        Pattern.__init__(self, pname, gender)

        self.style=style
        self.ease = ease


        self.dic_list=[]
        self.vertices_list=[]

        self.points_dic = {}
        self.Front_points_dic = {}
        self.Back_points_dic = {}

        self.Front_vertices = []
        self.Back_vertices = []


        # calculate Basic Skirt and sleeve
        if self.style == 'Donnanno':
            print("style Donnanno selected")
            pass

        elif self.style == 'Gilewska':
            print("style Gilewska selected")
            self.Gilewska_basic_skirt()

        elif self.style == 'Chiappetta':
            print("style Chiappetta selected")
            self.chiappetta_basic_Skirt()

    def add_dart(self,center = Point(),A = Point() , B = Point(), opening = 0, draw_curves = False, order = 'lr', rotate_end = 'none'):
        """adds a dart to a pattern

        if draw_curves=True draws the curve when the dart is closed then rotates when opening the dart
        if rotate = none rotation of the curves or segment decreases linearly to reach 0 at the end points.
        if rotate =  left or right or both also rotates the end points. The angle of rotation remains constant in this case

        Args:
            center: Point position of the dart summit and center of rotation
            A, B: Points segment to cut
            opening: float width of the dart

        returns:
            I1, I2 : depending on Args can be
                        1) points left and right of the dart center of rotation.
                        2) left and right curves of the dart center of rotation
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

    def chiappetta_basic_Skirt(self):

        print(self.m)
        if self.pname in ['W2C','W3C','W4C','W5C','W6C','W8C']:
            pince = {'W2C':6,'W3C':6.25,'W4C':6.5,'W5C':6.75,'W6C':7,'W8C':7.25}
            #basic points
            A = Point([0,self.m["taille_genou"]-4])
            B = A + Point([(self.m["tour_bassin"]+self.ease)/2,0])
            C = Point([0,0])
            D = C + Point([(self.m["tour_bassin"]+self.ease)/2,0])

            A1 = A + Point([0,-self.m["hauteur_bassin"]])
            B1 = A1 + Point([(self.m["tour_bassin"]+self.ease)/2,0])

            A2 = A + Point([0,-1])
            B2 = B +Point([0,-0.5])

            F = self.middle(A, B)
            E = self.middle(C, D)

            G = A + Point([self.m["tour_taille"]/4  + 2, 0])
            H = B + Point([-self.m["tour_taille"]/4  - 2, 0])

            # again we need two control points for the french curve because we need at lease three
            # add one point between A1 and B1
            C1 = self.middle(A1, B1)
            # add a second just upp by one cm to control the tangents
            C2 = C1 + Point([0,-1])
            # get the curves
            points_skirt_front = [H, C1, C2]
            dbskirt_f, skirt_front_side = self.pistolet(points_skirt_front, 2, tot = True)
            points_skirt_back = [G, C1, C2]
            dbskirt_b, skirt_back_side = self.pistolet(points_skirt_back, 2, tot = True)

            #back
            back_curves = True
            dart1 = A + Point([self.distance(A, G)/2,- pince[self.pname]])
            I1,I2 = self.add_dart(dart1, A2, G, 2, draw_curves=back_curves)
            #front
            front_curves = True
            dart2 = B + Point([-self.distance(B, H)/2,- pince[self.pname]])
            # I3_curve, I4_curve = self.add_dart(dart2, B2, H, 2, draw_curves = True)
            I3, I4 = self.add_dart(dart2, B2, H, 2, draw_curves = front_curves, order='rl')

            #dics and lists
            key=['A', 'A1','A2',  'dart1', 'G','C']
            val=[A,A1,A2,dart1,G,C]

            for i in range(len(key)): # add new points to the dictionnary
                self.Back_points_dic[key[i]] = val[i]

            if back_curves:
                #in this case I1 and I2 are lists of positions
                self.Back_vertices = [A2.pos()]+ I1 + [dart1.pos()] + I2 + [G.pos()] + skirt_back_side + [E.pos(), C.pos()]
            else:
                # in this case I1 and I2 are points
                self.Back_vertices = [A2.pos(), I1.pos(), dart1.pos(), I2.pos(), G.pos()] + skirt_back_side + [E.pos(), C.pos()]

            # key=['B', 'B1', 'B2', 'I4', 'I3', 'dart2', 'H','F','E','D']
            # val=[B,B1,B2,I4,I3,dart2,H,F,E,D]
            key=['B', 'B1', 'B2', 'dart2', 'H','F','E','D']
            val=[B,B1,B2,dart2,H,F,E,D]

            for i in range(len(key)): # add new points to the dictionnary
                self.Front_points_dic[key[i]] = val[i]

            #redraw the front bodice with the added dart
            if front_curves:
                self.Front_vertices = [B2.pos()] + I3 + [dart2.pos()] + I4 + [H.pos()] + skirt_front_side + [E.pos(), D.pos()]
            else:
                self.Front_vertices = [B2.pos(), I4.pos(), dart2.pos(), I3.pos(), H.pos()] + skirt_front_side + [E.pos(), D.pos()]

    def generate_lists(self):
    	"""
    	generates a list of point vertices and a list of point dictionnaries for drawing
    	this method can only be called by children classes but is common to them

    	"""

    	vl = [self.Front_vertices, self.Back_vertices]
    	dl = [self.Front_points_dic, self.Back_points_dic]

    	return dl, vl


    def draw_skirt(self, dic = {"Pattern":"Skirt"}, save = False, fname = None, paper='FullSize'):
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
    	# ax = self.print_info(ax, dic)

    	# 3 print specific drawings
    	# if self.style == 'Donnanno':
    		# print("to be done")
    	# else:
    		# ax = self.add_legends(ax)

    	if save:
    		if fname:
    			pass
    		else:
    			fname = 'Basic_Skirt'

    		of = '../patterns/'+ self.style + '_' + fname + '_' + self.pname +'_FullSize.pdf'

    		plt.savefig(of)

    		if paper != 'FullSize':
    			self.paper_cut(fig, ax, name = fname, paper = paper)

    	return fig, ax
