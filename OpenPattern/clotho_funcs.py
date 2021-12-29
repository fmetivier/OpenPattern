import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from copy import deepcopy


# the implementation of the clothoid is taken from
#

def clothoid_ode_rhs(state, s, kappa0, kappa1):
    x, y, theta = state[0], state[1], state[2]
    return np.array([np.cos(theta), np.sin(theta), kappa0 + kappa1*s])
    # theta_min = min(theta_1,theta_2)
    # theta_max = max(theta_1,theta_2)

def eval_clothoid(x0,y0,theta0, kappa0, kappa1, s):
    return odeint(clothoid_ode_rhs, np.array([x0,y0,theta0]), s, (kappa0, kappa1))



def find_center(xdat,ydat):
    xm = []
    ym = []
    for i in range(len(xdat)-1):
        xm.append( 0.5 * ( xdat[i] + xdat[i+1] ) )
        ym.append( 0.5 * ( ydat[i] + ydat[i+1] ) )

    xm=np.array(xm)
    ym=np.array(ym)

    # print(xm,ym)
    sm = np.tan( np.arctan( np.diff(ydat)/np.diff(xdat) ) + np.pi/2*np.ones(2) )
    bm = ym - sm * xm

    xc = - np.diff(bm)/np.diff(sm)
    yc = sm[0]*xc + bm[0]

    return xc,yc, sm, bm, xm, ym

"""à adapter au différents types de courbures
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

xdat = np.array([10, 15, 8])
ydat = np.array([25, 20, 10])


fig = plt.figure()
ax = fig.add_subplot(111)
ax.axis('square')
ax.plot(xdat, ydat, 'bo', zorder=5)
ax.set_xlim(-100,100)
ax.set_ylim(-100,100)

#preserve
x_ori = deepcopy(xdat)
y_ori = deepcopy(ydat)


vsym = False
#tester la position du second point et faire
if xdat[1] > xdat[2]:
    vsym = True
    xdat = -xdat



# rotation

dx = np.diff(xdat)
dy = np.diff(ydat)
a_ori = np.arctan(dy/dx)

M = np.array([[np.cos(a_ori[0]), -np.sin(a_ori[0])],[np.sin(a_ori[0]), np.cos(a_ori[0])]])
rotated = np.matmul(M,np.vstack([xdat-xdat[0],ydat-ydat[0]]))
xdat = rotated[0]
ydat = rotated[1]


ax.plot(xdat,ydat,'go')


#####################################
# Not the best and certainly not the most
# efficient BUT it enables to Fit
# a TRUE French curve (or clothoid)
# to our points and that is cool !
#####################################


# find center and slipes of the two circles
# that pass throug the points
xc,yc, sm, bm, xm, ym = find_center(xdat, ydat)

#compute radiuses
rm = np.sqrt((ydat[:-1]-yc)**2 + (xdat[:-1]-xc)**2)


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
        tmpth = np.arctan( (ydat[i+j]-yc)/(xdat[i+j]-xc) )

        # needed to check because arctan looses the point quadrant
        if xdat[i+j]- xc > 0:
            th.append(  tmpth )
        elif xdat[i+j]- xc < 0:
            th.append( tmpth +  np.pi)

    # because the jump occurs at 3pi/2 in python we have to
    # take this into account to prevent discontinuities in the
    # angles
    if th[1]>th[0]:
        T = np.linspace(th[0],th[1],10)
    else:
        T = np.linspace(th[0],th[1]+np.pi*2,10)

    for j in range(len(T)):
        X.append( xc + rm[i]*np.cos(T[j]) )
        Y.append( yc + rm[i]*np.sin(T[j]) )
        A.append(T[j] - np.pi/2)

X = np.hstack(X)
Y = np.hstack(Y)
d = np.cumsum( np.diff(X)**2 + np.diff(Y)**2 )
A = np.hstack(A)

# and again we have to go back to the orginial angle
# see the trick above
for i in range(len(A)-1):
    if np.abs(A[i+1]-A[i]) > 0.5:
        A[i+1] += 2*np.pi

# ok at present I olby use the first value...
K0 = (A[2]-A[1])/(d[1]-d[0])
# but I use the length !
L = max(d)
s = np.linspace(0, L, 100)

# minimisation procedure
# first we minimise kappa0 as it almost does the job
N0 = 100
isel = 0
dsel = 99999999
for i in range(N0):
    kappa0 = K0 + 0.005*(i-N0/2)
    kappa1 = 0

    sol = eval_clothoid(xdat[0],ydat[0], A[0]-np.pi, kappa0, kappa1, s)
    xs, ys, thetas = sol[:,0], sol[:,1], sol[:,2]

    dtest = 0
    for xv, yv in zip(xdat[1:],ydat[1:]):
        d = (xs-xv)**2 + (ys-yv)**2
        dmin = min(d)
        dtest += dmin

    if dtest < dsel:
        isel = i
        dsel = dtest

kappa0 = K0 + 0.005*(isel-N0/2)
#then fine tune with kappa1
N1 = 100
jsel = 0
dsel = 99999999
for j in range(N1):
    kappa1 = 0.0001*(j-N1/2)

    sol = eval_clothoid(xdat[0],ydat[0], A[0]-np.pi, kappa0, kappa1, s)
    xs, ys, thetas = sol[:,0], sol[:,1], sol[:,2]

    dtest = 0
    for xv, yv in zip(xdat[1:],ydat[1:]):
        d = (xs-xv)**2 + (ys-yv)**2
        dmin = min(d)
        dtest += dmin

    if dtest < dsel:
        jsel = j
        dsel = dtest

kappa1 = 0.0001*(jsel-N1/2)
print(kappa0,kappa1)



# And we have it !


sol = eval_clothoid(xdat[0],ydat[0], A[0]-np.pi, kappa0, kappa1, s)
xs, ys, thetas = sol[:,0], sol[:,1], sol[:,2]

# finally crop for L
d = (xs-xdat[2])**2 + (ys-ydat[2])**2
dmin = min(d)
end_index = np.where(d==dmin)[0][0]
print(end_index)

xs = xs[:end_index]
ys = ys[:end_index]
ax.plot(xs, ys)

# return to normal
Minv  = np.linalg.inv(M)
back1 = np.dot(Minv, np.array([xs,ys]))
if vsym:
    xs = back1[0] - x_ori[0]
else:
    xs = back1[0] + x_ori[0]
ys = back1[1] + y_ori[0]


if vsym:
    xs = -xs

ax.plot(xs, ys)

#
plt.show()
