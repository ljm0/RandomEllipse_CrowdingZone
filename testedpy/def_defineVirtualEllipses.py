# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 18:03:40 2018

@author: MiaoLi
"""
import numpy as np 
import math
from sympy import Ellipse, Point, Line, sqrt
from scipy.spatial import distance
import random
import time
import matplotlib.pyplot as plt
from shapely.geometry.polygon import LinearRing
from math import atan2, pi

def defineVirtualEllipses(coordinate, ka = 0.25, kb = 0.1): # parameter for a and b; 
    '''This function defines the virtual ellipse. coordinate: the center of the ellipse
       ka and kb are parameters of semi-major axis and semi-minor axis of the ellipse, respectivly.
       ka and kb should be defined according to crowding zone areas. This function reutrns coordiante of ellipse(the center),
       ellipse_axis(a and b for ellipse) and angle (radial direction)
    '''
    #t0 = time.time()
    e = distance.euclidean(coordinate, (0,0)) #np.sqrt((coordinate[0])**2 + (coordinate[1])**2)    
    a = ka * e
    b = kb * e
    ellipse_axis = [a, b]
    angle_rad = atan2(coordinate[1],coordinate[0])
    angle = angle_rad*180/pi
    V_ellipse = (coordinate[0],coordinate[1], ellipse_axis[0],ellipse_axis[1], angle)
    #t1 = time.time()
    #time1 = t1-t0
    #print("defineVirtualEllipses", time1)
    return V_ellipse


e = defineVirtualEllipses((3, 2))