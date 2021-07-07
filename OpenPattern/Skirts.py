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

    def __init__(self, pname="W6C", style='Chiappetta', gender = 'G', ease=8, curves=False):
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
        self.curves = curves


        self.dic_list=[]
        self.vertices_list=[]

        self.points_dic = {}
        self.Front_dic = {}
        self.Back_dic = {}

        self.Front_vertices = []
        self.Back_vertices = []

        # self.skirt_back_side = []
        # self.skirt_front_side = []


        # calculate Basic Skirt and sleeve
        if self.style == 'Donnanno':
            print("style Donnanno selected")
            self.donnanno_basic_skirt()


        elif self.style == 'Gilewska':
            print("style Gilewska selected")
            self.Gilewska_basic_skirt()

        elif self.style == 'Chiappetta':
            print("style Chiappetta selected")
            self.chiappetta_basic_skirt()


    def Gilewska_basic_skirt(self):
        """Basic pencil skirt whith slight asymmetry

        """
        A = Point([0,self.m["hauteur_taille_genou"]])
        B = A + Point([self.m["tour_bassin"]/2,0])
        D = Point([0,0])
        F = D + Point([self.m["tour_bassin"]/2,0])
        E = self.middle(D,F) + Point([-1,0])
        C = self.middle(A,B) + Point([-1,0])

        H = A + Point([0,-self.m["hauteur_bassin"]])
        H2 = B + Point([0,-self.m["hauteur_bassin"]])
        H1 = self.middle(H,H2) + Point([-1,0])


        # dart calculation for two darts
        # dart centers
        DF = B + Point([-self.m['ecart_poitrine']/2,-9])
        DB = A + Point([self.m['ecart_poitrine']/2,-12])

        dw = 0.5*(self.m['tour_bassin']-self.m['tour_taille'])

        if dw > 12:
            dwfb  = 3 # max front and back dart = 3
            dwbc = 1 # center back
            dws = 0.5*dw - dwfb - dwbc # side dart
        else:
            dwfb = np.floor((dw-1)/4) # front and back darts
            dwbc = 1 # center back
            dws = np.ceil((dw-1)/4) # sides


        K = B + Point([0,-1.5])
        J = C + Point([dws,0])
        L = C + Point([-dws,0])
        P = A + Point([1,-1.5])

        T4,T5 = self.add_dart(DB,P,L,dwfb,draw_curves=True)
        T2,T3 = self.add_dart(DF,J,K,dwfb,draw_curves=True)
        self.waist_curves = [T2,T3,T4,T5]

        #sides
        H3 = C +Point([0,-14]) # place a control point slightly below the depth of the back dart
        points_back_side = [L,H3,H1]
        ds, skirt_back_side = self.pistolet(points_back_side, 2,tot=True)
        points_front_side = [H1, H3, J]
        ds, skirt_front_side = self.pistolet(points_front_side, 2,tot=True)

        self.Back_vertices = [[D.pos(),H.pos(),P.pos()] + T4 + [DB.pos()] + T5 + skirt_back_side +\
        [E.pos(),D.pos()]]
        self.Front_vertices = [[E.pos()] + skirt_front_side +  T2 + [DF.pos()] + T3 +\
        [H2.pos(),F.pos(),E.pos()]]

        key = ['D','H','P','A','L','H1','E','DB']
        val = [D,H,P,A,L,H1,E,DB]
        for k,v in zip(key,val):
            self.Back_dic[k] = v

        key = ['E','H1','J','DF','B','K','H2','F']
        val = [E,H1,J,DF,B,K,H2,F]
        for k,v in zip(key,val):
            self.Front_dic[k] = v

        self.set_fold_line(H2 + Point([0,-2]), F + Point([0,2]), 'right')
        self.set_fold_line(H + Point([0,-2]), D + Point([0,2]), 'left')
        self.add_labelled_line(H, H2, 'HIP LINE','t')
        self.add_labelled_line(A, B, 'WAIST LINE','t')
        self.add_comment(self.middle(E,F)+Point([0,5]),'FRONT')
        self.add_comment(self.middle(D,E)+Point([0,5]),'BACK')
        self.set_grainline(DF + Point([0,-30]))

    def chiappetta_basic_skirt(self):
        """Basic pencil skirt (jupe droite)
           for girls between 2 and 16.
        """

        # print(self.m)
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

        # get the sides curves
        #here we add the front and back sides to the properties of the skirt
        #so we can alter them individually by transformations

        points_skirt_front = [H, C1, C2]
        dbskirt_f, self.skirt_front_side = self.pistolet(points_skirt_front, 2, tot = True)
        points_skirt_back = [G, C1, C2]
        dbskirt_b, self.skirt_back_side = self.pistolet(points_skirt_back, 2, tot = True)

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
                self.Back_vertices = [[A2.pos()]+ I1 + [dart1.pos()] + I2 + [G.pos()] + skirt_back_side + [E.pos(), C.pos()]]
            else:
                # in this case I1 and I2 are points
                self.Back_vertices = [[A2.pos(), I1.pos(), dart1.pos(), I2.pos(), G.pos()] + skirt_back_side + [E.pos(), C.pos()]]

            # key=['B', 'B1', 'B2', 'I4', 'I3', 'dart2', 'H','F','E','D']
            # val=[B,B1,B2,I4,I3,dart2,H,F,E,D]
            key=['B', 'B1', 'B2', 'dart2', 'H','F','E','D']
            val=[B,B1,B2,dart2,H,F,E,D]

            for i in range(len(key)): # add new points to the dictionnary
                self.Front_dic[key[i]] = val[i]

            #redraw the front bodice with the added dart
            if front_curves:
                self.Front_vertices = [[B2.pos()] + I3 + [dart2.pos()] + I4 + [H.pos()] + self.skirt_front_side + [E.pos(), D.pos()]]
            else:
                self.Front_vertices = [[B2.pos(), I4.pos(), dart2.pos(), I3.pos(), H.pos()] + self.skirt_front_side + [E.pos(), D.pos()]]
        else:
            key=['A', 'A1','A2',  'dart11', 'dart12','I11','I12','I21','I22', 'G','C']
            val=[A, A1, A2, dart11, dart12, I11, I12, I21, I22, G, C]

            for i in range(len(key)): # add new points to the dictionnary
                self.Back_dic[key[i]] = val[i]

            self.Back_vertices = [[A2.pos(), I11.pos(), dart11.pos(), I21.pos(), I12.pos(),dart12.pos(),I22.pos(), G.pos()] + self.skirt_back_side + [E.pos(), C.pos()]]

            key=['B', 'B1', 'B2', 'dart21','dart22','I31','I32','I41','I42' ,'H','F','E','D']
            val=[B, B1, B2, dart21, dart22, I31, I32, I41, I42, H, F, E, D]

            for i in range(len(key)): # add new points to the dictionnary
                self.Front_dic[key[i]] = val[i]

            self.Front_vertices = [[B2.pos(), I41.pos(), dart21.pos(), I31.pos(), I42.pos(), dart22.pos(), I32.pos(), H.pos()] + self.skirt_front_side + [E.pos(), D.pos()]]

        self.set_fold_line(A1 + Point([0,-2]), C + Point([0,2]), 'left')
        self.set_fold_line(B1 + Point([0,-2]), D + Point([0,2]), 'right')
        self.add_labelled_line(A1, B1, 'HIP LINE','t')
        self.add_labelled_line(A, B, 'WAIST LINE','t')
        self.add_comment(self.middle(E,D)+Point([0,5]),'FRONT')
        self.add_comment(self.middle(C,E)+Point([0,5]),'BACK')
        if self.pname not in ['W14C','W16C']:
            self.set_grainline(dart1 + Point([0,-20]))
        else:
            self.set_grainline(dart12 + Point([0,-20]))

    def donnanno_basic_skirt(self):
        """Pencil skirt
        """
        # the frame first
        A = Point([0,self.m["hauteur_taille_genou"]-4])
        B = Point([0,0])
        C = B + Point([(self.m["tour_bassin"]+self.ease)/2,0])
        D = A + Point([(self.m["tour_bassin"]+self.ease)/2,0])

        E = self.middle(A,D)
        F = self.middle(B,C)


        G = A + Point([0,-self.m['hauteur_bassin']])
        H = G + Point([(self.m["tour_bassin"]+self.ease)/2,0])

        E1 = E + Point([0,-self.m['hauteur_bassin']+5])
        E2 = E + Point([0,-self.m['hauteur_bassin']])

        A1 = A + Point([0,-2])
        D1 = D + Point([0,-2])


        # darts
        S3 = D + Point([-self.m['ecart_poitrine']/2,-14])
        S4 = A + Point([self.m['ecart_poitrine']/2,-8])


        dw = 0.5*(self.m['tour_bassin']-self.m['tour_taille'])

        if dw > 12:
            dwfb  = 3 # max front and back dart = 3
            dws = 0.5*dw - dwfb
        else:
            dwfb = np.floor(dw/4)
            dws = np.ceil(dw/4)


        W1 = E + Point([-dws,0])
        W = E + Point([dws,0])

        if self.curves:
            T4,T5 = self.add_dart(S4,A1,W1,dwfb,draw_curves=True)
            T2,T3 = self.add_dart(S3,W,D1,dwfb,draw_curves=True)
            self.waist_curves = [T2,T3,T4,T5]
        else:
            T4,T5 = self.add_dart(S4,A1,W1,dwfb)
            T2,T3 = self.add_dart(S3,D1,W,dwfb)


        #sides here we add the front and back sides to the properties of the skirt
        #so we can alter them individually by transformations
        points_skirt_front = [W1,E1,E2]
        dbskirt_f, self.skirt_front_side = self.pistolet(points_skirt_front, 2, tot = True)
        points_skirt_back = [E2,E1,W]
        dbskirt_b, self.skirt_back_side = self.pistolet(points_skirt_back, 2, tot = True)

        #dics and lists
        key = ['A','A1','G','B','F','E1','E2','W1','S4']
        val = [A,A1,G,B,F,E1,E2,W1,S4]

        for i in range(len(key)):
            self.Front_dic[key[i]] = val[i]

        key = ['C','H','D1','D','W','S3','E1','E2','F']
        val=[C,H,D1,D,W,S3,E1.copy(),E2.copy(),F.copy()]
        for i in range(len(key)):
            self.Back_dic[key[i]] = val[i]

        if self.curves:
            self.Back_vertices = [[C.pos(),F.pos(),E2.pos()] + self.skirt_back_side + [W.pos()] + T2 + [S3.pos()] + T3 + [D1.pos(),C.pos()]]
            self.Front_vertices = [[B.pos(),A1.pos()] + T4 + [S4.pos()] + T5 + [W1.pos()] + self.skirt_front_side + [E2.pos(),F.pos(),B.pos()]]
        else:
            self.Back_dic['T3'] = T3
            self.Back_dic['T2'] = T2
            self.Front_dic['T4'] = T4
            self.Front_dic['T5'] = T5

            self.Back_vertices = [[F.pos(),C.pos(),D1.pos(), T3.pos(),S3.pos(),T2.pos(),W.pos()] + self.skirt_back_side[::-1] + [F.pos(),C.pos()]]
            self.Front_vertices = [[B.pos(),A1.pos(),T4.pos(),S4.pos(),T5.pos(),W1.pos()] + self.skirt_front_side + [E2.pos(),F.pos(),B.pos()]]

        self.set_fold_line(G + Point([0,-2]), B + Point([0,2]), 'left')
        self.set_fold_line(H + Point([0,-2]), C + Point([0,2]), 'right')
        self.add_labelled_line(G, H, 'HIP LINE','t')
        self.add_labelled_line(A, D, 'WAIST LINE','t')
        self.add_comment(self.middle(B,F)+Point([0,5]),'FRONT')
        self.add_comment(self.middle(F,C)+Point([0,5]),'BACK')
        self.set_grainline(S3 + Point([0,-20]))

