#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

sys.path.append("./..")
import sqlite3
import numpy as np


from OpenPattern.Pattern import *
from OpenPattern.Points import *


class Bowtie(Pattern):
    """
    Class to draw a bowtie pattern.
    Inherits from Pattern

    Attributes

        style: style used to draw the pattern as string (classic or diamond)

        # Attributes that control the dictionnaries used for size measurements
        pname: measurements used corresponding to a json file

        # dics used here:
        Front_dic

        # lists of vertices:
        Front vertices

        # the others are instanciated but not used

    """

    def __init__(self, pname="gregoire", width=5, pointe=0, **kwargs):
        """
        Initilizes parent class &  attributes
        launches the calculation of the tie


        :param  pname: size measurements
        :param  width: width of the tie
        :param pointe: length of the diamond if pointe=0 then draws a butterfly tie
        :param style: just for drawing

        """
        Pattern.__init__(self, pname, **kwargs)

        self.width = width
        self.pointe = pointe
        if pointe == 0:
            self.style = "Butterfly"
        else:
            self.style = "Diamond"

        self.dic_list = []
        self.vertices_list = []

        self.points_dic = {}
        self.Front_dic = {}
        self.Back_dic = {}

        self.Front_vertices = []
        self.Back_vertices = []

        self.calculate_tie()

    def calculate_tie(self):

        tc = self.m["tour_encolure"]

        w = 1.5  # width of the neck strip

        lam = tc / np.pi  # wave length of the neck diameter

        x = np.linspace(0, 1.5 * lam, 100)
        y = 0.25 * (self.width - w) * (np.cos(x * 2 * np.pi / lam) + 1) + w / 2

        fcurve = []
        bcurve = []
        for i in range(len(x)):
            fcurve.append([x[i], y[i]])
            bcurve.append([x[len(x) - 1 - i], -y[len(x) - 1 - i]])

        E = Point([x[-1] + tc / 2, y[-1]])
        F = Point([x[-1] + tc / 2, -y[-1]])

        diamond = Point([-self.pointe, 0])
        self.Front_vertices = fcurve + [E.pos(), F.pos()] + bcurve + [diamond.pos()]
