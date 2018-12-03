# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 17:55:24 2018

@author: Miao
"""
from sympy.abc import t
from sympy import Rational
from sympy import Point, Ellipse,Line



e1 = Ellipse(Point(0, 0), 3, 2)

a=e1.equation()
#b = e1.intersection(Line(Point(6,0), Point(0,6)))

# Python 3 Program to check if
# the point lies within the
# ellipse or not
import math

# Function to check the point
def checkpoint( h, k, x, y, a, b):

# checking the equation of
# ellipse with the given point
    p = ((math.pow((x-h), 2) // math.pow(a, 2)) +
(math.pow((y-k), 2) // math.pow(b, 2)))

    return p



h = 0
k = 0
x = 2
y = 1
a = 4
b = 5

if (checkpoint(h, k, x, y, a, b) > 1):
    print('o')

# This code is contributed
# by ChitraNayal
    
