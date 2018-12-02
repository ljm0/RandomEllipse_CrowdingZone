# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 18:06:20 2018

@author: MiaoLi
"""

import numpy as np
from shapely.geometry.polygon import LinearRing
import matplotlib.pyplot as plt

def ellipse_polyline(ellipses, n=100):
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    st = np.sin(t)
    ct = np.cos(t)
    result = []
    for x0, y0, a, b, angle in ellipses:
        angle = np.deg2rad(angle)
        sa = np.sin(angle)
        ca = np.cos(angle)
        p = np.empty((n, 2))
        p[:, 0] = x0 + a * ca * ct - b * sa * st
        p[:, 1] = y0 + a * sa * ct + b * ca * st
        result.append(p)
    return result

def intersections(a, b):
    ea = LinearRing(a)
    eb = LinearRing(b)
    mp = ea.intersection(eb)

    x = [p.x for p in mp]
    y = [p.y for p in mp]
    return x, y

ellipses = [(1, 1, 2, 1, 90), (2, 0.5, 5, 1.5, -180)]
a, b = ellipse_polyline(ellipses)
x, y = intersections(a, b)

plt.plot(x, y, "o")
plt.plot(a[:,0], a[:,1])
plt.plot(b[:,0], b[:,1])