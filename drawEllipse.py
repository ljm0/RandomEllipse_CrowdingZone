# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 16:14:07 2018

@author: Miao
"""


import matplotlib.pyplot as plt
import numpy.random as rnd
from matplotlib.patches import Ellipse
from scipy.spatial import distance
import numpy as np
from math import atan2, pi

'''
NUM = 10

ells = [Ellipse(xy=rnd.rand(2)*10, width=rnd.rand(), height=rnd.rand(), angle=rnd.rand()*360)
        for i in range(NUM)]

fig = plt.figure(0)
ax = fig.add_subplot(111, aspect='equal')
for e in ells:
    ax.add_artist(e)
    e.set_clip_box(ax.bbox)
    e.set_alpha(rnd.rand())
    e.set_facecolor(rnd.rand(3))


ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

plt.show()
'''


e_posi = [(-35, 25), (-5, 5), (35, 5), (-15, 15), (25, -15), (5, 15), (5, 35), (15, 15), (-5, -25), (35, 25), (-5, 25), (-35, 35), (-25, -15), (5, 5), (-35, -25), (15, 5), (15, - 35), (-5, -15), (-35, 15), (25, 35), (15, 25), (-35, -35), (5, -5), (35, -5), (15, -25), (5, -15), (15, -5), (35, -25), (-5, -5), (35, 15), (-5, 15), (-5, -35), (-25, -5), (-35, 5), (-15, 5)]

eccentricities = []

for i in range(35):
    eccentricities0 = distance.euclidean(e_posi[i], (0,0))
    eccentricities.append(eccentricities0)


angle_deg = []
for ang in range(35):
    angle_rad0 = atan2(e_posi[ang][1],e_posi[ang][0])
    angle_deg0 = angle_rad0*180/pi
    angle_deg.append(angle_deg0)


my_e = [Ellipse(xy=e_posi[j], width=eccentricities[j]*0.5, height=eccentricities[j]*0.2, angle = angle_deg[j] )
        for j in range(35)]
    
fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})
for e in my_e:
    ax.add_artist(e)
    #e.set_clip_box(ax.bbox)
    #e.set_alpha(np.random.rand())
    e.set_facecolor(np.random.rand(3))


ax.set_xlim(-45, 45)
ax.set_ylim(-45, 45)
plt.show()


'''
fig = plt.figure(1)

ax = fig.add_subplot(111, aspect='equal')
#List=[(xy,wid,),()2,5]#TODO
#see what is inside the list and what is elles
List = [()]
elles = [Ellipse(xy = (i,i), width = i * 2, height = 0.94 * 2, angle= 1*pi) for i in List]

for e in elles:
    ax.add_artist(e)
    e.set_clip_box(ax.bbox)
    e.set_facecolor(np.random.rand())


#e.set_facecolor("red")
plt.xlim(-20, 20)
plt.ylim(-10, 10)
ax.grid(True)
plt.title("50% Probablity Contour - Homework 4.2")

plt.show()
'''