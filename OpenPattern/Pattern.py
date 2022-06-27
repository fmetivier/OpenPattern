# -*- coding: utf-8 -*-
# librairies
import sys

import matplotlib.pyplot as plt
import numpy as np
import json
import sqlite3

from scipy.interpolate import splprep, splev
from scipy.integrate import odeint

from matplotlib.patches import Polygon, PathPatch
from matplotlib.path import Path
from matplotlib.backends.backend_pdf import PdfPages

from OpenPattern.Points import Point
from copy import deepcopy


###############################################################
# Class defining tools to draw patterns
###############################################################


class Pattern:
    """Defines basic methods needed for pattern drafting

    Notes:
    - Pattern methods originally  used arrays or lists of values for points as arguments for calculations.
    - Since the development of the Point class I've progressively turned them to use it. I no longer use arrays for new methods.
    - Patterns can contain patterns (subpatterns) stored in a dictionnary of patterns

    :param    m: dictionnary of size measurements
    :param    pname:  name of size measurements
    :param    gender: gender

    """

    ############################################################

    def __init__(self, pname="W38G", gender="w", pattern_name="P0", **kwargs):
        """
        Initializes class instance

        :param    pname : measurement file if given
        :param    gender: gender of pattern to be drafted
        :param    pattern_name: a reference for use with overlays (enfin je crois...)
        :param    dbPATH: path to the sqlite3 db
        """

        self.pattern_name = pattern_name

        self.dbPATH = "./"  # default
        for k in kwargs.keys():
            if k == "dbPATH":
                self.dbPATH = kwargs["dbPATH"]
                print(self.dbPATH)

        if pname:
            self.m = self.get_measurements_sql(pname)
            self.pname = pname
        else:
            # in the end it should be able to store new measurements.
            pass  # create measures

        self.gender = gender

        # initialize dics and vertices for the pattern
        self.Front_dic = {}
        self.Back_dic = {}
        self.Front_vertices = []
        self.Back_vertices = []
        self.pattern_list = []  # List of subpatterns

    ############################################################
    #                add points or curves to dics
    #                and get them back
    #               copy pattern and add sub_patterns
    ############################################################

    def copy(self):
        """Deepcopy pattern to a newly named one"""
        return deepcopy(self)

    def add_pattern(self, P):
        self.pattern_list.append(P)

    def add_point(self, name="A", p=Point([0, 0]), dic="front"):
        """
        adds a point to the corresponding dic

        :param    name: point name
        :param    p: point
        :param    dic: 'front' for front dic, 'back' for back dic
        """

        if dic == "front":
            # print('coucou')
            self.Front_dic[name] = p
        elif dic == "back":
            self.Back_dic[name] = p
        else:
            print("choose back or front for the dictionnary that stores the points")

    def add_curve(self, name="front_curve", coords=[0, 0], dic="front"):
        """
        adds a curve to the corresponding dic


        :param    name: str,  curve name
        :param    coords: list of floats, x and y coordinates
        :param    dic: 'front' or 'back' dics to store the point
        """
        if dic == "front":
            self.Front_dic[name] = coords
        elif dic == "back":
            self.Back_dic[name] = coords
        else:
            print("choose back fo front for the dictionnary that stores the points")

    def get(self, pname="A", dic="front"):
        """
        returns the point/curve pname from the corresponding dic


        :param    pname: str point/curve name
        :param    dic: 'front' or back' dictionnary from which to extrac the point


        :returns: the chosen point or the list of coordinates of a curve
        :rtype: Point or list
        """
        if dic == "front":
            return self.Front_dic[pname]
        if dic == "back":
            return self.Back_dic[pname]
        else:
            print("choose back fo front for the dictionnary that stores the points")
            return 1

    def generate_lists(self):
        """
        generates a list of point vertices and a list of point dictionnaries for drawing
        this method can only be called by children classes but is common to them

        cheks if the front and back vertices are lists of points or if they are lists of lists of points
        in the former case adds the front and back vertices to a list of vertices_list
        in the latter adds the lists of vertices inside the front and back vertices list to the vertices list
        to be plotted. This trick enables to «cut» a pattern in as many pieces (polygons) as you want

        The problem does not apply for the dictionnary as there is no need to cut them.
        They are only here to plot points

        """
        vl = []
        dl = []

        if len(self.Front_vertices) > 0:
            if isinstance(self.Front_vertices[0][0], list):
                for fv in self.Front_vertices:
                    vl.append(fv)
            else:
                vl.append(self.Front_vertices)
        if len(self.Back_vertices) > 0:
            if isinstance(self.Back_vertices[0][0], list):
                for bv in self.Back_vertices:
                    vl.append(bv)
            else:
                vl.append(self.Back_vertices)

        if len(self.Front_dic) > 0:
            dl.append(self.Front_dic)
        if len(self.Back_dic) > 0:
            dl.append(self.Back_dic)

        return dl, vl

    ############################################################
    # get and store measurements
    ############################################################

    def get_measurements_json(self, pname="sophie"):
        """Load stored measurements.

        Measurements loaded are dictionnaries stored as json files in the measurements folder
        23/12/2020: This is the original version now i use sqlite

        :param    pname: name of json file as str

         :returns: a dictionnary of size measurments
        :rtype: dic
        """

        with open("../measurements/" + pname + "_data.json", "r") as read_file:
            dic = json.load(read_file)

        return dic

    def get_measurements_sql(self, pname="sophie"):
        """Load stored measurements.

        Measurements loaded are dictionnaries stored as json files in the measurements folder

        :param    pname: name of pattern measurement code string

        :returns:  a dictionnary of size measurments
        :rtype: dic
        """

        conn = sqlite3.connect(self.dbPATH + "measurements.db")
        c = conn.cursor()

        dic = {}
        for row in c.execute("select * from measurements where wkey = ?", (pname,)):
            dic[row[1]] = row[2]

        conn.close()

        return dic

    def save_measurements_json(self, ofname=None):
        """Save new measurements

        Save new measurements in ofname_data.json file in the mesures folder
        If no output format is given stores the data under the attribute self.pname
        20/12/2020 changed to sql

        :param    str ofname: output json filename

        """
        if ofname:
            with open("../measurements/" + ofname + "_data.json", "w") as write_file:
                json.dump(self.m, write_file)
        else:
            with open(
                "../measurements/" + self.pname + "_data.json", "w"
            ) as write_file:
                json.dump(self.m, write_file)

    def save_measurements_sql(self, ofname=None):
        """Save new measurements

        Save new measurements under ofname key in the mesurement database
        If no output format is given stores the data under the attribute self.pname
        ! beware of the final path.

        :param    str ofname: output wkey for measurements.db database

        """
        conn = sqlite3.connect(self.dbPATH + "measurements.db")
        c = conn.cursor()

        if ofname:
            if ofname != self.pname:
                pass
            else:
                c.execute("delete from measurements where wkey = ?", (ofname,))
        else:
            ofname = self.pname
            c.execute("delete from measurements where wkey = ?", (ofname,))

        for key, val in self.m.items():
            c.execute("insert into measurements values (?,?,?)", (ofname, key, val))

        conn.commit()
        conn.close()

    ############################################################
    #                Calculations
    ############################################################

    def distance(self, A, B):
        """Returns distance [AB]

        :param    A: point given as Point or array([x,y])
        :param    B: point given as Point or array([x,y])


        :returns: distance
        :rtype: float
        """

        if isinstance(A, Point) and isinstance(B, Point):
            return np.sqrt((A.x - B.x) ** 2 + (A.y - B.y) ** 2)
        else:
            return np.sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2)

    ############################################################

    def intersec_lines(self, A, B, C, D):
        """Finds the instersection between , lines AB and CD

        :param    A: Point or  array([x,y])
        :param    B: Point or  array([x,y])
        :param    C: Point or  array([x,y])
        :param    D: Point or  array([x,y])


        :returns: x,y coordinates
        :rtype:    Point or tuple
        """
        if isinstance(A, Point) and isinstance(B, Point) and isinstance(C, Point):
            # coefficient de AB
            aD1 = (B.y - A.y) / (B.x - A.x)
            bD1 = A.y - aD1 * A.x

            # coefficients de CD
            aD2 = (C.y - D.y) / (C.x - D.x)
            bD2 = C.y - aD2 * C.x

            xi = (bD2 - bD1) / (aD1 - aD2)
            yi = aD1 * xi + bD1

            return Point([xi, yi])
        else:
            aD1 = (B[1] - A[1]) / (B[0] - A[0])
            bD1 = A[1] - aD1 * A[0]

            # coefficients de CD
            aD2 = (C[1] - D[1]) / (C[0] - D[0])
            bD2 = C[1] - aD2 * C[0]

            xi = (aD1 - aD2) / (bD2 - bD1)
            yi = aD1 * xi + bD1

            return (xi, yi)

    ############################################################

    def intersec_manches(self, A, B, C, theta):
        """Intersection calculation

        Finds the point of intersection G of the AB line with the line going through C
        and making an  angle theta with the horizontal axis.
        Especially useful for sleeve heads.
        Does not work if AB is vertical !!!

        :param    A: Point or  array([x,y])
        :param    B: Point or  array([x,y])
        :param    C: Point or  array([x,y])
        :param    theta: angle in degrees

        :returns: Point([x,y]) or    (x,y) tuple of coordinates
        """

        if isinstance(A, Point) and isinstance(B, Point) and isinstance(C, Point):
            # coefficient de AB
            aD1 = (B.y - A.y) / (B.x - A.x)
            bD1 = A.y - aD1 * A.x

            # coefficients de CG
            aD2 = np.tan(theta * np.pi / 180)
            bD2 = C.y - aD2 * C.x

            # intersection
            x = (bD2 - bD1) / (aD1 - aD2)
            y = aD1 * x + bD1

            return Point([x, y])

        else:
            # coefficient de AB
            aD1 = (B[1] - A[1]) / (B[0] - A[0])
            bD1 = A[1] - aD1 * A[0]

            # coefficients de CG
            aD2 = np.tan(theta * np.pi / 180)
            bD2 = C[1] - aD2 * C[0]

            # intersection
            x = (bD2 - bD1) / (aD1 - aD2)
            y = aD1 * x + bD1

            return (x, y)

    ############################################################

    def middle(self, A, B):
        """returns the middle point of [AB]

        :param    A: Point or array([x,y])
        :param    B: Point or array([x,y])

        :returns: x,y as an array
        """
        if isinstance(A, Point) and isinstance(B, Point):
            return Point([0.5 * (A.x + B.x), 0.5 * (A.y + B.y)])
        else:
            return np.array([0.5 * (A[0] + B[0]), 0.5 * (A[1] + B[1])])

    ############################################################

    def segment_angle(self, A, B):
        """Returns slope of segment [AB]

        :param    A: Point or array([x,y])
        :param    B: Point or array([x,y])

        :returns:    angle in radians
        :rtype: float
        """

        if isinstance(A, Point) and isinstance(B, Point):
            if B.x - A.x == 0:
                return np.pi / 2
            else:
                return np.arctan((B.y - A.y) / (B.x - A.x))
        else:
            if B[0] - A[0] == 0:
                return np.pi / 2
            else:
                return np.arctan((B[1] - A[1]) / (B[0] - A[0]))

    ############################################################

    def oriented_segment_angle(self, A, B):
        """Returns slope of segment [AB]

        In this case the slope is positionned in the good quadrant depending
        on the relative positions of A and B

        :param    A: Point or array([x,y])
        :param    B: Point or array([x,y])

        :returns:    angle in radians
        :rtype: float
        """

        if isinstance(A, Point) and isinstance(B, Point):
            if B.x - A.x == 0:
                if B.y >= A.y:
                    return np.pi / 2
                else:
                    return 3 * np.pi / 2
            else:
                if (B.x - A.x) > 0:
                    return np.arctan((B.y - A.y) / (B.x - A.x))
                else:
                    return np.arctan((B.y - A.y) / (B.x - A.x)) + np.pi
        else:
            if B[0] - A[0] == 0:
                if B[1] - A[1] >= 0:
                    return np.pi / 2
                else:
                    return -np.pi / 2
            else:
                if B[0] - A[0] > 0:
                    return np.arctan((B[1] - A[1]) / (B[0] - A[0]))
                else:
                    return np.arctan((B[1] - A[1]) / (B[0] - A[0])) + np.pi

    ############################################################

    def segment_offset(self, A, B, alpha, d):
        """translates segment AB by a vector of length d making an angle alpha  with AB

        :param A,B: Points
        :param alpha : real angle in radians
        :param d: offset distance in m

        :returns: Ap, Bp the offset points
        :rtype: Point
        """

        if isinstance(A, Point) and isinstance(B, Point):
            a = self.oriented_segment_angle(A, B)
            beta = a + alpha

            Ap = Point([A.x + np.cos(beta) * d, A.y + np.sin(beta) * d])
            Bp = Point([B.x + np.cos(beta) * d, B.y + np.sin(beta) * d])

            return Ap, Bp
        else:
            print("Points needed for this method")
            return 1

    ############################################################

    def curve_offset(self, ilist, alpha, d, closed=False):
        """translates a curve by a vector of length d making an angle alpha  with the local tangent


        :param    plist: list of [x,y] points positions
        :param    alpha : real angle in radians
        :param    d: offset distance in m


        :returns:    olist list of [x,y] offset points positions
        :rtype: list of [x, y] coordinates
        """
        plist = deepcopy(ilist)
        olist = []
        N = len(plist)
        beta = []
        # first loop find the angles
        for i in range(N - 1):
            a = self.oriented_segment_angle(plist[i], plist[i + 1])
            beta.append(a + alpha)

        # second loop offset

        if closed == False:
            x = plist[0][0] + np.cos(beta[0]) * d
            y = plist[0][1] + np.sin(beta[0]) * d
            olist.append([x, y])
        else:
            plist[0][0] += np.cos(beta[0]) * d
            plist[0][1] += np.sin(beta[0]) * d

        plist[1][0] += np.cos(beta[0]) * d
        plist[1][1] += np.sin(beta[0]) * d

        for i in np.arange(N - 2) + 1:

            x = plist[i][0] + np.cos(beta[i]) * d
            y = plist[i][1] + np.sin(beta[i]) * d
            olist.append([x, y])

            plist[i + 1][0] += np.cos(beta[i]) * d
            plist[i + 1][1] += np.sin(beta[i]) * d

        # use the last value of beta for the last point
        if closed == False:
            x = plist[N - 1][0]
            y = plist[N - 1][1]
        else:
            x = plist[0][0] + np.cos(beta[N - 2]) * d
            y = plist[0][1] + np.sin(beta[N - 2]) * d

        olist.append([x, y])

        return olist

    ############################################################

    def pistolet(
        self,
        points,
        kval=2,
        ax=None,
        kwargs={"color": "blue", "linestyle": "solid"},
        tot=False,
    ):
        """French curve calculation

        calculates a spline of order kval from set of given points.
        if ax given draws the result on ax and returns length of Armhole
        if tot returns a list of 30 points to draw the spline curve.


        :param    points: array of tuples or list of points
        :param    kval: int
        :param    ax: matplotlib axis
        :param    kwargs: dictionnary of drawing properties
        :param    tot: boolean deciding whether the entire curve is returned

        :returns:    Total distance if tot = False
        :returns:    Total distance and list of interpolated points if tot = True
        """
        if isinstance(points[0], Point):  # test on the first point of the list
            xlist, ylist = [], []
            for p in points:
                xlist.append(p.x)
                ylist.append(p.y)
            tck, u = splprep([xlist, ylist], k=kval, s=0)

        else:
            tck, u = splprep(
                [points.transpose()[0], points.transpose()[1]], k=kval, s=0
            )

        us = np.linspace(u.min(), u.max(), 100)
        new_points = splev(us, tck)
        if ax:
            ax.plot(new_points[0], new_points[1], **kwargs)

        dx = np.diff(new_points[0])
        dy = np.diff(new_points[1])

        if tot:
            point_vertices = []
            for i in range(len(new_points[0])):
                point_vertices.append([new_points[0][i], new_points[1][i]])
            return np.sum(np.sqrt(dx ** 2 + dy ** 2)), point_vertices

        else:
            return np.sum(np.sqrt(dx ** 2 + dy ** 2))

    ############################################################
    # now true clothoid for sleeve hole (at least for now)
    # the implementation of the clothoid is taken from

    def clothoid_ode_rhs(self, state, s, kappa0, kappa1):
        x, y, theta = state[0], state[1], state[2]
        return np.array([np.cos(theta), np.sin(theta), kappa0 + kappa1 * s])
        # theta_min = min(theta_1,theta_2)
        # theta_max = max(theta_1,theta_2)

    def eval_clothoid(self, x0, y0, theta0, kappa0, kappa1, s):
        return odeint(
            self.clothoid_ode_rhs, np.array([x0, y0, theta0]), s, (kappa0, kappa1)
        )

    def find_center(self, xdat, ydat):
        xm = []
        ym = []
        for i in range(len(xdat) - 1):
            xm.append(0.5 * (xdat[i] + xdat[i + 1]))
            ym.append(0.5 * (ydat[i] + ydat[i + 1]))

        xm = np.array(xm)
        ym = np.array(ym)

        # print(xm,ym)
        sm = np.tan(np.arctan(np.diff(ydat) / np.diff(xdat)) + np.pi / 2 * np.ones(2))
        bm = ym - sm * xm

        xc = -np.diff(bm) / np.diff(sm)
        yc = sm[0] * xc + bm[0]

        return xc, yc, sm, bm, xm, ym

    def True_pistolet(self, point_list):
        """Fits a TRUE 100pt clothoid to three points
        designed primarily for sleeve holes
        but can do for any three point curve.

        args:
            point_list: list of three points

        returns:
            xs, ys: coordinates of clothoid curve points

        à adapter au différents types de courbures
        emmanchures, tour de col etc...

        pour les jupes, col et tête de manche les spleen semblent
        très bien fonctionner

        ce sont fondamentalement les emmanchures
        qui elles ne marchent pas bien.

        On pourrait aussi probablement améliorer le tour d'encolure

        il faut toujours commencer par la pente la plus douce
        et faire une Transformation de sorte à ce que la convexité soit
        bien orientée
        puis revenir au point initial
        """

        if len(point_list) > 3:
            print("bad point number")
            return 1

        xdat, ydat = [], []
        for p in point_list:
            xdat.append(p.x)
            ydat.append(p.y)

        xdat = np.array(xdat)
        ydat = np.array(ydat)

        # fig = plt.figure()
        # ax = fig.add_subplot(111)
        # ax.axis('square')
        # ax.plot(xdat, ydat, 'bo', zorder=5)
        # ax.set_xlim(-100,100)
        # ax.set_ylim(-100,100)

        # preserve
        x_ori = deepcopy(xdat)
        y_ori = deepcopy(ydat)

        vsym = False
        # tester la position du second point et faire
        if xdat[1] > xdat[2]:
            vsym = True
            xdat = -xdat

        # rotation

        dx = np.diff(xdat)
        dy = np.diff(ydat)
        a_ori = np.arctan(dy / dx)

        M = np.array(
            [
                [np.cos(a_ori[0]), -np.sin(a_ori[0])],
                [np.sin(a_ori[0]), np.cos(a_ori[0])],
            ]
        )
        rotated = np.matmul(M, np.vstack([xdat - xdat[0], ydat - ydat[0]]))
        xdat = rotated[0]
        ydat = rotated[1]
        # ax.plot(xdat,ydat,'go')

        #####################################
        # Not the best and certainly not the most
        # efficient BUT it enables to Fit
        # a TRUE French curve (or clothoid)
        # to our points and that is cool !
        #####################################

        # find center and slipes of the two circles
        # that pass throug the points
        xc, yc, sm, bm, xm, ym = self.find_center(xdat, ydat)

        # compute radiuses
        rm = np.sqrt((ydat[:-1] - yc) ** 2 + (xdat[:-1] - xc) ** 2)

        #####################################
        #
        # compute  slopes and
        # cumulative length
        # of the two circle portions
        #####################################

        X = []
        Y = []
        A = []

        for i in range(2):
            th = []
            for j in range(2):
                tmpth = np.arctan((ydat[i + j] - yc) / (xdat[i + j] - xc))

                # needed to check because arctan looses the point quadrant
                if xdat[i + j] - xc > 0:
                    th.append(tmpth)
                elif xdat[i + j] - xc < 0:
                    th.append(tmpth + np.pi)

            # because the jump occurs at 3pi/2 in python we have to
            # take this into account to prevent discontinuities in the
            # angles
            if th[1] > th[0]:
                T = np.linspace(th[0], th[1], 10)
            else:
                T = np.linspace(th[0], th[1] + np.pi * 2, 10)

            for j in range(len(T)):
                X.append(xc + rm[i] * np.cos(T[j]))
                Y.append(yc + rm[i] * np.sin(T[j]))
                A.append(T[j] - np.pi / 2)

        X = np.hstack(X)
        Y = np.hstack(Y)
        distance = np.cumsum(np.diff(X) ** 2 + np.diff(Y) ** 2)
        A = np.hstack(A)

        # and again we have to go back to the orginial angle
        # see the trick above
        for i in range(len(A) - 1):
            if np.abs(A[i + 1] - A[i]) > 0.5:
                A[i + 1] += 2 * np.pi

        # ok at present I only use the first value...
        K0 = (A[2] - A[1]) / (distance[1] - distance[0])
        # but I use the length !
        L = max(distance)
        s = np.linspace(0, L, 100)

        # minimisation procedure
        # first we minimise kappa0 as it almost does the job
        N0 = 100
        isel = 0
        dsel = 99999999
        for i in range(N0):
            kappa0 = K0 + 0.005 * (i - N0 / 2)
            kappa1 = 0

            sol = self.eval_clothoid(xdat[0], ydat[0], A[0] - np.pi, kappa0, kappa1, s)
            xs, ys, thetas = sol[:, 0], sol[:, 1], sol[:, 2]

            dtest = 0
            for xv, yv in zip(xdat[1:], ydat[1:]):
                d = (xs - xv) ** 2 + (ys - yv) ** 2
                dmin = min(d)
                dtest += dmin

            if dtest < dsel:
                isel = i
                dsel = dtest

        kappa0 = K0 + 0.005 * (isel - N0 / 2)
        # then fine tune with kappa1
        N1 = 100
        jsel = 0
        dsel = 99999999
        for j in range(N1):
            kappa1 = 0.0001 * (j - N1 / 2)

            sol = self.eval_clothoid(xdat[0], ydat[0], A[0] - np.pi, kappa0, kappa1, s)
            xs, ys, thetas = sol[:, 0], sol[:, 1], sol[:, 2]

            dtest = 0
            for xv, yv in zip(xdat[1:], ydat[1:]):
                d = (xs - xv) ** 2 + (ys - yv) ** 2
                dmin = min(d)
                dtest += dmin

            if dtest < dsel:
                jsel = j
                dsel = dtest

        kappa1 = 0.0001 * (jsel - N1 / 2)
        print(kappa0, kappa1)

        # And we have it !

        sol = self.eval_clothoid(xdat[0], ydat[0], A[0] - np.pi, kappa0, kappa1, s)
        xs, ys, thetas = sol[:, 0], sol[:, 1], sol[:, 2]

        # finally crop for L
        d = (xs - xdat[2]) ** 2 + (ys - ydat[2]) ** 2
        dmin = min(d)
        end_index = np.where(d == dmin)[0][0]
        print(end_index)

        xs = xs[:end_index]
        ys = ys[:end_index]

        L_clothoid = max(np.cumsum(np.sqrt(np.diff(xs) ** 2 + np.diff(ys) ** 2)))
        print("clothoid length", L_clothoid)
        # ax.plot(xs, ys)

        # return to normal
        Minv = np.linalg.inv(M)
        back1 = np.dot(Minv, np.array([xs, ys]))
        if vsym:
            xs = back1[0] - x_ori[0]
        else:
            xs = back1[0] + x_ori[0]
        ys = back1[1] + y_ori[0]

        if vsym:
            xs = -xs

        # Eventually transform into vertices list
        clothoid_vertices = []
        for x, y in zip(xs, ys):
            clothoid_vertices.append([x, y])

        # ax.plot(xs, ys)
        # plt.show()

        # FINI!  returns clothoid_length
        # and clothoid points coordinates as vertices
        return L_clothoid, clothoid_vertices

    def add_dart(
        self,
        center=Point(),
        A=Point(),
        B=Point(),
        opening=0,
        draw_curves=False,
        order="lr",
        rotate_end="none",
    ):
        """adds a dart to a pattern
        if draw_curves = True: draws the curve when the dart is closed then rotates when opening the dart
        if rotate = none: rotation of the curves or segment decreases linearly to reach 0 at the end points.
        if rotate =  left or right or both: also rotates the end points. The angle of rotation remains constant in this case NOT IMPLEMENTED YET

        BEWARE : bug. At present draw_curves works if the pattern polygon is drawn in lr hence
        in a clockwise manner.

        :param    center: Point position of the dart edge and center of rotation
        :param    A, B: Points segment to cut
        :param    opening: float width of the dart


        :returns:    dart1, dart2 points of the dart.
        :rtype: Points
        """

        # angle of the segment to cut
        theta = self.segment_angle(A, B) + np.pi / 2

        # point of intersection
        I = self.intersec_manches(A, B, center, theta * 180 / np.pi)

        if draw_curves == True:
            control_points = [A, I, B]

            db, curve_points = self.pistolet(control_points, 2, tot=True)
            if rotate_end == "none":
                # find the place of I and separate the curve into two subcurves
                list_1 = []
                list_2 = []
                dval = 1000
                for p in curve_points:
                    d = self.distance(I, Point(p))
                    dd = d - dval
                    if d < dval and dd < 0:
                        list_1.append(Point(p))
                    elif d > dval and dd > 0:
                        list_2.append(Point(p))
                    dval = d

                # rotate lists
                rotated_curve_1 = []
                N = len(list_1)

                if order == "lr":
                    theta_N = opening / (2 * self.distance(center, I) * N)
                    theta = 0
                    dtheta = theta_N
                elif order == "rl":
                    theta_N = opening / (2 * self.distance(center, I) * N)
                    theta = 0
                    dtheta = -theta_N

                for p in list_1:
                    p.rotate(center, theta, unit="rad")
                    theta += dtheta
                    rotated_curve_1.append(p.pos())

                rotated_curve_2 = []
                N = len(list_2)

                if order == "rl":
                    theta_N = opening / (2 * self.distance(center, I) * N)
                    theta = N * theta_N
                    dthetat = -theta_N
                elif order == "lr":
                    theta_N = opening / (2 * self.distance(center, I) * N)
                    theta = -N * theta_N
                    dtheta = theta_N

                for p in list_2:
                    p.rotate(center, theta, unit="rad")
                    theta += dtheta
                    rotated_curve_2.append(p.pos())

                return rotated_curve_1, rotated_curve_2

            elif rotate_end == "left":
                pass
            elif rotate_end == "right":
                pass
            elif rotate_end == "both":
                pass
            else:
                pass

        else:
            theta = opening / (2 * self.distance(center, I))
            I1 = I.copy()
            I1.rotate(center, theta, unit="rad")
            I2 = I.copy()
            I2.rotate(center, -theta, unit="rad")

            return I1, I2

    ############################################################

    def translate(self, dx, dy):
        """translation of the entire pattern by dx, dy

        :param dx, dy: floats
        """

        dl, vl = self.generate_lists()

        for dic in dl:
            for key, val in dic.items():
                val += [dx, dy]

        for j in range(len(vl)):
            for i in range(len(vl[j])):
                vl[j][i][0] += dx
                vl[j][i][1] += dy

    ############################################################

    def rotate(self, C=Point([0, 0]), theta=0):
        """Rotation of the entire pattern of angle theta around center class.

        In the case of points uses the rotate method for points if not does the rotation "manually".
        BEWARE not to pass dic points directly as the center because this might induce spurious rotations.

        :param C: Point, center of rotation
        :param theta: float angle of rotation in radians
        """

        dl, vl = self.generate_lists()

        for dic in dl:
            for key, val in dic.items():
                val.rotate(C, theta, "rad")

        for j in range(len(vl)):
            for i in range(len(vl[j])):
                x, y = vl[j][i]

                p = np.array(
                    [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]]
                )
                xo = p[0, 0] * (x - C.x) + p[0, 1] * (y - C.y) + C.x
                yo = p[1, 0] * (x - C.x) + p[1, 1] * (y - C.y) + C.y

                vl[j][i][0] = xo
                vl[j][i][1] = yo

    ############################################################
    def project_point(self, M, A, B):
        """returns the coordinates of the projection of M on the line (AB)

        :param M: points to be projected
        :param A,B: points defining the line on which M is projected

        :returns: projected point
        :rtype: Point
        """
        # print(type(M),type(A),type(B))
        dx = B.x - A.x
        dy = B.y - A.y

        if dx == 0:
            X = A.x
            Y = M.y
        else:
            X = (M.x * dx + A.x * dy ** 2 / dx - dy * (A.y - M.y)) / (dx + dy ** 2 / dx)
            Y = (dy / dx) * (X - A.x) + A.y

        return Point([X, Y])

    def mirror_point(self, A, M):
        """returns the mirror point of a point A with respect to point M
        <=> translate A by 2AM

        :param A: Point to mirror
        :param M: center of symetry

        :returns: mirrored point
        :rtype: Point
        """

        # print(type(A.x),type(M.x))
        dx = M.x - A.x
        dy = M.y - A.y

        X = A.x + 2 * dx
        Y = A.y + 2 * dy

        return Point([X, Y])

    def unfold(self, d, v, A, B):
        """Unfolds a pattern

        Unfolds a pattern stored on the vertices list  where AB represents the fold line.


        :param v: list of vertices
        :param d: dictionnary of points
        :param A,B: Points defining the fold line

        :returns: vu, du dictionnary and list of original and mirrored points
        :rtype: list and dic
        """

        vu = []
        du = {}

        for key, val in d.items():
            M = self.project_point(val, A, B)
            P = self.mirror_point(val, M)
            nkey = key + "m"
            du[nkey] = P

        for p in v:
            P = Point(p)
            M = self.project_point(P, A, B)
            MP = self.mirror_point(P, M)
            vu.append(MP.pos())

        return du, vu

    ############################################################
    #                Drawings
    ############################################################

    def segment(self, A, B, ax, kwargs={"color": "blue"}):
        """
        plots [AB] segment on ax


        :param    A,B: points given as array([x,y])
        :param    ax: axis on which to plot
        :param    kwargs: dictionnary of drawing porperties
        """

        if isinstance(A, Point) and isinstance(B, Point):
            ax.plot([A.x, B.x], [A.y, B.y], **kwargs)
        else:
            ax.plot([A[0], B[0]], [A[1], B[1]], **kwargs)

    def draw_pattern(
        self,
        dic_list=[],
        vertices_list=[],
        polyline_list=[],
        fig=None,
        ax=None,
        overlay=False,
    ):

        """
        for each dic in dic_list
            plots points given in dic
        for each vertices in vertices_list
            draws the polygon defined by vertices_list

            The figure is a 1:1 scaled pattern ready to print on a
            full size AO printer.


        :param    dic_list: list of dictionnaries of points to be plotted as points
                with label
        :param    vertices_list: list of vertices list to be plotted as lines


        :returns:    fig, ax
        """

        ####################################################
        #       Figure size calculation and axes creation
        ####################################################

        # checks if ax argument exists

        xmin = 0
        ymin = 0
        xmax = 0
        ymax = 0

        for polyline in polyline_list:
            for val in polyline:
                if int(val[0]) < xmin:
                    xmin = int(val[0])
                if int(val[0]) > xmax:
                    xmax = int(val[0])
                if int(val[1]) < ymin:
                    ymin = int(val[1])
                if int(val[1]) > ymax:
                    ymax = int(val[1])

        for vertice in vertices_list:
            for val in vertice:
                if int(val[0]) < xmin:
                    xmin = int(val[0])
                if int(val[0]) > xmax:
                    xmax = int(val[0])
                if int(val[1]) < ymin:
                    ymin = int(val[1])
                if int(val[1]) > ymax:
                    ymax = int(val[1])

        for dic in dic_list:
            for key, val in dic.items():
                if isinstance(val, Point):
                    if int(val.x) < xmin:
                        xmin = int(val.x)
                    if int(val.x) > xmax:
                        xmax = int(val.x)
                    if int(val.y) < ymin:
                        ymin = int(val.y)
                    if int(val.y) > ymax:
                        ymax = int(val.y)
                else:
                    if int(val[0]) < xmin:
                        xmin = int(val[0])
                    if int(val[0]) > xmax:
                        xmax = int(val[0])
                    if int(val[1]) < ymin:
                        ymin = int(val[1])
                    if int(val[1]) > ymax:
                        ymax = int(val[1])

        offset = 5

        H = ymax - ymin + 2 * offset
        W = xmax - xmin + 2 * offset

        if not fig or not ax:
            fig = plt.figure(figsize=(W / 2.54, H / 2.54))
            ax = plt.axes([0, 0, 1, 1])
            ax.axis("square")
            preexist = False
        else:
            preexist = True

        ####################################################
        #       plot pattern
        ####################################################

        for dic in dic_list:
            for key, val in dic.items():
                if isinstance(val, Point):
                    if overlay:
                        ax.plot(val.x, val.y, "o", color="silver")
                        ax.text(val.x + 0.2, val.y, key, ha="left")
                    else:
                        ax.plot(val.x, val.y, "ro")
                        ax.text(val.x + 0.2, val.y, key, ha="left")
                else:
                    if overlay:
                        ax.plot(val[0], val[1], "o", color="silver")
                        ax.text(val[0] + 0.2, val[1], key, ha="left")
                    else:
                        ax.plot(val[0], val[1], "ro")
                        ax.text(val[0] + 0.2, val[1], key, ha="left")

        for vertices in vertices_list:
            if overlay:
                poly = Polygon(vertices, facecolor="0.96", edgecolor="0.6", alpha=0.5)
                ax.add_patch(poly)
            else:
                poly = Polygon(vertices, facecolor="0.9", edgecolor="0.5")
                ax.add_patch(poly)

        for polyline in polyline_list:
            path = Path(polyline, codes=None, closed=False)
            patch = PathPatch(path, linestyle="--", edgecolor="grey", facecolor="None")
            ax.add_patch(patch)

        ####################################################
        #       Figure parameters before output
        ####################################################

        if preexist:
            ymin = min(ymin, ax.get_ylim()[0] + offset)
            ymax = max(ymax, ax.get_ylim()[1] - offset)
            xmin = min(xmin, ax.get_xlim()[0] + offset)
            xmax = max(xmax, ax.get_xlim()[1] - offset)

        ax.set_xlim(xmin - offset, xmax + offset)
        ax.set_ylim(ymin - offset, ymax + offset)

        ax.set_xticks(np.arange(np.floor(xmin - offset), np.ceil(xmax + offset)))
        ax.set_yticks(np.arange(np.floor(ymin - offset), np.ceil(ymax + offset)))
        ax.grid("on")

        plt.tick_params(
            axis="x",  # changes apply to the x-axis
            which="both",  # both major and minor ticks are affected
            bottom=False,  # ticks along the bottom edge are off
            top=False,  # ticks along the top edge are off
            labelbottom=False,
        )

        plt.tick_params(
            axis="y",  # changes apply to the x-axis
            which="both",  # both major and minor ticks are affected
            left=False,  # ticks along the bottom edge are off
            right=False,  # ticks along the top edge are off
            labelleft=False,
        )

        fig.set_size_inches(
            (xmax - xmin + 2 * offset) / 2.54, (ymax - ymin + 2 * offset) / 2.54
        )

        return fig, ax

    def paper_cut(self, fig, ax, name="patternA4", paper="A4"):
        """
        Cuts a pattern according to different paper sizes
        No overlap but the grid should suffice

        :param    name: the output filename
        :param    paper: the paper format for the cut

        """

        paper_dic = {
            "A4": (19, 27.7),
            "A3": (27, 40),
            "Legal": (19.6, 33.6),
            "Letter": (19.6, 25.9),
            "Tabloid": (25.9, 41.2),
            "Ledger": (25.9, 41.2),
        }
        from math import ceil

        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()

        w = xmax - xmin
        h = ymax - ymin

        minval, maxval = paper_dic[paper]

        n1 = ceil(w / maxval) * ceil(h / minval)
        n2 = ceil(w / minval) * ceil(h / maxval)

        if n1 >= n2:
            nx = ceil(w / minval)
            ny = ceil(h / maxval)
            x = minval
            y = maxval
        else:
            nx = ceil(w / maxval)
            ny = ceil(h / minval)
            x = maxval
            y = minval

        fig.set_size_inches(x / 2.54, y / 2.54)

        fname = (
            self.figPATH
            + "/"
            + self.style
            + "_"
            + name
            + "_"
            + self.pname
            + "_"
            + paper
            + ".pdf"
        )
        with PdfPages(fname) as pdf:
            for i in range(nx):
                for j in range(ny):
                    if (xmax - xmin - i * x) < x and (ymax - ymin - j * y) < y:
                        ax.set_xlim(xmin + i * x, xmin + (i + 1) * x)
                        ax.set_ylim(ymin + j * y, ymin + (j + 1) * y)
                    else:
                        ax.set_xlim(xmin + i * x, min(xmin + (i + 1) * x, xmax))
                        ax.set_ylim(ymin + j * y, min(ymin + (j + 1) * y, ymax))
                    pagename = "p%i-%i" % (i, j)

                    x1, x2 = ax.get_xlim()
                    xpos = 0.5 * (x1 + x2)

                    y1, y2 = ax.get_ylim()
                    ypos = 0.5 * (y1 + y2)

                    ax.text(xpos, ypos, pagename, fontsize=16, ha="center")
                    pdf.savefig()

            ax.set_xlim(xmin, xmax)
            ax.set_ylim(ymin, ymax)
            for i in range(nx):
                xpos = min(xmin + (i + 1) * x, xmax)
                ax.plot((xpos, xpos), (ymin, ymax), "k-")
            for j in range(ny):
                ypos = min(ymin + (j + 1) * y, ymax)
                ax.plot((xmin, xmax), (ypos, ypos), "k-")

            pdf.savefig()

        fig.set_size_inches((xmax - xmin) / 2.54, (ymax - ymin) / 2.54)

        return fig, ax

    def print_info(self, ax, model=None):

        """
        print generic info on each graph.


        :param    ax: ax on which to print info
        :param    model: a dictionnary of informations to be printed

        :returns:    ax

        """
        if hasattr(self, "fig"):
            ax = self.ax

        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()

        ax.text(xmin + 3, ymax - 1, "Style: %s" % (self.style))
        ax.text(xmin + 3, ymax - 2, "Gender: %s" % (self.gender))
        ax.text(xmin + 3, ymax - 3, "Measurements: %s" % (self.pname))
        y = 4
        if model:
            for key, val in model.items():
                ax.text(xmin + 3, ymax - y, "%s: %s" % (key, val))
                y += 1

        return ax

    def draw(
        self,
        dic={"Pattern": "My beautiful pattern"},
        save=False,
        fname=None,
        info=False,
        legends=True,
        paper="FullSize",
        scale_val=5,
        overlay=False,
        figPATH="./",
        frmt="pdf",
    ):
        """Draw pattern with legends and save it if asked for


        :param    dic: dictionnary of informations to be printed
        :param    save: if true save to file
        :param    fname: filename
        :param    paper: paper size on which to save (for cuts)
        :param    scale_val: length of scale (in cm)
        :param    overlay: does the figure plot on an existing pattern
        :param    PATH: path to the directory where the pattern is to be saved
        :param    fmrt: file extension that is compatible with matplotlib pdf by default note that format will
        always be pdf if you want the pattern to be cut in A4 or A3.

        :returns:    fig, ax
        """

        self.figPATH = figPATH
        dl, vl = self.generate_lists()

        if hasattr(self, "fig") and hasattr(self, "ax"):
            print("given fig and axes")
            self.draw_pattern(dl, vl, [], self.fig, self.ax, overlay)
        else:
            print("Nothing exists")
            self.fig, self.ax = self.draw_pattern(dl, vl, [], None, None, overlay)

        # 2 print heading
        if info:
            self.print_info(self.ax, dic)

        # 3 print specific drawings
        if legends:
            self.add_legends(self.ax)

        if save:
            self.add_scales(self.ax, scale_val)
            if fname:
                pass
            else:
                fname = "myPattern"

            if hasattr(self, "style"):
                of = (
                    self.figPATH
                    + "/"
                    + self.style
                    + "_"
                    + fname
                    + "_"
                    + self.pname
                    + "_FullSize."
                    + frmt
                )
            else:
                of = figPATH + "/" + fname + "_" + "_FullSize." + frmt
            plt.savefig(of)

            if paper != "FullSize":
                self.paper_cut(self.fig, self.ax, name=fname, paper=paper)

    def draw_subpatterns(self, overlay=False):
        """Draws each sub_pattern on a figure
        enables for different levels of patterning and composite Patterns

        """

        for p in self.pattern_list:

            dl, vl = p.generate_lists()

            if hasattr(self, "fig") and hasattr(self, "ax"):
                print("given fig and axes")
                self.draw_pattern(dl, vl, [], self.fig, self.ax, overlay)
            else:
                print("Nothing exists")
                self.fig, self.ax = self.draw_pattern(dl, vl, [], None, None, overlay)

    def set_grainline(self, A=Point([0, 0]), length=10, angle=np.pi / 2):
        """sets the droit-fil list porperty to be added to legends.

        :param A: origin of the segment
        :param length: length (cm) of the segment
        :param angle: angle (in radians) of the segment
        """
        self.grainline = [A, length, angle]

    def set_fold_line(self, A, B, pos):
        """sets the fold_line list porperty to be added to legends.
            if fold line already exists appends the new one
            for exemples (A,B,'right') gives


                A-->
                |
                |
                B-->


        :param A, B: fold line segment AB
        :param pos: string parameter that defines how the arrows are to be set with regard to AB
        """

        if hasattr(self, "fold_line"):
            self.fold_line.append([A, B, pos])
        else:
            self.fold_line = [[A, B, pos]]

    def add_comment(self, A=Point([0, 0]), comment="HELLO", angle=0):
        """adds a comment to be plotted with legends

        :param A: Point where to place the comment
        :param comment: the str comment
        :param angle: the angle of rotation of the comment in radians

        """
        if hasattr(self, "comments"):
            self.comments.append([A, comment, angle])
        else:
            self.comments = [[A, comment, angle]]

    def add_labelled_line(self, A, B, lab="HIP LINE", pos="t"):
        """adds a labelled line to be plotted with legends
        typical exemples are HIP LINE, WAIST LINE

        :param A, B: Points between which to draw the line
        :param lab: the str label
        :param pos: char(1)  t,b,l,r for position of the comment

        """
        if hasattr(self, "labelled_line"):
            self.labelled_line.append([A, B, lab, pos])
        else:
            self.labelled_line = [[A, B, lab, pos]]

    def add_legends(self, ax):
        """adds legends and comments  to the pattern

        :param: ax: the ax on which to place the comments
        """

        if hasattr(self, "grainline"):
            A = self.grainline[0]
            length = self.grainline[1]
            angle = self.grainline[2]
            B = A + [length * np.cos(angle), length * np.sin(angle)]
            self.segment(A, B, ax)
            C = self.middle(A, B)
            ax.text(
                C.x + 0.5,
                C.y + 0.5,
                "GRAINLINE",
                rotation=angle * 180 / np.pi,
                ha="center",
                va="center",
            )

        if hasattr(self, "fold_line"):
            for fl in self.fold_line:
                if fl[2] == "right":
                    dx = +0.5
                    dy = 0
                    a = -90
                elif fl[2] == "left":
                    dx = -0.5
                    dy = 0
                    a = 90
                elif fl[2] == "top":
                    dx = 0
                    dy = -0.5
                elif fl[2] == "bottom":
                    dx = 0
                    dy = +0.5

                ax.arrow(
                    fl[0].x - dx,
                    fl[0].y - dy,
                    dx,
                    dy,
                    color="blue",
                    width=0.05,
                    length_includes_head=True,
                )
                ax.arrow(
                    fl[1].x - dx,
                    fl[1].y - dy,
                    dx,
                    dy,
                    color="blue",
                    width=0.05,
                    length_includes_head=True,
                )
                self.segment(fl[0] - [dx, dy], fl[1] - [dx, dy], ax)
                C = self.middle(fl[0] - [2 * dx, 2 * dy], fl[1] - [2 * dx, 2 * dy])
                ax.text(C.x, C.y, "FOLD LINE", rotation=a, ha="center", va="center")

        if hasattr(self, "comments"):
            for comment in self.comments:
                p = comment[0]
                t = comment[1]
                a = comment[2]
                ax.text(p.x, p.y, t, rotation=a * 180 / np.pi, ha="center", va="center")

        if hasattr(self, "labelled_line"):
            for ll in self.labelled_line:
                x = np.array([ll[0].x, ll[1].x])
                y = np.array([ll[0].y, ll[1].y])
                ax.plot(x, y, "b--")
                if ll[3] == "t":
                    ax.text(np.mean(x), np.mean(y) + 0.5, ll[2], ha="center")
                elif ll[3] == "b":
                    ax.text(np.mean(x), np.mean(y) - 0.5, ll[2], ha="center")
                elif ll[3] == "l":
                    ax.text(np.mean(x) - 0.5, np.mean(y), ll[2], rotation=90)
                elif ll[3] == "r":
                    ax.text(np.mean(x) + 0.5, np.mean(y), ll[2], rotation=90)

    def add_scales(self, ax, val=5):
        """adds a blue scale at the bottom left

        :param ax: axis on which to plot
        :param val: length (cm) of the scale
        """

        # print(type(ax))
        ymin = ax.get_ylim()[0]
        ymax = ax.get_ylim()[1]
        xmin = ax.get_xlim()[0]
        xmax = ax.get_xlim()[1]

        ax.plot(
            [xmin + 1, xmin + 1 + val],
            [ymin + 1, ymin + 1],
            "b-",
            lw=5,
            solid_capstyle="butt",
        )
        ax.text(
            xmin + 1 + val / 2, ymin + 1.5, str(val) + " cm", ha="center", fontsize=16
        )
