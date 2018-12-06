# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 16:36:16 2018

@author: Miao
This scrip :
    0. Run under python environment
    1. define posible positins of disks
    2. vary the presentation window
    3. define virtual ellipse with 3 parameters, coordinate, ka and kb
    4. check a postion is in/outside an ellipse
    5. return a list contains a group of positions that the corresponding virtual ellipses never overlap 
    6. visuralized the results
"""
import numpy as np 
import math
#from sympy import Ellipse, Point, Line, sqrt
from scipy.spatial import distance
import random
#import time
import matplotlib.pyplot as plt
from shapely.geometry.polygon import LinearRing
from math import atan2, pi
from matplotlib.patches import Ellipse
#import sys

# =============================================================================
# Some global variables
# =============================================================================
ka = 0.25 #The parameter of semi-major axis of ellipse
kb = 0.1 #The parameter of semi-minor axis of ellipse
r = 200 #The radius of protected fovea area
newWindowSize = 0.8 #How much presentation area do we need?
draw_ellipse = "radial"

# =============================================================================
# Possible positions
# =============================================================================

'''a list of posible positions'''
# grid_dimention_x = 30
# grid_dimention_y = 30
grid_dimention_x = 152
grid_dimention_y = 84

linelength = 10
start_x = -0.5*linelength*grid_dimention_x + 0.5*linelength
start_y = -0.5*linelength*grid_dimention_y + 0.5*linelength

positions =[]
for x_count in range(0, grid_dimention_x):
    new_x = start_x + x_count*linelength
    for y_count in range(0, grid_dimention_y):
        new_y = start_y + y_count*linelength
        positions.append((new_x, new_y))

'''(0, 0) should not be in the positions list'''
try:
    positions.remove((0,0))
except ValueError:
    pass

''' Define and remove a fovea area (a circle) of r ==??'''
del_p = []
tempList = positions.copy()
for tempP in positions:
    if math.sqrt((tempP[0]**2) + (tempP[1]**2)) < r:
        del_p.append(tempP)
        try:
            tempList.remove(tempP)
        except ValueError:
            pass
positions = tempList
#print ("del_p:", del_p)

#show the removed fovea area
#for points in del_p:
#    plt.plot(points[0], points[1], 'co')
#cx = plt.gca()
#cx.set_xlim([-800,800])
#cx.set_ylim([-500,500])
#plt.show()
#print ("positions: ===============================", positions)

#show the results after removing fovea area
#for points in positions:
#    plt.plot(points[0], points[1], 'ro')
#dx = plt.gca()
#dx.set_xlim([-800,800])
#dx.set_ylim([-500,500])
#plt.show()

#print("len1:",len(positions))
#sys.exit()

'''define a smaller visual window (presentation area)'''

maxCorrdinate = max(positions)
del_p2 = []
tempList2 = positions.copy()
for outPosi in positions:
    if abs(outPosi[0]) > maxCorrdinate[0]*newWindowSize or abs(outPosi[1]) > maxCorrdinate[1]*newWindowSize:
        del_p2.append(outPosi)
        try:
            tempList2.remove(outPosi)
        except ValueError:
            pass
positions = tempList2

random.shuffle(positions)

#show deleted area
#for points in del_p2:
#    plt.plot(points[0], points[1], 'bo')
#plt.show()
#sys.exit()

#show all posible points
#for points in tempList2:
#    plt.plot(points[0], points[1], 'go')
#ex = plt.gca()
#ex.set_xlim([-800,800])
#ex.set_ylim([-500,500])
#plt.show()
#sys.exit()


# =============================================================================
# Defined functions
# =============================================================================

def defineVirtualEllipses(coordinate):
# parameter for a and b; When adjust them, DO NOT forget to change in the drawEllipse
    '''
    This function defines the virtual ellipse. coordinate: the center of the ellipse
    ka and kb are parameters of semi-major axis and semi-minor axis of the ellipse, respectivly.
    ka and kb should be defined according to crowding zone areas. This function reutrns coordiante of ellipse(the center),
    ellipse_axis(a and b for ellipse) and 2 angles (radial and tangential direction)
    '''
    e = distance.euclidean(coordinate, (0,0)) #np.sqrt((coordinate[0])**2 + (coordinate[1])**2)    
    a = ka * e
    b = kb * e
    ellipse_axis = [a, b]
    #radial angle
    angle_rad = atan2(coordinate[1],coordinate[0])
    angle_radial = angle_rad*180/pi
    angle_tangential = angle_radial + 90
    V_ellipse = (coordinate[0],coordinate[1], ellipse_axis[0],ellipse_axis[1], angle_radial, angle_tangential)

    return V_ellipse

def checkPosiOnEllipse( h, k, x, y, a, b):
    '''
    Check a given point (x, y) is inside, outside or on the ellipse
    centered (h, k), semi-major axis = a, semi-minor axix = b
    '''
    p = ((math.pow((x-h), 2) // math.pow(a, 2)) + (math.pow((y-k), 2) // math.pow(b, 2)))
    return p #if p<1, inside

def ellipse_polyline_intersection(ellipses, n=500):
    '''
    This function transfer an ellipse to ellipse_poluline and then check the intersections of two ellipses. It
    returns the intercetion coordinate 
    '''
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    st = np.sin(t)
    ct = np.cos(t)
    result = []
    for x0, y0, a, b, angle, angle2 in ellipses: #angle2: tangential direction of the ellilpse, not used in intersection expectation
        angle = np.deg2rad(angle)
        sa = np.sin(angle)
        ca = np.cos(angle)
        pointE = np.empty((n, 2))
        pointE[:, 0] = x0 + a * ca * ct - b * sa * st
        pointE[:, 1] = y0 + a * sa * ct + b * ca * st
        result.append(pointE)
    #ellipseA, ellipseB are the dots of two ellipse
    ellipseA = result[0]
    ellipseB = result[1]
    ea = LinearRing(ellipseA)
    eb = LinearRing(ellipseB)
    mp = ea.intersection(eb)
    #intersectionX, intersectionY are the intersections
    #if type(mp) == types.GeneratorType:
    # print(mp.geom_type)
    # print(mp)
    if mp.geom_type == 'Point':
        #print(mp.geom_type)
        #print(mp.x)
        return [mp.x], [mp.y]
    elif mp.geom_type == 'LineString':
        newmp = list(mp.coords)
        #print("newmp", newmp)
        intersectionX = [pE[0] for pE in newmp] 
        intersectionY = [pE[1] for pE in newmp]
        return intersectionX, intersectionY
    else:
        intersectionX = [pE.x for pE in mp] 
        intersectionY = [pE.y for pE in mp]
        return intersectionX, intersectionY
#    try:
#        #TypeError: 'Point' object is not iterable
#        intersectionX = [p.x for p in mp]
#        intersectionY = [p.y for p in mp]
#    except Exception as er:
#        print('Error:', er)
#        print("mp: ", mp)
#if you want to draw the two ellipse:
#   plt.plot(intersectionX, intersectionY, "o")
#   plt.plot(ellipseA[:, 0], ellipseA[:, 1])
#   plt.plot(ellipseB[:, 0], ellipseB[:, 1])

#ellipses = [(1, 1, 1.5, 1.8, 90), (2, 0.5, 5, 1.5, -180)]
#intersectionX, intersectionY = ellipse_polyline_intersection(ellipses)

def caclulateNewList (random_disk_coordinate, taken_list): 
    global positions
    # (新生成的随机点，已经保存的点坐标list) # new random disk corrdinate, previous disk corrdinates list
    '''
    This function generate the final list that contains a group of disks coordinate. 
    The newly selected disk position (with a virtual ellipse) will be inspected with all the exited virtual ellipses
    Only the one without intersection could be reutrned.
    '''
    virtual_e_2 = defineVirtualEllipses(random_disk_coordinate)
    
    for_number = 0
    for exist_n in taken_list: 
        exist_e = defineVirtualEllipses(exist_n) #perivous ellipses  
        for_number = for_number + 1
        ellipses = [exist_e, virtual_e_2]
        intersectionXList, intersectionYList = ellipse_polyline_intersection(ellipses)
        if len(intersectionXList) > 0:
            positions.pop(-1)
            return [0] #breakout the function and  go into the while loop to delete this position
        else:
            continue

#        if virtual_e_2.intersection(exist_e): 
#            ''''''
#            1. try to escape from sympy defined virtual ellipse.
#            2. if not
#                try to inspect all positions in (on) the virtual ellipse and check if two gorups of positions overlap
#            ''''''
#            positions.pop(0)
#            return [0] #breakout the function and  go into the while loop to delete this position
#        else:
#            continue
#    print ("forNumber: ", for_number)
    taken_list.append(random_disk_coordinate)
    #delete the the current position from the list positions and the corrosponding ellipses points.
    positions.pop(-1)
    del_p3 =[]
    tempList3 = positions.copy()
    for NPosition in positions:
        judge = checkPosiOnEllipse(random_disk_coordinate[0], random_disk_coordinate[1], NPosition[0],NPosition[1],virtual_e_2[2],virtual_e_2[3]) 
        if judge <= 1:
            del_p3.append(NPosition)
            try:
                tempList3.remove(del_p3)
            except ValueError:
                pass
    positions = tempList3
    return taken_list  #final list of position I want

'''
if new点和takenlist里的一个点相交
  删去该positions点，得到新点

else 不相交
 取下一个takenlist的点，直到和所有已知的takenlist都不相交，
  则把该点加入到takenlist,并删除positions里的该点，并删除该点周围的椭圆格点
'''

def drawEllipse (e_posi): 
    """
    This function allows to draw more than one ellipse. The parameter is 
    a list of coordinate (must contain at least two coordinates)
    The direction of ellipses are only radial direction,
    """
    eccentricities = []
    for i in range(len(e_posi)):
        eccentricities0 = distance.euclidean(e_posi[i], (0,0))
        eccentricities.append(eccentricities0)

    angle_deg = []
    for ang in range(len(e_posi)):
        angle_rad0 = atan2(e_posi[ang][1],e_posi[ang][0])
        if draw_ellipse == "radial":
            angle_deg0 = angle_rad0*180/pi
            angle_deg.append(angle_deg0)
        else: #tangential ellipses
            angle_deg0 = angle_rad0*180/pi + 90
            angle_deg.append(angle_deg0)
    my_e = [Ellipse(xy=e_posi[j], width=eccentricities[j]*0.5, height=eccentricities[j]*0.2, angle = angle_deg[j] )
            for j in range(len(e_posi))]
    
    fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})
    for e in my_e:
        ax.add_artist(e)
        #e.set_clip_box(ax.bbox)
        #e.set_alpha(np.random.rand())
        e.set_facecolor(np.random.rand(3))
    ax.set_xlim(-800, 800)
    ax.set_ylim(-500, 500)
    plt.show()

# =============================================================================
# Denerate disks with corresponding virtual ellipses
# =============================================================================

#first random disk
disk_posi = positions[-1] #random.choice(positions)
positions.pop(-1)

virtual_e1 = defineVirtualEllipses(disk_posi)

taken_posi = [disk_posi]

while_number = 0
while len(positions) > 0: 
    disk_posi_new = positions[-1] 
    new_list = caclulateNewList(disk_posi_new,taken_posi)
    while_number = while_number + 1

print ("taken_list", taken_posi)


# =============================================================================
# visualization
# =============================================================================

#show vitrual ellipses
drawEs = drawEllipse(taken_posi)

#show selected points
for points in taken_posi:
    plt.plot(points[0], points[1], 'ko')
bx = plt.gca()
bx.set_xlim([-800,800])
bx.set_ylim([-500,500])
plt.show()

# =============================================================================
# Crowding and Uncrowding conditions
# =============================================================================











