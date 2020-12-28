#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append('./..')
import sqlite3


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

        self.Skirt_points_dic = {}
        self.Skirt_Front_points_dic = {}
        self.Skirt_Back_points_dic = {}

        self.Skirt_Front_vertices = []
        self.Skirt_Back_vertices = []


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