###################################################################################################
###################################################################################################

class Waistband(Pattern):
    """draws a waist band with different styles depending on init arguments
    """

    def __init__(self, pname="W6C", ease=8, height=5, style='Donnanno'):
        """
        Initilizes parent class &  attributes
        launches the calculation of waistband

        Args:
            pname: size measurements
            style: style to be used for drafting
            age: used if for a child and style = Chiappetta.

        """
        Pattern.__init__(self, pname)

        self.ease = ease
        self.style = style

        self.dic_list=[]
        self.vertices_list=[]

        self.Front_dic = {}
        self.Back_dic = {}

        self.Front_vertices = []
        self.Back_vertices = []

        self.add_waistband(height)

    def add_waistband(self, wb_height = 5):


        B = Point([0, 0])
        A = B + Point([0, 2*wb_height])
        E = B + Point([0, wb_height])
        C = B + Point([self.m['tour_taille'] + 4 + self.ease, 0])
        D = C + Point([0, 2*wb_height])
        F = C + Point([0, wb_height])

        A1 = A + Point([2, 0])
        B1 = B + Point([2, 0])
        C1 = C + Point([-2, 0])
        D1 = D + Point([-2, 0])
        key = ['wA', 'wA1', 'wB', 'wB1', 'wC', 'wC1', 'wD', 'wD1', 'wE', 'wF']
        val = [A,A1,B,B1,C,C1,D,D1,E,F]

        for k,v in zip(key,val):
            self.Front_dic[k] = v

            wb = [B.pos(),A.pos(),D.pos(),C.pos(),B.pos()]
            self.Front_vertices.append(wb)

        self.add_labelled_line(E, F, 'FOLD','t')
        self.add_labelled_line(A1, B1, '')
        self.add_labelled_line(D1, C1, '')
        self.add_comment(self.middle(B,C)+Point([0,-1]),'CENTRE FRONT')
        self.add_comment(self.middle(B,C),'o')

