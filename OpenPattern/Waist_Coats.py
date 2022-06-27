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

            BB = deepcopy(self.Bodice_points_dic)

            # ease
            BB["SlB1"] = BB["SlB1"] + [2, -7]
            BB["SlF1"] = BB["SlF1"] + [-2, -7]

            # shoulders
            a = self.segment_angle(BB["CB1"], BB["ShB1"])
            BB["CB1"] = BB["CB1"] + [3 * np.cos(a), 3 * np.sin(a)]

            d = 7  # between 7 and 9
            BB["ShB1"] = BB["CB1"] + [d * np.cos(a), d * np.sin(a)]

            b = self.segment_angle(BB["CF1"], BB["ShF1"])
            BB["CF1"] = BB["CF1"] + [-3 * np.cos(b), -3 * np.sin(b)]
            BB["ShF1"] = BB["CF1"] + [-d * np.cos(b), -d * np.sin(b)]

            CPF = BB["SlF1"] + [2, 0]
            l_emmanchure_dev, sleeve_front_points = self.pistolet(
                [BB["ShF1"], CPF, BB["SlF1"]], 2, tot=True
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
            BB["CF"] = BB["CF"] + [croisure, (BB["SlF1"].y + 1) - BB["CF"].y]

            # Hip line
            hwc = 5  # between 5 and 7
            BB["HipB1"] = BB["WB1"] + [2, -hwc]
            BB["HipB"] = BB["WB"] + [0.5, -hwc]
            BB["HipF1"] = BB["WF1"] + [-2, -hwc]

            # waist
            BB["WF1"] = BB["WF1"] + [-1, 0]
            BB["WF"] = BB["WF"] + [croisure, 0]
            BB["WB1"] = BB["WB1"] + [0.5, 0]

            # Front tip
            BB["TipF"] = BB["WF"] + [-6, -hwc - 4]

            # darts
            PwF = BB["WF"] + [-self.m["tour_poitrine"] / 8, -hwc]
            PwFr = PwF + [1, 0]
            PwFl = PwF + [-1, 0]
            BB["OPwF"] = PwF + [0, 15]
            # find the intersection with the hip front line
            BB["PwFl"] = self.intersec_lines(BB["OPwF"], PwFl, BB["TipF"], BB["HipF1"])
            BB["PwFr"] = self.intersec_lines(BB["OPwF"], PwFr, BB["TipF"], BB["HipF1"])

            # patte de serrage dos
            BB["PSB"] = BB["WB"] + [15, 0]

            # Pockets
            BB["UPr"] = BB["SlF"] + [-6, 0]
            BB["UPl"] = BB["SlF"] + [-14, 1.5]

            BB["WPr"] = BB["WF"] + [-8, 0]
            BB["WPl"] = BB["WF"] + [-20, 1.5 * (12 / 8)]

            # do some cleaning
            del BB["CPCF"]
            del BB["HB1"]
            del BB["HF1"]
            del BB["BB1"]
            del BB["BF1"]
            del BB["CPSlB"]
            del BB["CPSlF"]

            """
			the use of self.overlap enables to stack patterns in order to see the difference between an original and an altered pattern
			for example waistcoat on top of basic bodice
			"""
            if self.overlap:
                self.dic_list.append(BB)

                self.vertices_list.append(
                    [
                        BB["TipF"].pos(),
                        BB["WF"].pos(),
                        BB["CF"].pos(),
                        BB["CF1"].pos(),
                        BB["ShF1"].pos(),
                    ]
                    + sleeve_front_points
                    + [
                        BB["WF1"].pos(),
                        BB["HipF1"].pos(),
                        BB["PwFl"].pos(),
                        BB["OPwF"].pos(),
                        BB["PwFr"].pos(),
                    ]
                )
                self.vertices_list.append(
                    [BB["HipB"].pos(), BB["SlB"].pos(), BB["HB"].pos()]
                    + collar_back_points
                    + sleeve_back_points
                    + [BB["WB1"].pos(), BB["HipB1"].pos()]
                )

            else:

                self.Bodice_points_dic = BB
                self.dic_list = [BB]

                self.Bodice_Front_vertices = (
                    [
                        BB["TipF"].pos(),
                        BB["WF"].pos(),
                        BB["CF"].pos(),
                        BB["CF1"].pos(),
                        BB["ShF1"].pos(),
                    ]
                    + sleeve_front_points
                    + [
                        BB["WF1"].pos(),
                        BB["HipF1"].pos(),
                        BB["PwFl"].pos(),
                        BB["OPwF"].pos(),
                        BB["PwFr"].pos(),
                    ]
                )

                self.Bodice_Back_vertices = (
                    [BB["HipB"].pos(), BB["SlB"].pos(), BB["HB"].pos()]
                    + collar_back_points
                    + sleeve_back_points
                    + [BB["WB1"].pos(), BB["HipB1"].pos()]
                )

                self.dic_list = [BB]
                self.vertices_list = [
                    self.Bodice_Front_vertices,
                    self.Bodice_Back_vertices,
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

        if len(self.dic_list) > 1:
            bpd = self.dic_list[1]
        else:
            bpd = self.dic_list[0]
        fs = 14
        ldic = {"color": "blue", "alpha": 0.4, "linestyle": "dashed"}

        pos = self.middle(bpd["WB"], bpd["SlB"])
        ax.text(pos.x + 0.5, pos.y, "FOLD LINE", fontsize=fs, rotation=90)

        pos = self.middle(bpd["WF"], bpd["SlF"])
        ax.text(pos.x - 0.5, pos.y, "OVERLAP", fontsize=fs, rotation=90)

        pos = self.middle(bpd["HF"], bpd["TipF"] + [4, 0])
        self.segment(bpd["HF"], bpd["TipF"] + [4, 0], ax, ldic)
        ax.text(pos.x - 1.5, pos.y + 10, "MIDDLE FRONT", fontsize=fs, rotation=90)

        self.segment(bpd["WF"], bpd["WB"], ax, ldic)
        pos = self.middle(bpd["WF"], bpd["WB"])
        ax.text(pos.x, pos.y + 0.5, "WAIST LINE", fontsize=fs, ha="center")

        self.segment(bpd["SlF"], bpd["SlB"], ax, ldic)
        pos = self.middle(bpd["SlF"], bpd["SlB"])
        ax.text(pos.x, pos.y + 0.5, "SLEEVE LINE", fontsize=fs, ha="center")

        self.segment(bpd["BF"], bpd["BB"], ax, ldic)
        pos = self.middle(bpd["BF"], bpd["BB"])
        ax.text(pos.x, pos.y + 0.5, "BUST LINE", fontsize=fs, ha="center")

        return ax
