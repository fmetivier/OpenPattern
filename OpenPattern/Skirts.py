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

		Front_dic
        Back_dic

		# lists of vertices:

		Back_vertices
		Front_vertices

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
        self.Front_dic = {}
        self.Back_dic = {}

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

    def chiappetta_basic_Skirt(self):

        print(self.m)
        if self.pname in ['W2C','W3C','W4C','W5C','W6C','W8C','W10C','W12C']:
            pince = {'W2C':6,'W3C':6.25,'W4C':6.5,'W5C':6.75,'W6C':7,'W8C':7.25,'W10C':10,'W12C':10}
            if self.pname in ['W10C','W12C']:
                dw = 3
            else:
                dw=2
        else:
            if self.pname == 'W14C':
                dw=2.15
                pince=10
            elif self.pname == 'W16C':
                dw=2.5
                pince=10
        #basic points
        A = Point([0,self.m["hauteur_taille_genou"]-4])
        B = A + Point([(self.m["tour_bassin"]+self.ease)/2,0])
        C = Point([0,0])
        D = C + Point([(self.m["tour_bassin"]+self.ease)/2,0])

        A1 = A + Point([0,-self.m["hauteur_bassin"]])
        B1 = A1 + Point([(self.m["tour_bassin"]+self.ease)/2,0])

        A2 = A + Point([0,-1])
        B2 = B +Point([0,-0.5])

        F = self.middle(A, B)
        E = self.middle(C, D)

        if self.pname in ['W10C','W12C']:
            G = A + Point([self.m["tour_taille"]/4  + dw - 0.5, 0])
            H = B + Point([-self.m["tour_taille"]/4 - dw - 0.5, 0])
        elif self.pname in ['W14C','W16C']:
            G = A + Point([self.m["tour_taille"]/4  + 2*dw - 0.5, 0])
            H = B + Point([-self.m["tour_taille"]/4 - 2*dw - 0.5, 0])
        else:
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
        if self.pname not in ['W14C','W16C']:
            back_curves=True
            dart1 = A + Point([self.distance(A, G)/2,- pince[self.pname]])
            I1,I2 = self.add_dart(dart1, A2, G, dw, draw_curves=back_curves)
            #front
            front_curves = True
            dart2 = B + Point([-self.distance(B, H)/2,- pince[self.pname]])
            # I3_curve, I4_curve = self.add_dart(dart2, B2, H, 2, draw_curves = True)
            I3, I4 = self.add_dart(dart2, B2, H, dw, draw_curves = front_curves, order='rl')
        else:
            dart11 = A + Point([self.distance(A, G)/3,-pince])
            I11,I21 = self.add_dart(dart11, A2, G, dw)
            dart12 = A + Point([2*self.distance(A, G)/3,-pince])
            I12,I22 = self.add_dart(dart12, I21, G, dw)
            #front
            dart21 = B + Point([-self.distance(B, H)/3,- pince])
            I31, I41 = self.add_dart(dart21, B2, H, dw)
            dart22 = B + Point([-2*self.distance(B, H)/3,- pince])
            I32, I42 = self.add_dart(dart22, I31, H, dw)

        #dics and lists
        if self.pname not in ['W14C','W16C']:
            key=['A', 'A1','A2',  'dart1', 'G','C']
            val=[A,A1,A2,dart1,G,C]

            for i in range(len(key)): # add new points to the dictionnary
                self.Back_dic[key[i]] = val[i]

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
                self.Front_dic[key[i]] = val[i]

            #redraw the front bodice with the added dart
            if front_curves:
                self.Front_vertices = [B2.pos()] + I3 + [dart2.pos()] + I4 + [H.pos()] + skirt_front_side + [E.pos(), D.pos()]
            else:
                self.Front_vertices = [B2.pos(), I4.pos(), dart2.pos(), I3.pos(), H.pos()] + skirt_front_side + [E.pos(), D.pos()]
        else:
            key=['A', 'A1','A2',  'dart11', 'dart12','I11','I12','I21','I22', 'G','C']
            val=[A, A1, A2, dart11, dart12, I11, I12, I21, I22, G, C]

            for i in range(len(key)): # add new points to the dictionnary
                self.Back_dic[key[i]] = val[i]

            self.Back_vertices = [A2.pos(), I11.pos(), dart11.pos(), I21.pos(), I12.pos(),dart12.pos(),I22.pos(), G.pos()] + skirt_back_side + [E.pos(), C.pos()]

            key=['B', 'B1', 'B2', 'dart21','dart22','I31','I32','I41','I42' ,'H','F','E','D']
            val=[B, B1, B2, dart21, dart22, I31, I32, I41, I42, H, F, E, D]

            for i in range(len(key)): # add new points to the dictionnary
                self.Front_dic[key[i]] = val[i]

            self.Front_vertices = [B2.pos(), I41.pos(), dart21.pos(), I31.pos(), I42.pos(), dart22.pos(), I32.pos(), H.pos()] + skirt_front_side + [E.pos(), D.pos()]

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