###################################################################################################
###################################################################################################

class Skirt_transform(Basic_Skirt):
    """Transformations of the Basic pencil skirt

    Donnanno
        - shifted side seams with kick pleats

    """

    def __init__(self, pname="W6C", style='Chiappetta', gender = 'G', ease = 8, curves = False, overlay = False, model = 'shifted', side_offset=5):

        Basic_Skirt.__init__(self, pname, style, gender, ease, curves)

        self.style = style
        self.ease = ease
        self.curves = curves
        self.model = model
        self.overlay = overlay

        # We DO NOT initialize the disc and list because they are initialized by the parent class
        # but we keep a copy of it before transforming it
        self.pattern_list.append(self.copy())

        if self.style == 'Donnanno':
            if self.model == 'shifted':
                self.shifted_side_seams()
            elif self.model == 'A-Line':
                self.A_Line(side_offset)
            elif self.model == 'Flared-A-Line':
                self.Flared_A_Line(side_offset)

    def shifted_side_seams(self, offset = 2, pleat_height = 20, pleat_width = 8):
        """ Moves the side by offset cm so the seam is positionned slightly at the back of the Skirt

        :param offset: float or int value of side offset
        """

        #move points
        self.Front_dic['W1'].move([offset,0])
        self.Front_dic['E1'].move([offset,0])
        self.Front_dic['E2'].move([offset,0])
        self.Front_dic['F'].move([offset,0])

        self.Back_dic['W'].move([offset,0])
        self.Back_dic['E1'].move([offset,0])
        self.Back_dic['E2'].move([offset,0])
        self.Back_dic['F'].move([offset,0])

        #add kick pleats
        X = self.Back_dic['C'] + Point([0,pleat_height])
        X1 = X + Point([pleat_width,0])
        C1 = self.Back_dic['C'] + Point([pleat_width,0])
        self.Back_dic['X'] = X
        self.Back_dic['X1'] = X1
        self.Back_dic['C1'] = C1
        #move curves
        for i in range(len(self.skirt_front_side)):
            self.skirt_front_side[i][0] += offset

        for i in range(len(self.skirt_back_side)):
            self.skirt_back_side[i][0] += offset

        if self.curves:
            # redraw the waist curves
            dw = 0.5*(self.m['tour_bassin']-self.m['tour_taille'])

            if dw > 12:
                dwfb  = 3 # max front and back dart = 3
            else:
                dwfb = np.floor(dw/4)

            T4,T5 = self.add_dart(self.Front_dic['S4'],self.Front_dic['A1'],self.Front_dic['W1'],dwfb,draw_curves=True)
            T2,T3 = self.add_dart(self.Back_dic['S3'],self.Back_dic['W'],self.Back_dic['D1'],dwfb,draw_curves=True)

            self.Back_vertices = [ [self.Back_dic['C'].pos(), self.Back_dic['F'].pos(), self.Back_dic['E1'].pos()] +\
             self.skirt_back_side + [self.Back_dic['W'].pos()] + T2 + [self.Back_dic['S3'].pos()] +\
              T3 + [self.Back_dic['D1'].pos(),self.Back_dic['C'].pos()],\
             [self.Back_dic['C'].pos(), C1.pos(), X1.pos(), X.pos()]]

            self.Front_vertices = [[self.Front_dic['B'].pos(),self.Front_dic['A1'].pos()] + T4 +\
            [self.Front_dic['S4'].pos()] + T5 + [self.Front_dic['W1'].pos()] + self.skirt_front_side\
             + [self.Front_dic['E2'].pos(),self.Front_dic['F'].pos(),self.Front_dic['B'].pos()]]

        else:
            self.Back_vertices = [[self.Back_dic['F'].pos(),self.Back_dic['C'].pos(), self.Back_dic['D1'].pos(),\
             self.Back_dic['T3'].pos(),self.Back_dic['S3'].pos(),self.Back_dic['T2'].pos(),self.Back_dic['W'].pos()]\
             + self.skirt_back_side[::-1] + [self.Back_dic['F'].pos(),self.Back_dic['C'].pos()],\
             [self.Back_dic['C'].pos(), C1.pos(), X1.pos(), X.pos()]]

            self.Front_vertices = [[self.Front_dic['B'].pos(),self.Front_dic['A1'].pos(),self.Front_dic['T4'].pos(),\
            self.Front_dic['S4'].pos(),self.Front_dic['T5'].pos(),self.Front_dic['W1'].pos()] + self.skirt_front_side\
             + [self.Front_dic['E2'].pos(),self.Front_dic['F'].pos(),self.Front_dic['B'].pos()]]

        self.add_labelled_line(self.middle(X,X1),self.middle(self.Back_dic['C'],C1),'FOLD','l')
        del self.fold_line[1]

    def A_Line(self,side_offset=5):
        """ A-line adapted from the basic pencil skirt

        - R = [E1F]
        - theta = side_offset/R the most simple way to draw a correct side
        - add F1 a control point at side_offset from the original position of F
        - rotate F by theta around E1
        - rotate E2 by theta around E1
        - redraw the side curves
        - draw the curve F-F1-C for the Hem.
        - do the opposite for the front
        - offset all points before drawing

        :param side_offset: the value of the lateral enlargement of the side.
        """
        #parameters
        R =self.distance(self.Back_dic['F'],self.Back_dic['E1'])
        theta = np.arctan(side_offset/R)

        ###########
        #Back
        ###########
        F1 = self.Back_dic['F'] + Point([side_offset,0])
        self.Back_dic['F1'] = F1

        #translate all points so skirt sides do not overlap
        for key,val in self.Back_dic.items():
            val.move([3*side_offset,0])

        self.Back_dic['F'].rotate(self.Back_dic['E1'].pos(), -theta, unit='rad')
        self.Back_dic['E2'].rotate(self.Back_dic['E1'].pos(), -theta, unit='rad')

        #draw curves
        points_hem_back = [self.Back_dic['C'],self.Back_dic['F1'],self.Back_dic['F']]
        hem_length, hem_curve_back = self.pistolet(points_hem_back, 2, tot = True)

        points_skirt_back = [self.Back_dic['E2'],self.Back_dic['E1'],self.Back_dic['W']]
        dbskirt_b, self.skirt_back_side = self.pistolet(points_skirt_back, 2, tot = True)


        ###############
        #Front
        ##############

        F1 = self.Front_dic['F'] + Point([-side_offset,0])
        self.Front_dic['F1'] = F1


        self.Front_dic['F'].rotate(self.Front_dic['E1'].pos(), theta, unit='rad')
        self.Front_dic['E2'].rotate(self.Front_dic['E1'].pos(), theta, unit='rad')

        points_hem_front = [self.Front_dic['F'],self.Front_dic['F1'],self.Front_dic['B']]
        hem_length, hem_curve_front = self.pistolet(points_hem_front, 2, tot = True)

        points_skirt_front = [self.Front_dic['W1'],self.Front_dic['E1'],self.Front_dic['E2']]
        dbskirt_b, self.skirt_front_side = self.pistolet(points_skirt_front, 2, tot = True)


        ######################
        # built skirt vertices
        ######################
        if self.curves:
            # redraw the waist curves
            dw = 0.5*(self.m['tour_bassin']-self.m['tour_taille'])

            if dw > 12:
                dwfb  = 3 # max front and back dart = 3
            else:
                dwfb = np.floor(dw/4)

            T4,T5 = self.add_dart(self.Front_dic['S4'],self.Front_dic['A1'],self.Front_dic['W1'],dwfb,draw_curves=True)
            T2,T3 = self.add_dart(self.Back_dic['S3'],self.Back_dic['W'],self.Back_dic['D1'],dwfb,draw_curves=True)

            self.Back_vertices = [ hem_curve_back + [self.Back_dic['E2'].pos()] +\
             self.skirt_back_side + [self.Back_dic['W'].pos()] + T2 + [self.Back_dic['S3'].pos()] +\
              T3 + [self.Back_dic['D1'].pos(),self.Back_dic['C'].pos()]]

            self.Front_vertices = [[self.Front_dic['B'].pos(),self.Front_dic['A1'].pos()] + T4 +\
            [self.Front_dic['S4'].pos()] + T5 + [self.Front_dic['W1'].pos()] + self.skirt_front_side\
             + [self.Front_dic['E2'].pos()] + hem_curve_front]

        else:
            self.Back_vertices = [hem_curve_back[::-1] + [self.Back_dic['D1'].pos(),\
             self.Back_dic['T3'].pos(),self.Back_dic['S3'].pos(),self.Back_dic['T2'].pos(),self.Back_dic['W'].pos()]\
             + self.skirt_back_side[::-1] + [self.Back_dic['F'].pos()]]

            self.Front_vertices = [[self.Front_dic['B'].pos(),self.Front_dic['A1'].pos(),self.Front_dic['T4'].pos(),\
            self.Front_dic['S4'].pos(),self.Front_dic['T5'].pos(),self.Front_dic['W1'].pos()] + self.skirt_front_side\
             + [self.Front_dic['E2'].pos()] + hem_curve_front]

        del self.fold_line[1]
        self.set_fold_line(self.Back_dic['H'] + Point([0,-2]), self.Back_dic['C'] + Point([0,2]), 'right')

    def Flared_A_Line(self, side_offset = 5):
        """Flared A line.
        add the closure of darts and corresponding expansion at the hem.

        to rotate a portion of the pattern
        calculate angle of rotation = angle of dart to be closed
        select points to be rotated
        select curves to be rotated
        rotate around the dart point
        """
        # start by making an
        self.A_Line(side_offset)

        #offset all the back points
        for key,val in self.Back_dic.items():
            val.move([3*side_offset,0])

        #cutting points
        HR = Point([self.Front_dic['S4'].x,0]) # vertical projection of S4 on hem = cutting point
        self.Front_dic['HR'] = HR

        HR = Point([self.Back_dic['S3'].x,0]) # vertical projection of S3 on hem = cutting point
        self.Back_dic['HR'] = HR

        if self.curves:
            # calculate angle
            # self.waist_curves = [T2,T3,T4,T5]
            num_f = self.distance(Point(self.waist_curves[2][-1]),Point(self.waist_curves[3][0]))
            self.Front_dic['S4'].y = self.Back_dic['S3'].y #lower S4 to the level of S3 so the rotation is the same
            den_f = self.distance(Point(self.waist_curves[2][-1]),self.Front_dic['S4'])
            alpha_f = num_f/den_f

            self.Front_dic['T4'] = Point(self.waist_curves[2][-1])

            Front_Point_names = ['HR','F1','F','E2','E1','W1','T4']

            # calculate angle back
            T2 = Point(self.waist_curves[0][-1])
            T2.move([6*side_offset,0]) # offset times 2  because we start from the A-line skirt.
            T3 = Point(self.waist_curves[1][0])
            T3.move([6*side_offset,0])

            num_b = self.distance(T2,T3)
            den_b = self.distance(T2,self.Back_dic['S3'])
            alpha_b = -num_b/den_b

            self.Back_dic['T2'] = T2
            Back_Point_names = ['HR','F1','F','E2','E1','W', 'T2']

        else:

            # calculate angle front
            num_f = self.distance(self.Front_dic['T4'],self.Front_dic['T5'])
            self.Front_dic['S4'].y = self.Back_dic['S3'].y #lower S4 to the level of S3 so the rotation is the same
            den_f = self.distance(self.Front_dic['T4'],self.Front_dic['S4'])
            alpha_f = num_f/den_f

            Front_Point_names = ['HR','F1','F','E2','E1','W1','T5']

            # calculate angle back
            num_b = self.distance(self.Back_dic['T2'],self.Back_dic['T3'])
            den_b = self.distance(self.Back_dic['T2'],self.Back_dic['S3'])
            alpha_b = -num_b/den_b

            Back_Point_names = ['HR','F1','F','E2','E1','W','T2']

        #FRONT
        for key in Front_Point_names:
            self.Front_dic[key].rotate(self.Front_dic['S4'], alpha_f, unit='rad')

        #BACK
        for key in Back_Point_names:
            self.Back_dic[key].rotate(self.Back_dic['S3'], alpha_b, unit='rad')

        #redraw hem and side curve
        #FRONT
        points_hem_front = [self.Front_dic['F'],self.Front_dic['F1'],self.Front_dic['HR'],self.Front_dic['B']]
        hem_length, hem_curve_front = self.pistolet(points_hem_front, 2, tot = True)

        points_skirt_front = [self.Front_dic['W1'],self.Front_dic['E1'],self.Front_dic['E2']]
        dbskirt_b, self.skirt_front_side = self.pistolet(points_skirt_front, 2, tot = True)

        #BACK
        points_hem_Back = [self.Back_dic['C'],self.Back_dic['HR'],self.Back_dic['F1'],self.Back_dic['F']]
        hem_length, hem_curve_back = self.pistolet(points_hem_Back, 2, tot = True)

        points_skirt_Back = [self.Back_dic['E2'],self.Back_dic['E1'],self.Back_dic['W']]
        dbskirt_b, self.skirt_back_side = self.pistolet(points_skirt_Back, 2, tot = True)

        if self.curves:

            points_front_waist = [self.Front_dic['A1'],self.Front_dic['T4'],self.Front_dic['W1']]
            fwl, front_waist_curve =  self.pistolet(points_front_waist, 2, tot = True)

            points_back_waist = [self.Back_dic['W'],self.Back_dic['T2'],self.Back_dic['D1']]
            bwl, back_waist_curve =  self.pistolet(points_back_waist, 2, tot = True)

            self.Back_vertices = [ hem_curve_back + [self.Back_dic['E2'].pos()] +\
             self.skirt_back_side + [self.Back_dic['W'].pos()] + back_waist_curve +\
             [self.Back_dic['D1'].pos(),self.Back_dic['C'].pos()]]

            self.Front_vertices = [[self.Front_dic['B'].pos(),self.Front_dic['A1'].pos()] + front_waist_curve +\
            [self.Front_dic['W1'].pos()] + self.skirt_front_side +\
            [self.Front_dic['E2'].pos()] + hem_curve_front]


        else:
            #redraw vertices
            self.Front_vertices = [[self.Front_dic['B'].pos(),self.Front_dic['A1'].pos(),self.Front_dic['T5'].pos(),\
            self.Front_dic['W1'].pos()] + self.skirt_front_side + [self.Front_dic['E2'].pos()] + hem_curve_front]

            #redraw vertices
            self.Back_vertices = [hem_curve_back + [self.Back_dic['E2'].pos()] +  self.skirt_back_side +\
             [self.Back_dic['T2'].pos(),self.Back_dic['D1'].pos(), self.Back_dic['C'].pos()]]

            del self.labelled_line[:]
            del self.grainline[:]
            del self.fold_line[1]
            self.set_grainline(self.Back_dic['E2']+Point([10,-20]),20, np.pi/2)
            self.set_fold_line(self.Back_dic['H'] + Point([0,-2]), self.Back_dic['C'] + Point([0,2]), 'right')

        del self.fold_line[1]
        del self.labelled_line[:]
        del self.grainline
        self.set_grainline(self.Back_dic['E2']+Point([10,-20]),20 , np.pi/2)
        self.set_fold_line(self.Back_dic['H'] + Point([0,-2]), self.Back_dic['C'] + Point([0,2]), 'right')


