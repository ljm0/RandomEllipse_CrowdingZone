# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 10:35:21 2018

@author: Miao
"""

from sympy import Point, Ellipse, Segment
from sympy.abc import t
from sympy import Rational


p1 = Point (0,0)
ellipse = Ellipse(p1, 10, 5)

random_p = ellipse.random_point(seed = None)

print(random_p.n(1))












