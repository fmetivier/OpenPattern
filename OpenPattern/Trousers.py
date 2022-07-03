#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

sys.path.append("./..")

from OpenPattern.Pattern import *
from OpenPattern.Points import *

###############################################################
# Basic Trousers templates
# from different stylists Donnanno, Gilewska
###############################################################


class Basic_Trousers(Pattern):
    """
    Class used to calculate the pattern of basic trousers
    Inherits from Pattern

    Attributes:
            # dics used here for pattern construction points and labels:
            Back_dic
            Front_dic

            # lists of vertices to draw pattern curves:
            Back_vertices
            Front_vertices

            # list of points to be used for alterations
            Trousers_Front_Contour_list
            Trousers_Back_Contour_list

            # curves obtained from spline interpolation:
            # SORRY IT'S IN FRENCH
            fourche_arriere
            interieur_arriere
            exterieur_arriere
            fourche_avant
            interieur_avant
            exterieur_avant
            ceinture_avant

    """

    ############################################################
    def __init__(
        self,
        pname="M44D",
        gender="m",
        style="Donnanno",
        darts=False,
        wfd=None,
        **kwargs
    ):
        """
        Class initialisation. Launches trouser calculation

        """
        Pattern.__init__(self, pname, gender, **kwargs)

        if self.gender == "m":
            self.ease = 0
        else:
            self.ease = 2

        self.style = style
        self.darts = darts
        if wfd:
            self.wfd = wfd  # a dictionnary that contains the adjustements
        else:
            self.wfd = {
                "sides": 0,
                "center_front": 0,
                "front_left": 0,
                "front_right": 0,
                "center_back": 0,
                "back": 0,
            }

        self.Back_dic = {}
        self.Front_dic = {}

        self.Trousers_Front_Contour_list = []
        self.Trousers_Back_Contour_list = []

        # some issues with measurements
        if "longueur_tot" in self.m:
            pass
        else:
            if "hauteur_taille_terre" in self.m:
                self.m["longueur_tot"] = self.m["hauteur_taille_terre"]
            elif "longueur_taille_terre" in self.m:
                self.m["longueur_tot"] = self.m["longueur_taille_terre"]

        if self.style == "Donnanno":
            print("style Donnanno selected")
            self.Donnanno_front_trousers()
            self.Donnanno_back_trousers()
            if self.darts == True:
                self.Donnanno_add_darts()

        else:
            print("style %s unknown, using Donnanno instead" % (self.style))
            self.Donnanno_front_trousers()
            self.Donnanno_back_trousers()

    ############################################################
    def Donnanno_front_trousers(self):
        """
        Calculate front Trousers' pattern
        Essentially the same for women and men with some slight differences
        """

        # Front frame

        A = Point([0, self.m["longueur_tot"]])
        B = Point([self.m["tour_bassin"] / 4, self.m["longueur_tot"]])
        C = Point([0, 0])
        D = Point([B.x, 0])

        # crotch and hip lines
        E = Point([0, A.y - self.m["montant"]])
        F = Point([B.x, E.y])
        G = A - [0, self.m["hauteur_bassin"]]
        H = Point([B.x, G.y])

        if self.gender == "m":
            E1 = E - [self.m["tour_bassin"] / 20, 0]
        else:
            E1 = E - [self.m["tour_bassin"] / 16 - 1.5, 0]

        # connect and fold lines
        I = E - [0, self.m["montant"]]
        L = Point([B.x, I.y])

        # fold line
        X = Point([0.5 * (E1.x + F.x), E1.y])
        N = Point([X.x, C.y])
        X1 = Point([X.x, I.y])

        # comments regarding M:
        # point A1  and dart vertical positioning are not detailed
        # in Donnanno's book so I had to guess them empirically for the fit !
        # Hence the points Mbis...

        M = Point([X.x, A.y])

        # dart position
        if self.gender == "m":
            Mbis = Point([X.x, A.y - 0.5])  # don't ask me where I got this from !
            M2 = Mbis + [6, 0]
            L1 = X1 + [12.5, 0]
            I1 = X1 - [12.5, 0]
            N1 = N + [0, 1.5]
            A1 = A + [1 + self.wfd["center_front"], 0]
        else:
            if self.darts == True:
                A1 = A + [0 + self.wfd["center_front"], -1]
                B1 = B + [-1 - self.wfd["sides"], 0]
                Mbis = Point(
                    [X.x, A.y - 0.9]
                )  # adaptation pour la femme # same question
                M2 = Mbis + [7, +0.2]
            else:
                A1 = A + [0.5 + self.wfd["center_front"], -0.5]
                B1 = B + [-3 - self.wfd["sides"], 0]
                Mbis = Point(
                    [X.x, A.y - 0.7]
                )  # adaptation pour la femme # same question

            L1 = X1 + [12, 0]
            I1 = X1 - [12, 0]
            N1 = N + [0, 1]

        C1 = N - [11, 0]
        D1 = N + [11, 0]

        # knee
        O = Point([X.x, M.y - self.m["hauteur_taille_genou"]])

        # points en plus
        E1G = Point(
            [E.x + (E1.x - E.x) / 5, E.y + (G.y - E.y) / 3]
        )  # permet une jolie courbe de fourche avant

        ONC1 = C1 + [0, 10]  # permettent un tombé droit sous le genou.
        OND1 = D1 + [0, 10]

        dfa, self.fourche_avant = self.pistolet(np.array([E1, E1G, G]), 2, tot=True)
        dia, self.interieur_avant = self.pistolet(
            np.array([C1, ONC1, I1, E1]), 3, tot=True
        )

        if self.gender == "m":
            dha, self.ceinture_avant = self.pistolet(
                np.array([A1, Mbis, M2, B]), 2, tot=True
            )
            print("Front waist = " + str(dha))
            Front_Points_Names = [
                "A",
                "B",
                "C",
                "D",
                "E",
                "F",
                "G",
                "H",
                "E1",
                "I",
                "L",
                "X",
                "M",
                "Mbis",
                "N",
                "O",
                "M2",
                "X1",
                "L1",
                "I1",
                "N1",
                "C1",
                "D1",
                "A1",
            ]
            Front_Points_List = [
                A,
                B,
                C,
                D,
                E,
                F,
                G,
                H,
                E1,
                I,
                L,
                X,
                M,
                Mbis,
                N,
                O,
                M2,
                X1,
                L1,
                I1,
                N1,
                C1,
                D1,
                A1,
            ]
            dca, self.exterieur_avant = self.pistolet(
                np.array([B, H, L1, OND1, D1]), 4, tot=True
            )
        else:
            if self.darts == True:
                dha, self.ceinture_avant = self.pistolet(
                    np.array([A1, Mbis, M2, B1]), 2, tot=True
                )
                print("Front waist = " + str(dha))
                Front_Points_Names = [
                    "A",
                    "B",
                    "B1",
                    "C",
                    "D",
                    "E",
                    "F",
                    "G",
                    "H",
                    "E1",
                    "I",
                    "L",
                    "X",
                    "M",
                    "Mbis",
                    "N",
                    "O",
                    "M2",
                    "X1",
                    "L1",
                    "I1",
                    "N1",
                    "C1",
                    "D1",
                    "A1",
                ]
                Front_Points_List = [
                    A,
                    B,
                    B1,
                    C,
                    D,
                    E,
                    F,
                    G,
                    H,
                    E1,
                    I,
                    L,
                    X,
                    M,
                    Mbis,
                    N,
                    O,
                    M2,
                    X1,
                    L1,
                    I1,
                    N1,
                    C1,
                    D1,
                    A1,
                ]
            else:
                dha, self.ceinture_avant = self.pistolet(
                    np.array([A1, Mbis, B1]), 2, tot=True
                )
                print("Front waist = " + str(dha))
                Front_Points_Names = [
                    "A",
                    "B",
                    "B1",
                    "C",
                    "D",
                    "E",
                    "F",
                    "G",
                    "H",
                    "E1",
                    "I",
                    "L",
                    "X",
                    "M",
                    "Mbis",
                    "N",
                    "O",
                    "X1",
                    "L1",
                    "I1",
                    "N1",
                    "C1",
                    "D1",
                    "A1",
                ]
                Front_Points_List = [
                    A,
                    B,
                    B1,
                    C,
                    D,
                    E,
                    F,
                    G,
                    H,
                    E1,
                    I,
                    L,
                    X,
                    M,
                    Mbis,
                    N,
                    O,
                    X1,
                    L1,
                    I1,
                    N1,
                    C1,
                    D1,
                    A1,
                ]

            dca, self.exterieur_avant = self.pistolet(
                np.array([B1, H, L1, OND1, D1]), 4, tot=True
            )

        #
        # finish by referencing the points and building the contour point list
        #

        for i in range(len(Front_Points_Names)):
            self.Front_dic[Front_Points_Names[i]] = Front_Points_List[i]
            self.Front_dic[
                Front_Points_Names[i]
            ].pname_ori = Front_Points_Names[i]

        self.Front_vertices = (
            self.interieur_avant
            + self.fourche_avant
            + self.ceinture_avant
            + self.exterieur_avant
            + [N1.pos(), C1.pos()]
        )
        for i in range(len(self.Front_vertices)):
            p = Point(
                self.Front_vertices[i],
                point_type="contour",
                pname_ori="fp%s" % (i),
            )
            self.Trousers_Front_Contour_list.append(p)

        self.front_width = dha
        print(self.front_width)

    ############################################################

    def Donnanno_back_trousers(self, delta=6):
        """
        Calculate back Trousers' pattern

        Args:
                delta: distance between patterns as int (or float)
        """

        dx = self.m["tour_bassin"] / 4 + delta

        A = Point([dx + self.m["tour_bassin"] / 4 + 2, self.m["longueur_tot"]])
        B = Point([dx, A.y])
        C = Point([A.x, 0])
        D = Point([dx, 0])

        G = A - [0, self.m["hauteur_bassin"]]  # hip line
        H = Point([B.x, G.y])

        E = A - [0, self.m["montant"]]  # crotch line
        F = Point([B.x, E.y])

        if self.gender == "m":
            E1 = E + [self.distance(E, F) / 3 + 1.5, 0]
            E2 = E1 - [0, 2]
            Es = E2 - [2, 0]
        else:
            E1 = E + [self.m["tour_bassin"] / 16 + 3, 0]
            E2 = E1 + [0, -1]
            E3 = E + [0, -2]
            E4 = E1 + [0, -2]
            Es = self.middle(E3, E4)

        I = E - [0, self.m["montant"]]
        L = Point([F.x, I.y])

        X = self.middle(E1, F)
        M = Point([X.x, A.y])
        N = Point([X.x, C.y])
        X1 = Point([X.x, I.y])

        O = Point([X.x, M.y - self.m["hauteur_taille_genou"]])
        if self.gender == "m":
            A1 = A - [4.5, 0]
            A2 = A1 + [0, 2.5]  # from 2 to 3.5

            B1 = B - [0, 0.5]
        else:
            A1 = A - [3.5 - self.wfd["center_back"], 0]
            A2 = A1 + [0, 2]  # from 1 to 3.5
            if self.darts == True:
                B1 = B + [1 + self.wfd["sides"], 0]
            else:
                B1 = B + [3 + self.wfd["sides"], 0]

        a = self.segment_angle(A2, B1)
        self.back_waist_angle = a

        if self.gender == "m":
            waist = self.distance(A, B)
            B3 = A2 - (waist * np.cos(a), waist * np.sin(a))
            B4 = A2 - (2 * waist * np.cos(a) / 3, 2 * waist * np.sin(a) / 3)
            I1 = X1 + (14, 0)  # thigh originally 14 why ?
            L1 = X1 - (14, 0)
            N1 = N - (0, 1.5)
        else:
            if self.darts == True:
                waist = self.distance(A2, B1)
                print("Back waist = " + str(waist))
                B2 = B1 + [0.5 * waist * np.cos(a), 0.5 * waist * np.sin(a)]
            I1 = X1 + (13, 0)  # thigh originally 13 why ?
            L1 = X1 - (13, 0)
            N1 = N - (0, 1)

        C1 = N + (12, 0)  # why 12
        D1 = N - (12, 0)

        # points supplémentaires

        CC1 = C1 + [0, 10]
        DD1 = D1 + [0, 10]

        EG = self.middle(E, G)

        dfa, self.fourche_arriere = self.pistolet(np.array([EG, Es, E2]), 2, tot=True)
        dia, self.interieur_arriere = self.pistolet(
            np.array([E2, I1, CC1, C1]), 3, tot=True
        )
        if self.gender == "m":
            dea_bas, self.exterieur_arriere_bas = self.pistolet(
                np.array([D1, DD1, L1, F]), 3, tot=True
            )
            dea_haut, self.exterieur_arriere_haut = self.pistolet(
                np.array([F, H - [1, 0], B3]), 2, tot=True
            )
            Back_Points_Names = [
                "A",
                "B",
                "C",
                "D",
                "E",
                "F",
                "G",
                "H",
                "E1",
                "E2",
                "I",
                "L",
                "X",
                "M",
                "N",
                "O",
                "A1",
                "A2",
                "B1",
                "B3",
                "B4",
                "I1",
                "L1",
                "C1",
                "D1",
                "N1",
            ]
            Back_Points_List = [
                A,
                B,
                C,
                D,
                E,
                F,
                G,
                H,
                E1,
                E2,
                I,
                L,
                X,
                M,
                N,
                O,
                A1,
                A2,
                B1,
                B3,
                B4,
                I1,
                L1,
                C1,
                D1,
                N1,
            ]

            self.Back_vertices = (
                self.exterieur_arriere_bas
                + self.exterieur_arriere_haut
                + [B4.pos(), A2.pos()]
                + self.fourche_arriere
                + self.interieur_arriere
                + [N1.pos(), D1.pos()]
            )
            self.back_width = self.distance(B3, A) + self.distance(E, E1)
        else:
            dea1, self.exterieur_arriere1 = self.pistolet(
                np.array([D1, DD1, L1, F + [0.1, -2], F]), 3, tot=True
            )
            dea2, self.exterieur_arriere2 = self.pistolet(
                np.array([F, H, B1]), 2, tot=True
            )
            if self.darts == True:
                Back_Points_Names = [
                    "A",
                    "B",
                    "C",
                    "D",
                    "E",
                    "F",
                    "G",
                    "H",
                    "E1",
                    "E2",
                    "E3",
                    "I",
                    "L",
                    "X",
                    "M",
                    "N",
                    "O",
                    "A1",
                    "A2",
                    "B1",
                    "B2",
                    "I1",
                    "L1",
                    "C1",
                    "D1",
                    "N1",
                ]
                Back_Points_List = [
                    A,
                    B,
                    C,
                    D,
                    E,
                    F,
                    G,
                    H,
                    E1,
                    E2,
                    E3,
                    I,
                    L,
                    X,
                    M,
                    N,
                    O,
                    A1,
                    A2,
                    B1,
                    B2,
                    I1,
                    L1,
                    C1,
                    D1,
                    N1,
                ]
            else:
                Back_Points_Names = [
                    "A",
                    "B",
                    "C",
                    "D",
                    "E",
                    "F",
                    "G",
                    "H",
                    "E1",
                    "E2",
                    "E3",
                    "I",
                    "L",
                    "X",
                    "M",
                    "N",
                    "O",
                    "A1",
                    "A2",
                    "B1",
                    "I1",
                    "L1",
                    "C1",
                    "D1",
                    "N1",
                ]
                Back_Points_List = [
                    A,
                    B,
                    C,
                    D,
                    E,
                    F,
                    G,
                    H,
                    E1,
                    E2,
                    E3,
                    I,
                    L,
                    X,
                    M,
                    N,
                    O,
                    A1,
                    A2,
                    B1,
                    I1,
                    L1,
                    C1,
                    D1,
                    N1,
                ]

            self.Back_vertices = (
                self.exterieur_arriere1
                + self.exterieur_arriere2
                + [B1.pos(), A2.pos()]
                + self.fourche_arriere
                + self.interieur_arriere
                + [N1.pos(), D1.pos()]
            )
            self.back_width = self.distance(B1, A) + self.distance(E, E1)

        #
        # finish by referencing the points and building the contour point list
        #

        for i in range(len(self.Back_vertices)):
            p = Point(
                self.Back_vertices[i],
                point_type="contour",
                pname_ori="bp%s" % (i),
            )
            self.Trousers_Back_Contour_list.append(p)

        for i in range(len(Back_Points_Names)):
            self.Back_dic[Back_Points_Names[i]] = Back_Points_List[i]
            self.Back_dic[Back_Points_Names[i]].pname_ori = Back_Points_Names[
                i
            ]

        back_waist = self.distance(B1, A2)
        print("back waist: " + str(back_waist))
        print(
            "taille: "
            + str(self.m["tour_taille"])
            + "; bassin: "
            + str(self.m["tour_bassin"])
        )
        print(self.back_width)

    ############################################################

    def Donnanno_add_darts(self):
        """
        Add front and back darts.
        TODO darts properties should calculated from waist-hip difference.
        at present they are set by default to the typical values given by Donnanno
        Normally the maximum absorption with 3x2 darts is going to be
        4 x 2 (front)  + 2 x 3 (back) = 14cm.
        then you have to save on the sides or the central darts
        As usual Chiappetta offers a solution at least for men
        if no dart then you take from the sides and middle darts
        in a uniform manner hence (hip-waist)/4 and you redraw
        if pleats (not darts for men) she leaves the back untouched
        and adds 2x2 pleats of the necessary length
        hence ((hip - waist) - 2 x back)/4 for each pleat

        """

        if self.gender == "w":
            front_dart_list = [
                ["Mbis", "r", 1.5 + self.wfd["front_left"], -5],
                ["M2", "c", 1.5 + self.wfd["front_right"], -5],
            ]
            back_dart_list = [["B2", "c", 2 + self.wfd["back"], -9]]

        elif self.gender == "m":
            front_dart_list = [
                ["Mbis", "c", 1.5 + self.wfd["front_left"], -5],
                ["M2", "c", 1.5 + self.wfd["front_right"], -5],
            ]
            back_dart_list = [["B4", "r", 3 + self.wfd["back"], -9]]

        fpd = self.Front_dic
        poslist = []
        for dart in front_dart_list:
            if dart[1] == "r":
                Dl = fpd[dart[0]]
                Dr = Dl + [dart[2], 0]
                Dc = self.middle(Dl, Dr) + [0, dart[3]]
                poslist.append(Dl.pos())
                poslist.append(Dc.pos())
                poslist.append(Dr.pos())

            elif dart[1] == "c":
                Dl = fpd[dart[0]] - [0.5 * dart[2], 0]
                Dr = fpd[dart[0]] + [0.5 * dart[2], 0]
                Dc = fpd[dart[0]] + [0, dart[3]]
                poslist.append(Dl.pos())
                poslist.append(Dc.pos())
                poslist.append(Dr.pos())

            else:
                pass

        if self.gender == "w":
            self.ceinture_avant = [fpd["A1"].pos()] + poslist + [fpd["B1"].pos()]
        elif self.gender == "m":
            self.ceinture_avant = [fpd["A1"].pos()] + poslist + [fpd["B"].pos()]

        self.Front_vertices = (
            self.interieur_avant
            + self.fourche_avant
            + self.ceinture_avant
            + self.exterieur_avant
            + [fpd["N1"].pos(), fpd["C1"].pos()]
        )

        fbd = self.Back_dic
        poslist = []
        for dart in back_dart_list:
            if dart[1] == "c":
                Dl = fbd[dart[0]] - [
                    0.5 * dart[2] * np.cos(self.back_waist_angle),
                    0.5 * dart[2] * np.sin(self.back_waist_angle),
                ]
                Dr = fbd[dart[0]] + [
                    0.5 * dart[2] * np.cos(self.back_waist_angle),
                    0.5 * dart[2] * np.sin(self.back_waist_angle),
                ]
                Dc = fbd[dart[0]] - [
                    dart[3] * np.sin(self.back_waist_angle),
                    -dart[3] * np.cos(self.back_waist_angle),
                ]
                poslist.append(Dl.pos())
                poslist.append(Dc.pos())
                poslist.append(Dr.pos())
            elif dart[1] == "r":
                Dl = fbd[dart[0]]
                Dr = Dl + [
                    dart[2] * np.cos(self.back_waist_angle),
                    dart[2] * np.sin(self.back_waist_angle),
                ]
                Dc = self.middle(Dl, Dr) - [
                    dart[3] * np.sin(self.back_waist_angle),
                    -dart[3] * np.cos(self.back_waist_angle),
                ]
                poslist.append(Dl.pos())
                poslist.append(Dc.pos())
                poslist.append(Dr.pos())

        if self.gender == "w":
            self.ceinture_arriere = [fbd["B1"].pos()] + poslist + [fbd["A2"].pos()]
            self.Back_vertices = (
                self.exterieur_arriere1
                + self.exterieur_arriere2
                + self.ceinture_arriere
                + self.fourche_arriere
                + self.interieur_arriere
                + [fbd["N1"].pos(), fbd["D1"].pos()]
            )
        elif self.gender == "m":
            self.ceinture_arriere = [fbd["B3"].pos()] + poslist + [fbd["A2"].pos()]
            self.Back_vertices = (
                self.exterieur_arriere_bas
                + self.exterieur_arriere_haut
                + self.ceinture_arriere
                + self.fourche_arriere
                + self.interieur_arriere
                + [fbd["N1"].pos(), fbd["D1"].pos()]
            )

        self.Trousers_Front_Contour_list = []  # reinitialize the contour point list
        for i in range(len(self.Front_vertices)):
            p = Point(
                self.Front_vertices[i],
                point_type="contour",
                pname_ori="fp%s" % (i),
            )
            self.Trousers_Front_Contour_list.append(p)

        self.Trousers_Back_Contour_list = []  # reinitialize the contour point list
        for i in range(len(self.Back_vertices)):
            p = Point(
                self.Back_vertices[i],
                point_type="contour",
                pname_ori="bp%s" % (i),
            )
            self.Trousers_Back_Contour_list.append(p)

    ############################################################

    def draw_basic_trousers(
        self,
        dic={"Pattern": "Basic Trousers"},
        save=False,
        fname=None,
        paper="FullSize",
    ):
        """
        Draw basic trousers' pattern

        Args:
                dic: information to be written on the pattern as dictionnary
                save: if True save pattern to file
                fname: pattern file name as str
                paper: paper type as str

        Returns:
                ax: instance of axis used for drawing
        """
        fig, ax = self.draw_pattern(
            [self.Front_dic, self.Back_dic],
            [self.Front_vertices, self.Back_vertices],
        )

        if self.style == "Donnanno":
            fpd = self.Front_dic

            ldic = {"color": "black", "linestyle": "dashed"}
            self.segment(fpd["G"], fpd["H"], ax, ldic)
            self.segment(fpd["E1"], fpd["F"], ax, ldic)
            self.segment(fpd["M"], fpd["N"], ax, ldic)
            self.segment(fpd["A"], fpd["C"], ax, ldic)
            self.segment(fpd["B"], fpd["D"], ax, ldic)
            self.segment(fpd["C1"], fpd["D"], ax, ldic)
            self.segment(fpd["I1"], fpd["L"], ax, ldic)

            bpd = self.Back_dic
            self.segment(bpd["G"], bpd["H"], ax, ldic)
            self.segment(bpd["E1"], bpd["F"], ax, ldic)
            self.segment(bpd["M"], bpd["N"], ax, ldic)
            self.segment(bpd["A"], bpd["C"], ax, ldic)
            self.segment(bpd["A"], bpd["B"], ax, ldic)
            self.segment(bpd["B"], bpd["D"], ax, ldic)
            self.segment(bpd["C1"], bpd["D"], ax, ldic)
            self.segment(bpd["I1"], bpd["L"], ax, ldic)

        ax = self.print_info(ax, dic)

        if save:
            if fname:
                pass
            else:
                fname = "Basic_Trousers"

            of = (
                "../patterns/"
                + self.style
                + "_"
                + fname
                + "_"
                + self.pname
                + "_FullSize.pdf"
            )

            plt.savefig(of)

            if paper != "FullSize":
                self.paper_cut(fig, ax, name=fname, paper=paper)

        return ax

    ############################################################