class Culotte(Basic_Skirt):
    """Transformations of the Basic pencil skirt into culottes

    Donnanno

    """

    def __init__(self, pname="sophie", style='Donnanno', gender = 'W', ease = 8, overlay = False, model='basic'):

        Basic_Skirt.__init__(self, pname, style, gender, ease, curves=False)

        self.style = style
        self.ease = ease
        self.curves = False
        self.model = model
        self.overlay = overlay

        # We DO NOT initialize the disc and list because they are initialized by the parent class
        # but we keep a copy of it before transforming it
        self.pattern_list.append(self.copy())

        if self.style == 'Donnanno':
            if self.model == 'basic':
                self.donnanno_basic_culotte()


    def donnanno_basic_culotte(self):

        #add body rise
        P = self.Front_dic['G'] + [0,-self.m["tour_bassin"]/10]
        I = P + [-self.m["tour_bassin"]/10,0]
        B1 = self.Front_dic['B'] + [-self.m["tour_bassin"]/10,0]
        self.Front_dic['P'] = P
        self.Front_dic['I'] = I
        self.Front_dic['B1'] = B1

        O = self.Back_dic['H'] + [0,-self.m["tour_bassin"]/10]
        L = O + [self.m["tour_bassin"]/10,0]
        C1 = self.Back_dic['C'] + [self.m["tour_bassin"]/10,0]
        self.Back_dic['O'] = O
        self.Back_dic['L'] = L
        self.Back_dic['C1'] = C1

        #add the control points for the body rise curve
        control_P = P + [-4*np.cos(np.pi/4),4*np.sin(np.pi/4)]
        control_O = O + [5*np.cos(np.pi/4),5*np.sin(np.pi/4)]

        #modify the waist
        self.Front_dic['W1'] += [2,0]
        self.Front_dic['A1'] += [2,0]
        self.Back_dic['W'] += [-2,0]
        self.Back_dic['D1'] += [-2,4]

        # recalculate the darts
        dw = 0.5*(self.m['tour_bassin']-self.m['tour_taille'])
        if dw > 12:
            dwfb  = 3 # max front and back dart = 3
        else:
            dwfb = np.floor(dw/4)

        self.Front_dic['T4'],self.Front_dic['T5'] = self.add_dart(self.Front_dic['S4'],self.Front_dic['A1'],self.Front_dic['W1'],dwfb)
        self.Back_dic['T2'],self.Back_dic['T3'] = self.add_dart(self.Back_dic['S3'],self.Back_dic['D1'],self.Back_dic['W'],dwfb)


        #redraw curves...not the waist curve for now
        points_skirt_front = [self.Front_dic['W1'],self.Front_dic['E1'],self.Front_dic['E2']]
        dbskirt_f, self.skirt_front_side = self.pistolet(points_skirt_front, 2, tot = True)
        points_skirt_back = [self.Back_dic['E2'],self.Back_dic['E1'],self.Back_dic['W']]
        dbskirt_b, self.skirt_back_side = self.pistolet(points_skirt_back, 2, tot = True)

        points_front_fourche = [I,control_P, self.Front_dic['G']]
        db_ff, front_fourche = self.pistolet(points_front_fourche, 2, tot = True)
        points_back_fourche = [L,control_O,self.Back_dic['H']]
        db_bf, back_fourche = self.pistolet(points_back_fourche, 2, tot = True)

        #vertices
        self.Back_vertices = [[self.Back_dic['F'].pos(),self.Back_dic['C1'].pos(),self.Back_dic['L'].pos()] +\
         back_fourche + [self.Back_dic['D1'].pos(), self.Back_dic['T3'].pos(), self.Back_dic['S3'].pos(), self.Back_dic['T2'].pos(), self.Back_dic['W'].pos()] +\
         self.skirt_back_side[::-1] + [self.Back_dic['F'].pos(),self.Back_dic['C1'].pos()]]
        self.Front_vertices = [[self.Front_dic['B1'].pos(), self.Front_dic['I'].pos()] +\
         front_fourche + [self.Front_dic['A1'].pos(),self.Front_dic['T4'].pos(),self.Front_dic['S4'].pos(),self.Front_dic['T5'].pos(),self.Front_dic['W1'].pos()] +\
         self.skirt_front_side + [self.Front_dic['E2'].pos(), self.Front_dic['F'].pos(),self.Front_dic['B1'].pos()]]

        self.fold_line = []
        # self.add_comment(self.middle(self.Front_dic['B'], self.Front_dic['F'])+Point([0,5]),'FRONT')
        # self.add_comment(self.middle(self.Back_dic['F'], self.Back_dic['C'])+Point([0,5]),'BACK')
        # self.set_grainline(self.Back_dic['S3'] + Point([0,-20]))
