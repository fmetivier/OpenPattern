import sys

sys.path.append("./..")

import matplotlib.pyplot as plt

# ~ from OpenPattern.Points import Point
from OpenPattern.Points import Point
from copy import copy, deepcopy
import numpy as np
import matplotlib.pyplot as plt
import random
import time
import sqlite3


class movingPoint(Point):
    def __init__(self, pos=[0, 0], point_type="soulard", comment=None, pname_ori=0):

        Point.__init__(self, pos, point_type, comment, pname_ori)

        self.p_neighbours = []  # point neighbours
        self.w_neighbours = []  # wall neighbour
        self.available = []  # path available

        self.moved = False
        self.target = [500, 50]

        self.point_type = point_type
        self.pname_ori = pname_ori

    ##################################################################

    def move_to_target(self):
        """self wants to move
        towards direction

        """
        if self.target:
            vy = self.target[1] - self.y
            vx = self.target[0] - self.x
            vnorm = np.sqrt(vx ** 2 + vy ** 2)
            if vnorm != 0:
                vdir = (vx / vnorm, vy / vnorm)

                prod = -2
                wanted = [0, 0]

                random.shuffle(self.available)  # add some randomness
                for u in self.available:
                    nu = np.sqrt(u[0] ** 2 + u[1] ** 2)
                    if nu > 0:
                        uvdir = (u[0] * vdir[0] + u[1] * vdir[1]) / nu
                        if uvdir > prod:
                            prod = uvdir
                            wanted = u
            else:
                wanted = [0, 0]

        self.x += wanted[0]
        self.y += wanted[1]

        # track change
        if self.track_changes:
            self.track.append((self.x, self.y))

    def random_move(self, pos_map):

        if len(self.available) >= 1:
            random.shuffle(self.available)  # add some randomness
            wanted = self.available[0]

            pos_map[self.x, self.y] = -1

            self.x += wanted[0]
            self.y += wanted[1]

            pos_map[self.x, self.y] = self.pname_ori

        else:
            self.x += 0
            self.y += 0

        # track change
        if self.track_changes:
            self.track.append((self.x, self.y))

        return pos_map

    def neighbours(self, t=0, wall=[], pos_map=np.array([]), idic={}):

        self.available = []
        whit = 0
        phit = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if (i, j) != (0, 0):
                    nx = self.x + i
                    ny = self.y + j
                    if pos_map[nx, ny] > -1:
                        self.p_neighbours.append([t, pos_map[nx, ny]])
                        phit += 1
                        nkey = pos_map[nx, ny]
                        if self.point_type == "n" and idic[nkey] == "i":
                            self.point_type = "i"
                            idic[self.pname_ori] = "i"
                    elif pos_map[nx, ny] < -1:
                        self.w_neighbours.append([t, "w"])
                        whit += 1

                    else:
                        self.available.append([i, j])

        return whit, phit, idic


def create_geometry(geometry_type="square", a=100, pos_map=np.array([])):

    wall = []

    if geometry_type == "square":
        for i in range(a):
            wall.append([i, a - 1])
            pos_map[i, a - 1] = -2
            wall.append([a - 1, i])
            pos_map[a - 1, i] = -2
            wall.append([0, i])
            pos_map[0, i] = -2
            wall.append([i, 0])
            pos_map[i, 0] = -2

    # ~ for i in range(40):
    # ~ wall.append([100+i,i])
    # ~ wall.append([101+i,i])
    # ~ wall.append([100+i,100-i])
    # ~ wall.append([101+i,100-i])

    # ~ for i in range(25):
    # ~ wall.append([50,i+25])

    return wall, pos_map