class Flared_pants(Basic_Trousers):
    """
    Flared pants based on Donnanno dartless basic trousers

    supplementary Args:
            flare_length: added length of Trousers
            flare_width: added width at the hem,
            flare_start: place to start relative to Knee
    """

    def __init__(
        self,
        pname="gregoire",
        gender="m",
        save=False,
        paper="FullSize",
        flare_length=2,
        flare_width=5,
        flare_start=0,
        **kwargs
    ):

        style = "Donnanno"
        darts = False
        Basic_Trousers.__init__(self, pname, gender, style, darts, **kwargs)

        # beware these are not  true copies. Changes to the dic changes the original which is fine to me !
        pbf = self.Front_dic
        pbb = self.Back_dic

        tfcl = self.Trousers_Front_Contour_list
        tbcl = self.Trousers_Back_Contour_list

        N1 = pbf["N"] + [0, -flare_length]
        C2 = pbf["C1"] + [-flare_width, -flare_length]
        D2 = pbf["D1"] + [flare_width, -flare_length]

        pbf["N1"] = N1
        pbf["C2"] = C2
        pbf["D2"] = D2

        d, front_hem_curve = self.pistolet([D2, N1 + [0, 0.5], C2], kval=2, tot=True)

        y_th = pbf["O"].y + flare_start
        newContourFront = []
        newFrontVertices = [C2.pos()]
        for p in tfcl:
            if p.y > y_th:
                newContourFront.append(p)
                newFrontVertices.append(p.pos())

        newFrontVertices += front_hem_curve

        # same for the back pattern

        N1 = pbb["N"] + [0, -flare_length]
        C2 = pbb["C1"] + [flare_width, -flare_length]
        D2 = pbb["D1"] + [-flare_width, -flare_length]

        pbb["N1"] = N1
        pbb["C2"] = C2
        pbb["D2"] = D2

        d, back_hem_curve = self.pistolet([C2, N1 + [0, -0.5], D2], kval=2, tot=True)

        y_th = pbb["O"].y + flare_start
        newContourBack = []
        newBackVertices = [D2.pos()]
        for p in tbcl:
            if p.y > y_th:
                newContourBack.append(p)
                newBackVertices.append(p.pos())

        newBackVertices += back_hem_curve

        self.Front_vertices = newFrontVertices
        self.Back_vertices = newBackVertices

        ax = self.draw_basic_trousers()
        # for p in newContourBack:
        # 	ax.text(p.x,p.y,p.pname_ori)
        #
        # for p in newContourFront:
        # 	ax.text(p.x,p.y,p.pname_ori)

        ax.plot(N1.x, N1.y, "ro")
        ax.plot(C2.x, C2.y, "ro")
        ax.plot(D2.x, D2.y, "ro")


