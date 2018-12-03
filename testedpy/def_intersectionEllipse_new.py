# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 18:06:20 2018
@author: MiaoLi
"""

import numpy as np
from shapely.geometry.polygon import LinearRing
import matplotlib.pyplot as plt

def ellipse_polyline_intersection(ellipses, n=100):
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
    #ellipseA, ellipseB are the dots of two ellipse
    ellipseA = result[0]
    ellipseB = result[1]
    ea = LinearRing(ellipseA)
    eb = LinearRing(ellipseB)
    mp = ea.intersection(eb)
    #intersectionX, intersectionY are the intersections
    intersectionX = [p.x for p in mp]
    intersectionY = [p.y for p in mp]
    #if you want to draw the two ellipse:
    plt.plot(intersectionX, intersectionY, "o")
    plt.plot(ellipseA[:, 0], ellipseA[:, 1])
    plt.plot(ellipseB[:, 0], ellipseB[:, 1])

    plt.show()
    return intersectionX, intersectionY

ellipses = [(1, 1, 1.5, 1.8, 90), (2, 0.5, 5, 1.5, -180)]
intersectionX, intersectionY = ellipse_polyline_intersection(ellipses)



