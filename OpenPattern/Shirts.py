#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

sys.path.append("./..")

from OpenPattern.Pattern import *
from OpenPattern.Points import *
from OpenPattern.Bodices import *


class Shirt(Basic_Bodice):
    """Shirt class inherits from bodice
    can be used to draw shirt dresses by ajusting the value of lower_lenght

    for now only Basinc_shirt method
    the method has to be called

    """

    def __init__(
        self,
        pname="M40mC",
        gender="m",
        style="Chiappetta",
        age=99,
        ease=0,
        lower_length=25,
        hip=False,
        Back_Front_space=12,
        collar_ease=1,
        sleeve_lowering=3,
        side_ease=4,
        shoulder_ease=1,
        button_overlap=2,
        **kwargs
    ):
        """Init for shirt

        :param pname: size key
        :param gender: gender
        :param stype: stylist
        :param age: age for Chiappetta kids
        :param ease: ease around bust
        :param lower_length: length of shirt from the waist
        :param hip: if true length of shirt is to the base of hip.
        :param Back_Front_space: distance between the two half patterns
        :param collar_ease: ease around neck !
        :param sleeve_lowering: ease of the armhole
        :param side_ease: ease to be applied to the side
        I need to check but beware this one is added to ease
        :param shoulder_ease: length added to shoulder length
        :param button_overlap: width of the button overlap band

        """

        Basic_Bodice.__init__(
            self,
            pname=pname,
            gender=gender,
            style=style,
            age=age,
            ease=ease,
            hip=hip,
            Back_Front_space=Back_Front_space,
            **kwargs
        )

        self.collar_ease = collar_ease
        self.sleeve_lowering = sleeve_lowering
        self.side_ease = side_ease
        self.shoulder_ease = shoulder_ease
        self.button_overlap = button_overlap
        self.lower_length = lower_length  # length from waist to shirt bottom

        #################################################
        # keep track of the original bodice
        #################################################
        Ori = self.copy()
        self.add_pattern(Ori)

    def basic_shirt_bodice(self, style="Chiappetta"):
        """transformation of the bodice into a shirt

        :param  style: stylist
        """
        if style == "Chiappetta":
            #################################################
            # Transformation of the Bodice
            #################################################

            # armhole
            self.Front_dic["ShF1"] += Point([self.shoulder_ease, 0.5])
            self.Front_dic["SlF1"] += Point([self.side_ease, -self.sleeve_lowering])
            self.Front_dic["BF1"] += Point([self.shoulder_ease, 0])

            aa = np.arctan(2.4 / 5.0) + np.pi / 2
            self.Front_dic["ClShF"] = self.Front_dic["ShF1"] + Point(
                [np.cos(aa) * 2, -np.sin(aa) * 2]
            )
            self.Front_dic["ClBF"] = self.Front_dic["BF1"] + Point([0, -1])

            if (self.Front_dic["ShF1"].x - self.Front_dic["BF1"].x) > 2:
                (
                    self.m["longueur_emmanchure_devant"],
                    self.front_sleeve_curve,
                ) = self.pistolet(
                    [
                        self.Front_dic["ShF1"],
                        self.Front_dic["ClShF"],
                        self.Front_dic["BF1"],
                        self.Front_dic["ClBF"],
                        self.Front_dic["SlF1"],
                    ],
                    3,
                    tot=True,
                )
            else:
                (
                    self.m["longueur_emmanchure_devant"],
                    self.front_sleeve_curve,
                ) = self.pistolet(
                    [
                        self.Front_dic["ShF1"],
                        self.Front_dic["BF1"],
                        self.Front_dic["SlF1"],
                    ],
                    2,
                    tot=True,
                )

            print("emmanchure devant", self.m["longueur_emmanchure_devant"])

            self.Back_dic["ShB1"] += Point([-self.shoulder_ease, 0.5])
            self.Back_dic["SlB1"] += Point([-self.side_ease, -self.sleeve_lowering])
            self.Back_dic["BB1"] += Point([-self.shoulder_ease, 0])

            bb = np.arctan(2 / 5) - np.pi / 2
            self.Back_dic["ClShB"] = self.Back_dic["ShB1"] + Point(
                [np.cos(bb) * 2, np.sin(bb) * 2]
            )
            self.Back_dic["ClBB"] = self.Back_dic["BB1"] + Point([0, -1])

            if (self.Back_dic["ShB1"].x - self.Back_dic["BB1"].x) < -2:
                (
                    self.m["longueur_emmanchure_dos"],
                    self.back_sleeve_curve,
                ) = self.pistolet(
                    [
                        self.Back_dic["ShB1"],
                        self.Back_dic["ClShB"],
                        self.Back_dic["BB1"],
                        self.Back_dic["ClBB"],
                        self.Back_dic["SlB1"],
                    ],
                    3,
                    tot=True,
                )
            else:
                (
                    self.m["longueur_emmanchure_dos"],
                    self.back_sleeve_curve,
                ) = self.pistolet(
                    [
                        self.Back_dic["ShB1"],
                        self.Back_dic["BB1"],
                        self.Back_dic["SlB1"],
                    ],
                    2,
                    tot=True,
                )
            print("emmanchure dos", self.m["longueur_emmanchure_dos"])

            # shirt's lower part
            self.Front_dic["HiF"] = self.Front_dic["WF"] + Point(
                [0, -self.lower_length]
            )
            self.Front_dic["HiF1"] = self.Front_dic["WF1"] + Point(
                [self.side_ease, -self.lower_length + 3]
            )
            self.Back_dic["HiB"] = self.Back_dic["WB"] + Point([0, -self.lower_length])
            self.Back_dic["HiB1"] = self.Back_dic["WB1"] + Point(
                [-self.side_ease, -self.lower_length + 3]
            )

            # Oh my god ! points with fixes values added... no good
            ClHiF = self.Front_dic["HiF"] + Point([4, 0])
            ClHiF1 = self.Front_dic["HiF1"] + Point([-3, 0])
            ClHiB = self.Back_dic["HiB"] + Point([-4, 0])
            ClHiB1 = self.Back_dic["HiB1"] + Point([3, 0])

            sfbc, self.front_base_curve = self.pistolet(
                [self.Front_dic["HiF"], ClHiF, ClHiF1, self.Front_dic["HiF1"]],
                3,
                tot=True,
            )
            sbbc, self.back_base_curve = self.pistolet(
                [self.Back_dic["HiB"], ClHiB, ClHiB1, self.Back_dic["HiB1"]],
                3,
                tot=True,
            )

            # move collar
            self.Front_dic["CF2"] += Point([-0.5, 0])
            self.Front_dic["ClCF"] += Point([-0.5, 0])

            self.m["longueur_col_devant"], self.front_collar_curve = self.pistolet(
                [self.Front_dic["CF"], self.Front_dic["ClCF"], self.Front_dic["CF2"]],
                2,
                tot=True,
            )
            self.m["longueur_col_dos"], self.back_collar_curve = self.pistolet(
                [self.Back_dic["HB"], self.Back_dic["ClCB"], self.Back_dic["CB2"]],
                2,
                tot=True,
            )

            self.Back_vertices = [
                [self.Back_dic["HiB"].pos(), self.Back_dic["HB"].pos()]
                + self.back_collar_curve
                + [self.Back_dic["ShB1"].pos()]
                + self.back_sleeve_curve
                + [self.Back_dic["HiB1"].pos()]
                + self.back_base_curve[::-1]
                + [self.Back_dic["HiB"].pos()]
            ]

            self.Front_vertices = [
                [self.Front_dic["HiF"].pos(), self.Front_dic["CF"].pos()]
                + self.front_collar_curve
                + [self.Front_dic["ShF1"].pos()]
                + self.front_sleeve_curve
                + [self.Front_dic["HiF1"].pos()]
                + self.front_base_curve[::-1]
                + [self.Front_dic["HiF"].pos()]
            ]

            # add the button overlap
            TB1 = self.Front_dic["CF"] + Point([-self.button_overlap, 0])
            TB2 = self.Front_dic["HiF"] + Point([-self.button_overlap, 0])

            overlap = [
                self.Front_dic["HiF"].pos(),
                self.Front_dic["CF"].pos(),
                TB1.pos(),
                TB2.pos(),
                self.Front_dic["HiF"].pos(),
            ]
            self.Front_vertices.append(overlap)

            # parure
            # 2x2cm
            P1 = TB1 + Point([-2, 0])
            P2 = TB2 + Point([-2, 0])
            parure = [TB2.pos(), TB1.pos(), P1.pos(), P2.pos(), TB2.pos()]
            self.Front_vertices.append(parure)

            # second parure
            PL1 = P1 + Point([-2, 0])
            PL2 = P2 + Point([-2, 0])
            sparure = [P2.pos(), P1.pos(), PL1.pos(), PL2.pos(), P2.pos()]
            self.Front_vertices.append(sparure)

        elif style == "Gilewska":
            #################################################
            # Transformation of the Bodice
            #################################################

            # armhole
            fsh_a = self.segment_angle(self.Front_dic["CF2"], self.Front_dic["ShF1"])
            self.Front_dic["ShF1"] += Point(
                [
                    (self.shoulder_ease + 1) * np.cos(fsh_a),
                    (self.shoulder_ease + 1) * np.sin(fsh_a),
                ]
            )
            self.Front_dic["SlF1"] += Point([self.side_ease, -self.sleeve_lowering])
            self.Front_dic["BF1"] += Point([self.shoulder_ease + 1, 0])

            aa = fsh_a + np.pi / 2
            self.Front_dic["ClShF"] = self.Front_dic["ShF1"] + Point(
                [-np.cos(aa) * 2, -np.sin(aa) * 2]
            )
            self.Front_dic["ClBF"] = self.Front_dic["BF1"] + Point([0, -1])

            if (self.Front_dic["ShF1"].x - self.Front_dic["BF1"].x) > 2:
                (
                    self.m["longueur_emmanchure_devant"],
                    self.front_sleeve_curve,
                ) = self.pistolet(
                    [
                        self.Front_dic["ShF1"],
                        self.Front_dic["ClShF"],
                        self.Front_dic["BF1"],
                        self.Front_dic["ClBF"],
                        self.Front_dic["SlF1"],
                    ],
                    3,
                    tot=True,
                )
            else:
                (
                    self.m["longueur_emmanchure_devant"],
                    self.front_sleeve_curve,
                ) = self.pistolet(
                    [
                        self.Front_dic["ShF1"],
                        self.Front_dic["BF1"],
                        self.Front_dic["SlF1"],
                    ],
                    2,
                    tot=True,
                )

            bsh_a = self.segment_angle(self.Back_dic["ShB1"], self.Back_dic["CB2"])
            self.Back_dic["ShB1"] += Point(
                [
                    -(self.shoulder_ease + 1) * np.cos(bsh_a),
                    -(self.shoulder_ease + 1) * np.sin(bsh_a),
                ]
            )
            self.Back_dic["SlB1"] += Point([-self.side_ease, -self.sleeve_lowering])
            self.Back_dic["BB1"] += Point([-self.shoulder_ease - 1, 0])

            bb = bsh_a - np.pi / 2
            self.Back_dic["ClShB"] = self.Back_dic["ShB1"] + Point(
                [np.cos(bb) * 2, np.sin(bb) * 2]
            )
            self.Back_dic["ClBB"] = self.Back_dic["BB1"] + Point([0, -1])

            if (self.Back_dic["ShB1"].x - self.Back_dic["BB1"].x) < -2:
                (
                    self.m["longueur_emmanchure_dos"],
                    self.back_sleeve_curve,
                ) = self.pistolet(
                    [
                        self.Back_dic["ShB1"],
                        self.Back_dic["ClShB"],
                        self.Back_dic["BB1"],
                        self.Back_dic["ClBB"],
                        self.Back_dic["SlB1"],
                    ],
                    3,
                    tot=True,
                )
            else:
                (
                    self.m["longueur_emmanchure_dos"],
                    self.back_sleeve_curve,
                ) = self.pistolet(
                    [
                        self.Back_dic["ShB1"],
                        self.Back_dic["BB1"],
                        self.Back_dic["SlB1"],
                    ],
                    2,
                    tot=True,
                )

            # shirt's lower part
            self.Front_dic["HiF"] = self.Front_dic["WF"] + Point(
                [0, -self.lower_length]
            )
            self.Front_dic["HiF1"] = self.Front_dic["WF1"] + Point(
                [self.side_ease, -self.lower_length + 10]
            )
            self.Back_dic["HiB"] = self.Back_dic["WB"] + Point([0, -self.lower_length])
            self.Back_dic["HiB1"] = self.Back_dic["WB1"] + Point(
                [-self.side_ease, -self.lower_length + 10]
            )

            ClHiF = self.Front_dic["HiF"] + Point([4, 0])
            ClHiF1 = self.Front_dic["HiF1"] + Point([-3, 0])
            ClHiB = self.Back_dic["HiB"] + Point([-4, 0])
            ClHiB1 = self.Back_dic["HiB1"] + Point([3, 0])

            sfbc, self.front_base_curve = self.pistolet(
                [self.Front_dic["HiF"], ClHiF, ClHiF1, self.Front_dic["HiF1"]],
                3,
                tot=True,
            )
            sbbc, self.back_base_curve = self.pistolet(
                [self.Back_dic["HiB"], ClHiB, ClHiB1, self.Back_dic["HiB1"]],
                3,
                tot=True,
            )

            # move collar
            self.Front_dic["CF2"] += Point([np.cos(fsh_a), np.sin(fsh_a)])
            self.Front_dic["ClCF"] += Point([np.cos(fsh_a), np.sin(fsh_a)])
            self.Front_dic["CF"] += Point([0, -1])

            self.m["longueur_col_devant"], self.front_collar_curve = self.pistolet(
                [self.Front_dic["CF"], self.Front_dic["ClCF"], self.Front_dic["CF2"]],
                2,
                tot=True,
            )

            self.Back_dic["CB2"] += Point([-np.cos(bsh_a), -np.sin(bsh_a)])
            self.Back_dic["ClCB"] += Point([-np.cos(bsh_a), -np.sin(bsh_a)])
            self.Back_dic["HB"] += Point([0, -1])
            self.m["longueur_col_dos"], self.back_collar_curve = self.pistolet(
                [self.Back_dic["HB"], self.Back_dic["ClCB"], self.Back_dic["CB2"]],
                2,
                tot=True,
            )

            self.Back_vertices = [
                [self.Back_dic["HiB"].pos(), self.Back_dic["HB"].pos()]
                + self.back_collar_curve
                + [self.Back_dic["ShB1"].pos()]
                + self.back_sleeve_curve
                + [self.Back_dic["HiB1"].pos()]
                + self.back_base_curve[::-1]
                + [self.Back_dic["HiB"].pos()]
            ]

            self.Front_vertices = [
                [self.Front_dic["HiF"].pos(), self.Front_dic["CF"].pos()]
                + self.front_collar_curve
                + [self.Front_dic["ShF1"].pos()]
                + self.front_sleeve_curve
                + [self.Front_dic["HiF1"].pos()]
                + self.front_base_curve[::-1]
                + [self.Front_dic["HiF"].pos()]
            ]

            # add the button overlap
            TB1 = self.Front_dic["CF"] + Point([-self.button_overlap, 0])
            TB2 = self.Front_dic["HiF"] + Point([-self.button_overlap, 0])

            overlap = [
                self.Front_dic["HiF"].pos(),
                self.Front_dic["CF"].pos(),
                TB1.pos(),
                TB2.pos(),
                self.Front_dic["HiF"].pos(),
            ]
            self.Front_vertices.append(overlap)

            # parure
            # 2x2 cm
            P1 = TB1 + Point([-2, 0])
            P2 = TB2 + Point([-2, 0])
            parure = [TB2.pos(), TB1.pos(), P1.pos(), P2.pos(), TB2.pos()]
            self.Front_vertices.append(parure)

            # second "parure"
            PL1 = P1 + Point([-2, 0])
            PL2 = P2 + Point([-2, 0])
            sparure = [P2.pos(), P1.pos(), PL1.pos(), PL2.pos(), P2.pos()]
            self.Front_vertices.append(sparure)

        print("################")
        print("longueurs col")
        print("devant = %f" % (self.m["longueur_col_devant"]))
        print("dos = %f" % (self.m["longueur_col_dos"]))
        print("################")
        print("emmanchures")
        print("emmanchure devant", self.m["longueur_emmanchure_devant"])
        print("emmanchure dos", self.m["longueur_emmanchure_dos"])

        self.save_measurements_sql()

    def yoked_shirt_bodice(self):
        """yoked shirt but not finished..."""

        if self.style == "Chiappetta":
            # Transformation of the Bodice

            # Front
            self.Front_dic["ShF1"] += Point([self.shoulder_ease, 0.5])
            self.Front_dic["SlF1"] += Point([self.side_ease, -self.sleeve_lowering])
            self.Front_dic["BF1"] += Point([self.shoulder_ease, 0])

            aa = np.arctan(2.4 / 5.0) + np.pi / 2
            self.Front_dic["ClShF"] = self.Front_dic["ShF1"] + Point(
                [np.cos(aa) * 2, -np.sin(aa) * 2]
            )
            self.Front_dic["ClBF"] = self.Front_dic["BF1"] + Point([0, -1])

            (
                self.m["longueur_emmanchure_devant"],
                self.front_sleeve_curve,
            ) = self.pistolet(
                [
                    self.Front_dic["ShF1"],
                    self.Front_dic["ClShF"],
                    self.Front_dic["BF1"],
                    self.Front_dic["ClBF"],
                    self.Front_dic["SlF1"],
                ],
                3,
                tot=True,
            )
            print("emmanchure devant", self.m["longueur_emmanchure_devant"])

            # move collar
            self.Front_dic["CF2"] += Point([-0.5, 0])
            self.Front_dic["ClCF"] += Point([-0.5, 0])

            # redraw collar
            self.m["longueur_col_devant"], self.front_collar_curve = self.pistolet(
                [self.Front_dic["CF"], self.Front_dic["ClCF"], self.Front_dic["CF2"]],
                2,
                tot=True,
            )

            l_sl = self.distance(self.Front_dic["CF2"], self.Front_dic["ShF1"])

            # Back

            TmpSh = self.Back_dic["ShB1"] + Point([0, 0.5])
            a = self.segment_angle(TmpSh, self.Back_dic["CB2"])
            self.Back_dic["ShB1"] = self.Back_dic["CB2"] + Point(
                [-l_sl * np.cos(a), -l_sl * np.sin(a)]
            )

            self.Back_dic["SlB1"] += Point([-self.side_ease, -self.sleeve_lowering])

            self.Back_dic["BB1"] += Point([self.Back_dic["ShB1"].x - TmpSh.x, 0])

            bb = np.arctan(2 / 5) - np.pi / 2
            self.Back_dic["ClShB"] = self.Back_dic["ShB1"] + Point(
                [np.cos(bb) * 2, np.sin(bb) * 2]
            )
            self.Back_dic["ClBB"] = self.Back_dic["BB1"] + Point([0, -1])

            self.m["longueur_emmanchure_dos"], self.back_sleeve_curve = self.pistolet(
                [
                    self.Back_dic["ShB1"],
                    self.Back_dic["ClShB"],
                    self.Back_dic["BB1"],
                    self.Back_dic["ClBB"],
                    self.Back_dic["SlB1"],
                ],
                3,
                tot=True,
            )
            print("emmanchure dos", self.m["longueur_emmanchure_dos"])

            # shirt's lower part
            self.Front_dic["HiF"] = self.Front_dic["WF"] + Point(
                [0, -self.m["montant"]]
            )
            self.Front_dic["HiF1"] = self.Front_dic["WF1"] + Point(
                [self.side_ease, -self.m["montant"] + 10]
            )
            self.Back_dic["HiB"] = self.Back_dic["WB"] + Point([0, -self.m["montant"]])
            self.Back_dic["HiB1"] = self.Back_dic["WB1"] + Point(
                [-self.side_ease, -self.m["montant"] + 10]
            )

            ClHiF = self.Front_dic["HiF"] + Point([4, 0])
            ClHiF1 = self.Front_dic["HiF1"] + Point([-3, 0])
            ClHiB = self.Back_dic["HiB"] + Point([-4, 0])
            ClHiB1 = self.Back_dic["HiB1"] + Point([3, 0])

            sfbc, self.front_base_curve = self.pistolet(
                [self.Front_dic["HiF"], ClHiF, ClHiF1, self.Front_dic["HiF1"]],
                3,
                tot=True,
            )
            sbbc, self.back_base_curve = self.pistolet(
                [self.Back_dic["HiB"], ClHiB, ClHiB1, self.Back_dic["HiB1"]],
                3,
                tot=True,
            )

            # self.m['longueur_col_dos'], self.back_collar_curve = self.pistolet([HB,ClCB,CB2], 2, tot = True)

            # locate yoke Points for front and cut
            d = 0
            c_sl = 0
            yoke_sl = [copy(self.front_sleeve_curve[0])]
            N = len(self.front_sleeve_curve) - 1
            for i in range(N):
                if d < 3.5:
                    d += self.distance(
                        Point(self.front_sleeve_curve[i]),
                        Point(self.front_sleeve_curve[i + 1]),
                    )
                    yoke_sl.append(copy(self.front_sleeve_curve[i + 1]))
                    YFSl = Point(self.front_sleeve_curve[i + 1])  # Yoke Front Sleeve
                    c_sl += 1

            print(d, c_sl, N)
            self.Front_dic["YFSl"] = YFSl

            d = 0
            N = len(self.front_collar_curve) - 1
            c_cl = N
            yoke_cl = [copy(self.front_collar_curve[N])]
            for i in range(N):
                if d < 2.5:
                    d += self.distance(
                        Point(self.front_collar_curve[N - i]),
                        Point(self.front_collar_curve[N - i - 1]),
                    )
                    yoke_cl.append(copy(self.front_collar_curve[N - i - 1]))
                    YFCl = Point(
                        self.front_collar_curve[N - i - 1]
                    )  # Yoke Front Sleeve
                    c_cl -= 1

            print(d, c_cl, N)
            self.Front_dic["YFCl"] = YFCl

            # create yoke
            self.front_yoke = (
                [YFCl.pos()] + yoke_cl[::-1] + yoke_sl + [YFSl.pos(), YFCl.pos()]
            )

            # translate and rotate yoke
            dx = self.Back_dic["ShB1"].x - self.Front_dic["ShF1"].x
            dy = self.Back_dic["ShB1"].y - self.Front_dic["ShF1"].y
            for i in range(len(self.front_yoke)):
                self.front_yoke[i][0] += dx
                self.front_yoke[i][1] += dy

            a1 = self.oriented_segment_angle(
                self.Front_dic["ShF1"], self.Front_dic["CF2"]
            )
            a2 = self.oriented_segment_angle(
                self.Back_dic["ShB1"], self.Back_dic["CB2"]
            )

            print(a1, a2)
            theta = a1 - a2
            tmp_list = []
            for p in self.front_yoke:
                Pt = Point(p)
                Pt.rotate(self.Back_dic["ShB1"], -theta, "rad")
                tmp_list.append(Pt.pos())

            self.front_yoke = tmp_list

            self.Back_vertices = [
                [self.Back_dic["HiB"].pos(), self.Back_dic["HB"].pos()]
                + self.back_collar_curve
                + [self.Back_dic["ShB1"].pos()]
                + self.back_sleeve_curve
                + [self.Back_dic["HiB1"].pos()]
                + self.back_base_curve[::-1]
                + [self.Back_dic["HiB"].pos()]
            ]

            self.Front_vertices = [
                [self.Front_dic["HiF"].pos(), self.Front_dic["CF"].pos()]
                + self.front_collar_curve[0:c_cl]
                + self.front_sleeve_curve[c_sl:]
                + [self.Front_dic["HiF1"].pos()]
                + self.front_base_curve[::-1]
                + [self.Front_dic["HiF"].pos()]
            ]

            # add the button overlap
            TB1 = self.Front_dic["CF"] + Point([-1.5, 0])
            TB2 = self.Front_dic["HiF"] + Point([-1.5, 0])

            overlap = [
                self.Front_dic["HiF"].pos(),
                self.Front_dic["CF"].pos(),
                TB1.pos(),
                TB2.pos(),
                self.Front_dic["HiF"].pos(),
            ]
            self.Front_vertices.append(overlap)

            # parure
            P1 = TB1 + Point([-2, 0])
            P2 = TB2 + Point([-2, 0])
            parure = [TB2.pos(), TB1.pos(), P1.pos(), P2.pos(), TB2.pos()]
            self.Front_vertices.append(parure)

            # second parure
            PL1 = P1 + Point([-2, 0])
            PL2 = P2 + Point([-2, 0])
            sparure = [P2.pos(), P1.pos(), PL1.pos(), PL2.pos(), P2.pos()]
            self.Front_vertices.append(sparure)

            self.Front_vertices.append(self.front_yoke)

            self.save_measurements_sql()