class Pants_block(Basic_Trousers):
    """
    Adapted from Pants_block for things like jogging or pyjamas.
    Donnanno. I used it to make baggy pyjamas to my teenage son...

    the front and back measurements at the bottom are calculated on the
    basis of the ankle measurement.

    It is impossible to comply with donnanno's instructions because of an incoherence
    AV = hip +6
    as the back frame is 1/2 hip +2 and the front frame 1/ Hip front + back = hip + 2
    then the distance between the two pants pieces must be 4 not 6 in order to comply with AV

    so either we comply with AV or we comply with VZ being at 3cm from the two frames and in this case V is offset by 2cm towards the front
    which keeps the sligh difference between front and back parts.
    I keep VZ as 3cm apart from the front and back patterns so V is 1cm to the left of the middle of AV

    """

    def __init__(
        self,
        pname="gregoire",
        gender="m",
        save=False,
        paper="FullSize",
        overlay=False,
        classic=True,
        **kwargs
    ):

        style = "Donnanno"
        Basic_Trousers.__init__(self, pname, gender, style, **kwargs)

        self.Donnanno_back_trousers(delta=6)

        pbf = self.Front_dic
        pbb = self.Back_dic

        AF = pbf["A"] + [0, 6]
        AB = pbb["A"] + [0, 6]

        V = self.middle(AF, AB) - [1, 0]
        Z = V + [0, -V.y]

        if classic == True:
            B1 = Z - [self.distance(pbf["C1"], pbf["D1"]) + 3, 0]
            C1 = Z + [self.distance(pbb["C1"], pbb["D1"]) + 3, 0]
        else:
            # tighter version at the ankle for my son's pyjama !
            B1 = Z - [self.m["tour_cheville"] * 3 / 4 - 2, 0]
            C1 = Z + [self.m["tour_cheville"] * 3 / 4 + 2, 0]

        print("front leg:", self.distance(pbf["E1"], B1))
        print("back leg:", self.distance(pbb["E2"], C1))

        pants_points_dic = {
            "B1": B1,
            "E1": pbf["E1"],
            "AF": AF,
            "V": V,
            "AB": AB,
            "E2": pbb["E2"],
            "C1": C1,
            "Z": Z,
        }

        pants_bloc_vertices = (
            [B1.pos(), pbf["E1"].pos()]
            + self.fourche_avant
            + [AF.pos(), AB.pos()]
            + self.fourche_arriere
            + [C1.pos(), B1.pos()]
        )

        if overlay == True:
            fig, ax = self.draw_pattern(
                [pants_points_dic, pbf, pbb],
                [
                    pants_bloc_vertices,
                    self.Front_vertices,
                    self.Back_vertices,
                ],
            )
        else:
            fig, ax = self.draw_pattern([pants_points_dic], [pants_bloc_vertices])

        # Dictionnary for plot kwargs
        ldic = {"color": "black", "linestyle": "dashed"}

        self.segment(V, Z, ax, ldic)
        self.segment(pbf["A"], pbb["A"], ax, ldic)

        # Fold line
        Fof = self.middle(AF, pbf["A"])
        Fob = self.middle(AB, pbb["A"])

        ldic = {"color": "blue", "marker": "s", "linestyle": "dashed"}
        self.segment(Fof, Fob, ax, ldic)
        mfold = self.middle(Fof, Fob)
        ax.text(mfold.x, mfold.y + 0.1, "Fold Line")

        d = np.abs(pbf["E1"].x - pbb["E1"].x)
        ankle = self.distance(B1, C1)

        ax = self.print_info(
            ax, {"Pattern": "Pyjama", "Max width": d, "Height": V.y, "Ankle": ankle}
        )

        fname = "../patterns/" + self.style + "_Block_pants_" + self.pname + ".pdf"

        if save:
            plt.savefig(fname)

            if paper != "FullSize":
                self.paper_cut(fig, ax, name="Block_pants", paper=paper)