def create_walkers(
    N_points=100,
    a=100,
    walker_type="n",
    ipos=[],
    graph=False,
    lp=[],
    pos_map=np.array([]),
    idic={},
    start_i=0,
):

    for i in range(N_points):
        pos = [np.random.randint(0, a), np.random.randint(0, a)]
        while pos_map[pos[0], pos[1]] != -1:
            # ~ print("position déjà prise")
            pos = [np.random.randint(0, a), np.random.randint(0, a)]

        new_p = movingPoint(pos, pname_ori=i + start_i, point_type=walker_type)
        lp.append(new_p)
        pos_map[new_p.x, new_p.y] = new_p.pname_ori
        idic[new_p.pname_ori] = new_p.point_type
        print(new_p.pname_ori)

        if graph:
            new_p.plot(ax1, None, {"marker": ".", "color": "blue"})

    return lp, pos_map, idic


if __name__ == "__main__":

    # ~ conn = sqlite3.connect('test.db')
    # ~ c=conn.cursor()

    # ~ c.execute("""create table runparams (idrun int, Npoints int, N_steps int, p_tot int, w_tot int)""")
    # ~ c.execute("""create table hits (idrun int, point_number int, t int, neighbour int)""")
    # ~ c.execute("select max(rowid) from runparams")
    # ~ max_number = c.fetchone()
    # ~ print(max_number)
    # ~ if  max_number[0] == None:
    # ~ max_number = [0]

    T0 = time.time()
    graph = True

    N_points = 200
    N_steps = 10
    N_loops = 50

    wall_size = 200
    space_size = 200

    if graph:
        fig = plt.figure(figsize=(20, 10))
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)

        ax1.set_xlim(0, space_size)
        ax1.set_ylim(0, space_size)
        ax2.set_xlim(0, space_size)
        ax2.set_ylim(0, space_size)

        plt.ion()

    N_infected = 1
    infected_list = []
    for j in range(N_loops):

        lp = []
        ipos = []
        pos_dic = {}
        idic = {}
        wall = []

        if graph:
            ax1.cla()

        pos_map = np.zeros((space_size, space_size)) - 1 * np.ones(
            (space_size, space_size)
        )
        print(pos_map)

        wall, pos_map = create_geometry("square", wall_size, pos_map)
        print("wall ok")

        lp, pos_map, idic = create_walkers(
            N_points - N_infected, space_size, "n", ipos, graph, lp, pos_map, idic
        )
        print("walkers 1 ok")

        lp, pos_map, idic = create_walkers(
            N_infected,
            space_size,
            "i",
            ipos,
            graph,
            lp,
            pos_map,
            idic,
            start_i=N_points,
        )
        print("walkers 2 ok")

        print(pos_map)
        for i in range(N_steps):
            if graph:
                ax2.cla()
                ax2.plot(
                    np.array(wall).transpose()[0], np.array(wall).transpose()[1], "r."
                )
                ax2.set_xlim(0, space_size)
                ax2.set_ylim(0, space_size)

            neighbour_count = 0
            wall_count = 0

            random.shuffle(lp)
            for p in lp:
                whit, phit, idic = p.neighbours(i, wall, pos_map, idic)

                neighbour_count += phit
                wall_count += whit

                pos_map = p.random_move(pos_map)

                if graph:
                    if p.point_type == "n":
                        p.plot(ax2, None, {"marker": ".", "color": "blue"})
                    else:
                        p.plot(ax2, None, {"marker": ".", "color": "red"})

            infected = list(idic.values())
            infected_list.append(infected.count("i"))
            N_infected = infected.count("i")
            if graph:
                ax2.set_title(
                    "time_loop: %i, time step: %i, infected %i"
                    % (j, i, infected.count("i")),
                    fontsize=16,
                )
                plt.draw()
                plt.pause(1e-17)

    if graph:
        plt.ioff()

    if graph:
        fig2, ax1 = plt.subplots(1)
        ax1.plot(infected_list, "r-")

    # ~ cursor.execute("insert into runparams values (?,?,?,?,?)", (RN, N_points, N_steps, sum(neighbour_list), sum(wall_list)))
    # ~ conn.commit()
    print(time.time() - T0)


plt.show()
