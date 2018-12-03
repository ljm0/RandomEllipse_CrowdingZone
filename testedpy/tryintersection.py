# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 22:51:41 2018

@author: Miao
"""

import numpy as np 
import math
from sympy import Ellipse, Point, Line, sqrt
from scipy.spatial import distance
import random
import time


coor = Point(0, 0)
e1 = Ellipse(coor, 3, 1)


coor2 = Point(3, 5)
e2 = Ellipse(coor2, 6, 2)

t = time.time()
if e2.intersection(e1):
    print ("there are intersections")
    
else:
    print ("there is no intersectiion")

t2 = time.time()

t3 = t2-t
print (t3)