class Bermudas(Basic_Trousers):

    """
    Bermudas based on Donnanno darted basic trousers

    specific Args:
    height_above_knee: added length of Trousers
    """

    def __init__(
        self, pname="gregoire", gender="m", height_above_knee=4, wfd=None, **kwargs
    ):

        self.style = "Donnanno"
        self.darts = True
        self.height_above_knee = 4
        Basic_Trousers.__init__(
            self, pname, gender, self.style, self.darts, wfd, **kwargs
        )

        self.calculate_front_bermudas()
        self.calculate_back_bermudas()

        # translate the bermudas down so we do not use lots of paper
        self.translate(dx=0, dy=-self.Front_dic["I3"].y)

    def calculate_front_bermudas(self):

        # beware these are not  true copies. Changes to the dic changes the original which is fine to me !
        pbf = self.Front_dic

        # place points and line above the knee
        pbf["X2"] = pbf["O"] + [0, self.height_above_knee]
        pbf["I2"] = Point([pbf["E1"].x, pbf["X2"].y])
        pbf["L2"] = Point([pbf["L"].x, pbf["X2"].y])
        pbf["I3"] = pbf["I2"] - [0, 8]
        pbf["L3"] = pbf["L2"] - [0, 8]

        # redraw side curve.
        control_points = [pbf["B1"], pbf["H"], pbf["F"]]
        d, self.exterieur_avant = self.pistolet(control_points, 2, tot=True)

        # redefine the front
        self.Front_vertices = [
            [pbf["I3"].pos(), pbf["E1"].pos()]
            + self.fourche_avant
            + self.ceinture_avant
            + self.exterieur_avant
            + [pbf["L3"].pos(), pbf["I3"].pos()]
        ]

        for key in ["C1", "C", "N1", "N", "D1", "D"]:
            pbf.pop(key, 0)
        self.Front_dic = pbf

        self.add_labelled_line(pbf["H"], pbf["G"], "HIP LINE", "t")
        self.add_labelled_line(pbf["A"], pbf["B"], "WAIST LINE", "t")
        self.add_comment(self.middle(pbf["E"], pbf["F"]) + Point([0, -5]), "FRONT")

    def calculate_back_bermudas(self):
        pbb = self.Back_dic

        # place points and line above the knee
        pbb["X2"] = pbb["O"] + [0, self.height_above_knee]
        pbb["I2"] = Point([pbb["E2"].x, pbb["X2"].y])
        pbb["L2"] = Point([pbb["L"].x, pbb["X2"].y])
        pbb["I3"] = pbb["I2"] - [0, 8]
        pbb["L3"] = pbb["L2"] - [0, 8]

        # redraw side curve.
        control_points = [pbb["F"], pbb["H"], pbb["B1"]]
        d, self.exterieur_arriere = self.pistolet(control_points, 2, tot=True)

        if self.gender == "w":
            self.Back_vertices = [
                [pbb["L3"].pos()]
                + self.exterieur_arriere
                + self.ceinture_arriere
                + self.fourche_arriere
                + [pbb["I3"].pos(), pbb["L3"].pos()]
            ]
        elif self.gender == "m":
            # bugged because it's a simple copy of women back. To be redefined later
            self.Back_vertices = [
                [pbb["L3"].pos()]
                + self.exterieur_arriere
                + self.ceinture_arriere
                + self.fourche_arriere
                + [pbb["I3"].pos(), pbb["L3"].pos()]
            ]

        for key in ["C1", "C", "N1", "N", "D1", "D"]:
            pbb.pop(key, 0)

        self.Back_dic = pbb

        self.add_labelled_line(pbb["H"], pbb["G"], "HIP LINE", "t")
        self.add_labelled_line(pbb["A2"], pbb["B1"], "WAIST LINE", "t")
        self.add_comment(self.middle(pbb["E"], pbb["F"]) + Point([0, -5]), "BACK")
