#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

sys.path.append("./..")

from OpenPattern.Pattern import *
from OpenPattern.Points import *
from OpenPattern.Bodices import *
from copy import copy, deepcopy


class Waist_Coat(Basic_Bodice):
    """
    first test for alteration capacities of my pattern system.
    its hard !

    """

    def __init__(
        self,
        pname="M44G",
        gender="m",
        style="Gilewska",
        age=12,
        ease=8,
        wc_style="Classical",
        overlap=False,
        **kwargs
    ):

        Basic_Bodice.__init__(
            self, pname, gender, style, age, ease, hip=False, **kwargs
        )

        self.wc_style = wc_style
        self.overlap = overlap

        self.cal_wc()

    def cal_wc(self):
        """
        define the style

        calculate the Bodice
        define the movement of points
        le faire à la main et ensuite passer
        au calcul

        """
        if self.wc_style == "Classical":

            BB = deepcopy(self.Back_dic)
            BF = deepcopy(self.Front_dic)

            # ease
            BB["SlB1"] = BB["SlB1"] + [2, -7]
            BF["SlF1"] = BF["SlF1"] + [-2, -7]

            # shoulders
            a = self.segment_angle(BB["CB1"], BB["ShB1"])
            BB["CB1"] = BB["CB1"] + [3 * np.cos(a), 3 * np.sin(a)]

            d = 7  # between 7 and 9
            BB["ShB1"] = BB["CB1"] + [d * np.cos(a), d * np.sin(a)]

            b = self.segment_angle(BF["CF1"], BF["ShF1"])
            BF["CF1"] = BF["CF1"] + [-3 * np.cos(b), -3 * np.sin(b)]
            BF["ShF1"] = BF["CF1"] + [-d * np.cos(b), -d * np.sin(b)]

            CPF = BF["SlF1"] + [2, 0]
            l_emmanchure_dev, sleeve_front_points = self.pistolet(
                [BF["ShF1"], CPF, BF["SlF1"]], 2, tot=True
            )

            CPB = BB["SlB1"] + [-2, 0]
            l_emmanchure_dos, sleeve_back_points = self.pistolet(
                [BB["ShB1"], CPB, BB["SlB1"]], 2, tot=True
            )

            # collars
            BB["HB"] = BB["HB"] + [0, -2]
            collar_CP = BB["HB"] + [1, 0]

            l_collar, collar_back_points = self.pistolet(
                [BB["HB"], collar_CP, BB["CB1"]], 2, tot=True
            )

            croisure = 2
            BF["CF"] = BF["CF"] + [croisure, (BF["SlF1"].y + 1) - BF["CF"].y]

            # Hip line
            hwc = 5  # between 5 and 7
            BB["HipB1"] = BB["WB1"] + [2, -hwc]
            BB["HipB"] = BB["WB"] + [0.5, -hwc]
            BF["HipF1"] = BF["WF1"] + [-2, -hwc]

            # waist
            BF["WF1"] = BF["WF1"] + [-1, 0]
            BF["WF"] = BF["WF"] + [croisure, 0]
            BB["WB1"] = BB["WB1"] + [0.5, 0]

            # Front tip
            BF["TipF"] = BF["WF"] + [-6, -hwc - 4]

            # darts
            PwF = BF["WF"] + [-self.m["tour_poitrine"] / 8, -hwc]
            PwFr = PwF + [1, 0]
            PwFl = PwF + [-1, 0]
            BF["OPwF"] = PwF + [0, 15]
            # find the intersection with the hip front line
            BF["PwFl"] = self.intersec_lines(BF["OPwF"], PwFl, BF["TipF"], BF["HipF1"])
            BF["PwFr"] = self.intersec_lines(BF["OPwF"], PwFr, BF["TipF"], BF["HipF1"])

            # patte de serrage dos
            BB["PSB"] = BB["WB"] + [15, 0]

            # Pockets
            BF["UPr"] = BF["SlF"] + [-6, 0]
            BF["UPl"] = BF["SlF"] + [-14, 1.5]

            BF["WPr"] = BF["WF"] + [-8, 0]
            BF["WPl"] = BF["WF"] + [-20, 1.5 * (12 / 8)]

            # do some cleaning
            del BF["CPCF"]
            del BB["HB1"]
            del BF["HF1"]
            del BB["BB1"]
            del BF["BF1"]
            del BB["CPSlB"]
            del BF["CPSlF"]

            """
			the use of self.overlap enables to stack patterns in order to see the difference between an original and an altered pattern
			for example waistcoat on top of basic bodice
			"""
            if self.overlap:
                self.dic_list = [BF, BB]

                self.vertices_list.append(
                    [
                        BF["TipF"].pos(),
                        BF["WF"].pos(),
                        BF["CF"].pos(),
                        BF["CF1"].pos(),
                        BF["ShF1"].pos(),
                    ]
                    + sleeve_front_points
                    + [
                        BF["WF1"].pos(),
                        BF["HipF1"].pos(),
                        BF["PwFl"].pos(),
                        BF["OPwF"].pos(),
                        BF["PwFr"].pos(),
                    ]
                )
                self.vertices_list.append(
                    [BB["HipB"].pos(), BB["SlB"].pos(), BB["HB"].pos()]
                    + collar_back_points
                    + sleeve_back_points
                    + [BB["WB1"].pos(), BB["HipB1"].pos()]
                )

            else:

                self.Back_dic = BB
                self.Front_dic = BF
                self.dic_list = [BF, BB]

                self.Front_vertices = (
                    [
                        BF["TipF"].pos(),
                        BF["WF"].pos(),
                        BF["CF"].pos(),
                        BF["CF1"].pos(),
                        BF["ShF1"].pos(),
                    ]
                    + sleeve_front_points
                    + [
                        BF["WF1"].pos(),
                        BF["HipF1"].pos(),
                        BF["PwFl"].pos(),
                        BF["OPwF"].pos(),
                        BF["PwFr"].pos(),
                    ]
                )

                self.Back_vertices = (
                    [BB["HipB"].pos(), BB["SlB"].pos(), BB["HB"].pos()]
                    + collar_back_points
                    + sleeve_back_points
                    + [BB["WB1"].pos(), BB["HipB1"].pos()]
                )

                self.vertices_list = [
                    self.Front_vertices,
                    self.Back_vertices,
                ]

            self.draw_bodice(dic={"Pattern": "Classical Waistcoat"})

    def add_legends(self, ax):
        """Adds common legends to the Bodice pattern

        Args:
                ax on which to plot

        Returns:
                ax

        This method is overloaded As some legends to change. There is probably a means to escape overloading
        """

        bfd = self.dic_list[0]
        bbd = self.dic_list[1]

        fs = 14
        ldic = {"color": "blue", "alpha": 0.4, "linestyle": "dashed"}

        pos = self.middle(bbd["WB"], bbd["SlB"])
        ax.text(pos.x + 0.5, pos.y, "FOLD LINE", fontsize=fs, rotation=90)

        pos = self.middle(bfd["WF"], bfd["SlF"])
        ax.text(pos.x - 0.5, pos.y, "OVERLAP", fontsize=fs, rotation=90)

        pos = self.middle(bfd["HF"], bfd["TipF"] + [4, 0])
        self.segment(bfd["HF"], bfd["TipF"] + [4, 0], ax, ldic)
        ax.text(pos.x - 1.5, pos.y + 10, "MIDDLE FRONT", fontsize=fs, rotation=90)

        self.segment(bfd["WF"], bbd["WB"], ax, ldic)
        pos = self.middle(bfd["WF"], bbd["WB"])
        ax.text(pos.x, pos.y + 0.5, "WAIST LINE", fontsize=fs, ha="center")

        self.segment(bfd["SlF"], bbd["SlB"], ax, ldic)
        pos = self.middle(bfd["SlF"], bbd["SlB"])
        ax.text(pos.x, pos.y + 0.5, "SLEEVE LINE", fontsize=fs, ha="center")

        self.segment(bfd["BF"], bbd["BB"], ax, ldic)
        pos = self.middle(bfd["BF"], bbd["BB"])
        ax.text(pos.x, pos.y + 0.5, "BUST LINE", fontsize=fs, ha="center")

        return ax
