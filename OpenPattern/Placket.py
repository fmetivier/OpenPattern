#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

sys.path.append("./..")

from OpenPattern.Pattern import *
from OpenPattern.Points import *


class Placket(Pattern):
    """
    Sleeve placket and underlap (if wanted)

    """

    def __init__(
        self,
        pname="sophie",
        gender="w",
        placket_style="SimpleOneSide",
        slit_length=11,
        **kwargs
    ):

        Pattern.__init__(self, pname, gender, **kwargs)

        self.pl = placket_style
        self.sll = slit_length

        self.Placket_dic = []
        self.Placket_vertices = []
        self.Placket_segments = {}

        self.calculate_plackets()

    def calculate_plackets(self):

        if self.pl == "SimpleOneSide":

            Pbl = Point([0, 0])
            Pbm = Pbl + [3, 0]
            Pbr = Pbm + [3, 0]
            Pur = Pbr + [0, self.sll]
            Purm = Pbm + [0, self.sll]
            Pum = Pbm + [0, self.sll + 2]
            Pul = Pbl + [0, self.sll + 2]
            Ptip = self.middle(Pum, Pul) + Point([0, 2])

            self.Placket_dic.append(
                {
                    "Pbl": Pbl,
                    "Pbm": Pbm,
                    "Pbr": Pbr,
                    "Pur": Pur,
                    "Purm": Purm,
                    "Pum": Pum,
                    "Pul": Pul,
                    "Ptip": Ptip,
                }
            )
            self.Placket_vertices.append(
                [
                    Pbl.pos(),
                    Pbr.pos(),
                    Pur.pos(),
                    Purm.pos(),
                    Pum.pos(),
                    Ptip.pos(),
                    Pul.pos(),
                    Pbl.pos(),
                ]
            )

            self.Placket_segments = {"Fold": [Pbm + [1, 0], Purm + [1, 0]]}
            self.Placket_segments["fr"] = Ptip - [0, 1], Pum - [0, 1]
            self.Placket_segments["fl"] = Ptip - [0, 1], Pul - [0, 1]
            self.Placket_segments["slit line"] = Pur - [0, 1], Pul - [0, 3]

    def draw_placket(self, save=False):

        fig, ax = self.draw_pattern(self.Placket_dic, self.Placket_vertices)

        for key, val in self.Placket_segments.items():
            lbl_pos = self.middle(val[0], val[1])
            kwdic = {"color": "blue", "linestyle": "dashed", "alpha": 0.5}
            self.segment(val[0], val[1], ax, kwdic)
            angle = self.segment_angle(val[0], val[1]) * 180 / np.pi
            ax.text(lbl_pos.x, lbl_pos.y, key, rotation=angle)

        if save:

            of = (
                self.figPATH
                + "placket_"
                + self.style
                + "_"
                + self.pl
                + "_"
                + self.pname
                + "_FullSize.pdf"
            )

            plt.savefig(of)
