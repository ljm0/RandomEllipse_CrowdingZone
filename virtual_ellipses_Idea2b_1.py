# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 17:32:07 2019

@author: MiaoLi

This scrip :
    0. Strongly depend on the following environment under Python
        0.0 scipy:  https://www.scipy.org/install.html
        0.1 shapely:  https://pypi.org/project/Shapely/
    1. define posible positins of disks
    2. vary the presentation window
    3. define tangiantial and radial virtual ellipses 
    4. check a postion is in/outside an ellipse
    5. return a list contains a group of positions that the corresponding virtual ellipses never overlap 
    Idea1:
        crowding and no crowding conditions by filling the ellipses directly
        --->fill the display with ellipses till no ellipse could be added. 
            Radial ellipses formed the no crowding condition and tangential 
            ellipses formed the crowding condition
    *6. add extra positions under radial and tangential conditions
        6.0 fixed dictionary with an initial ellipse as a key and corrospanding no-overlapping areas as a value list
    *7. visuralized the results
        7.0 improved the visual resolution
TODO: rfp (radial frequency patterns) modulation for foveal
    Idea2:
        crowding and no crowding conditions by filling the disply with
        a grouped tangential and radial ellipses.
        2.1 fixed position for extra disks.-they are always in a line of the radial and tangential direction
        b add an extra disk 
        2b_1: add the extra disk randomly in non-overlaping place (no distinguish between area1, 2 and 
        area3, 4, so that only one extra disk could be added)
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
#from shapely.geometry import LineString
from shapely.geometry import Point
from shapely.geometry import Polygon
from psychopy import locale_setup, gui, visual, core, data, event, logging, sound, monitors
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import sys
import csv
import pandas as pd

# =============================================================================
# Run multiple times
# =============================================================================
# try:
#     _, loop_number = sys.argv
# except Exception as e:
#     pass
#     #print('Usage: python loop_times')
#     #sys.exit(0)
    
# =============================================================================
# Some global variables
# =============================================================================
ka = 0.25#The parameter of semi-major axis of ellipse.ka > kb, radial ellipse; ka < kb, tangential ellipse; ka = kb, circle
kb = 0.1
r = 100 #The radius of protected fovea area
extra_disk =1 # extra disk could be 1 or 2
newWindowSize = 0.5 #How much presentation area do we need?
disk_radius = 3.82

if newWindowSize == 0.8:
    frameSize = [2000, 1520] #for win = 0.8
elif newWindowSize == 0.7:
    frameSize = [1750, 1300]
elif newWindowSize == 0.6: #TODO
    frameSize = [1550, 1100]
elif newWindowSize == 0.5:
    frameSize = [1350,1000]
elif newWindowSize == 0.4:
    frameSize = [1150, 800]
elif newWindowSize == 0.3:
    frameSize =[900, 650]
else:
    frameSize =[0,0]

# =============================================================================
# Possible positions
# =============================================================================

'''a list of posible positions'''
# grid_dimention_x = 30
# grid_dimention_y = 30
grid_dimention_x = 101
grid_dimention_y = 75


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

''' Define and remove a fovea area (a circle) of r == ??'''
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
positions_copy = positions

# with open('Allposi_fovea1.csv', 'a+', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(positions)


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

def ellipseToPolygon(ellipse, n=200):
    '''
    This function transfer an ellipse to Polygon in radial and tangential directions
    '''
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    st = np.sin(t)
    ct = np.cos(t)
    result = []
    for x0, y0, a, b, angle, angle2 in ellipse: #angle2: tangential direction of the ellilpse, not used in intersection expectation
        angle = np.deg2rad(angle)
        sa = np.sin(angle)
        ca = np.cos(angle)
        pointE = np.empty((n, 2))
        pointE[:, 0] = x0 + a * ca * ct - b * sa * st
        pointE[:, 1] = y0 + a * sa * ct + b * ca * st
        result.append(pointE)
    result2 = []
    for x0, y0, a, b, angle, angle2 in ellipse: #angle2: tangential direction of the ellilpse, not used in intersection expectation
        angle2 = np.deg2rad(angle2)
        sa2 = np.sin(angle2)
        ca2 = np.cos(angle2)
        pointE2 = np.empty((n, 2))
        pointE2[:, 0] = x0 + a * ca2 * ct - b * sa2 * st
        pointE2[:, 1] = y0 + a * sa2 * ct + b * ca2 * st
        result2.append(pointE2)
    #ellipseA, ellipseB are the dots of two ellipse
    ellipse1 = result[0]
    ellipse2 = result2[0]
#    ellipseB = result[1]
#    ellipse1 = Polygon(ellipse1)
#    ellipse2 = Polygon(ellipse2)
    return ellipse1, ellipse2

def ellipse_polyline_intersection_two_radial(ellipses, n=500):
    '''
    This function transfer an ellipse to ellipse_polyline and then check the intersections of two ellipses. It
    returns the intercetion coordinate 
    '''
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    st = np.sin(t)
    ct = np.cos(t)
    result = []
    for x0, y0, a, b, angle, angle2 in ellipses: #angle2: tangential direction of the ellilpse
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

'''
    The main difference between the second idea with the first idea is from here,
    Here, we have to make four inspections everytime when a new coordinate is added.
    
'''
def ellipse_polyline_intersection_full(ellipses, n=500):
    '''
    This function transfer an ellipse to ellipse_polyline and then check the intersections of two ellipses. It
    returns the intercetion coordinate 
    '''
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    st = np.sin(t)
    ct = np.cos(t)
    result_radial = []
    result_tangential = []
    for x0, y0, a, b, angle, angle2 in ellipses: #angle2: tangential direction of the ellilpse
        angle = np.deg2rad(angle)
        sa = np.sin(angle)
        ca = np.cos(angle)
        pointE = np.empty((n, 2))
        pointE[:, 0] = x0 + a * ca * ct - b * sa * st
        pointE[:, 1] = y0 + a * sa * ct + b * ca * st
        result_radial.append(pointE)
        
        angle2 = np.deg2rad(angle2)
        sa2 = np.sin(angle2)
        ca2 = np.cos(angle2)
        pointE_t = np.empty((n, 2))
        pointE_t[:, 0] = x0 + a * ca2 * ct - b * sa2 * st
        pointE_t[:, 1] = y0 + a * sa2 * ct + b * ca2 * st
        result_tangential.append(pointE_t)
        
    #ellipseA, ellipseB are the dots of two ellipse
    ellipseA = result_radial[0]
    ellipseB = result_radial[1]
    ea = LinearRing(ellipseA)
    eb = LinearRing(ellipseB)
    mp = ea.intersection(eb) #2 radial ellipses
    
    #same for ellipseC and ellipseD, the dots of two ellipses
    ellipseC = result_tangential[0]
    ellipseD = result_tangential[1]
    ec = LinearRing(ellipseC)
    ed = LinearRing(ellipseD)
    mp2 = ec.intersection(ed) #2 tangential ellipses
    
    mp3 = ea.intersection(ed) # 1 tangental and 1 radial
    mp4 = eb.intersection(ec)
    
    #intersectionX, intersectionY are the intersections
    #if type(mp) == types.GeneratorType:
    # print(mp.geom_type)
    # print(mp)
    mp_list = []
    mp_list = [mp,mp2,mp3,mp4]
    #loop to judge all 4 situations
    for i_mp in mp_list:
        #point: 相切,only one point overloop
        if i_mp.geom_type == 'Point':
            #print(mp.geom_type)
            #print(mp.x)
            return [i_mp.x], [i_mp.y]
        #lingstring: two ellipses overlap
        elif i_mp.geom_type == 'LineString':
            newmp = list(mp.coords)
            #print("newmp", newmp)
            intersectionX = [pE[0] for pE in newmp] 
            intersectionY = [pE[1] for pE in newmp]
            return intersectionX, intersectionY
        #normal situation:if len()==0 means there is no overlap return empty list[][]
                            #if len()>0 return the two points
        else:
            intersectionX = [pE.x for pE in i_mp]
            intersectionY = [pE.y for pE in i_mp]
            if len(intersectionX) == 0:#if len()==0: no overlap, next situation
                continue
            else:#if len()>0 return the two points
                return intersectionX, intersectionY
    #all four situations no overlap
    return [], []
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

#try
# e1 = defineVirtualEllipses((200, 0))
# e2 = defineVirtualEllipses((220, 20))
# intersectionX, intersectionY = ellipse_polyline_intersection_full((e1,e2))

# e=drawEllipse(((200,0),(220,20)))
# ellipses = [(1, 1, 1.5, 1.8, 90), (2, 0.5, 5, 1.5, -180)]
# intersectionX, intersectionY = ellipse_polyline_intersection(ellipses)

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
        intersectionXList, intersectionYList = ellipse_polyline_intersection_full(ellipses)#TODO
        if len(intersectionXList) > 0:
            positions.pop(-1)
            return [0] #breakout the function and  go into the while loop to delete this position
        else:
            continue

    taken_list.append(random_disk_coordinate)
    #delete the the current position from the list positions and the corrosponding ellipses points.
    positions.pop(-1)
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
        angle_deg0 = angle_rad0*180/pi
        angle_deg.append(angle_deg0)
    my_e = [Ellipse(xy=e_posi[j], width=eccentricities[j]*ka*2, height=eccentricities[j]*kb*2, angle = angle_deg[j])
            for j in range(len(e_posi))]
    
    fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})
    for e in my_e:
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        e.set_alpha(np.random.rand())
        e.set_facecolor(np.random.rand(3))
    ax.set_xlim([-800, 800])
    ax.set_ylim([-500, 500])
    ax.set_title('c_%s_f_%s_wS_%s_eS_%s_%s_E.png' %(crowding_cons,r,newWindowSize,ka,kb))
    try:
        loop_number
    except NameError:
        var_exists = False
    else:
        var_exists = True
        plt.savefig('%s_c_%s_f_%s_wS_%s_eS_%s_%s_E.png' %(loop_number,crowding_cons,r,newWindowSize,ka,kb))
def drawEllipseT (e_posi): 
    """
    This function allows to draw more than one ellipse. The parameter is 
    a list of coordinate (must contain at least two coordinates)
    The direction of ellipses are only tangential direction,
    """
    eccentricities = []
    for i in range(len(e_posi)):
        eccentricities0 = distance.euclidean(e_posi[i], (0,0))
        eccentricities.append(eccentricities0)

    angle_deg = []
    for ang in range(len(e_posi)):
        angle_rad0 = atan2(e_posi[ang][1],e_posi[ang][0])
        angle_deg0 = angle_rad0*180/pi + 90
        angle_deg.append(angle_deg0)
    my_e = [Ellipse(xy=e_posi[j], width=eccentricities[j]*ka*2, height=eccentricities[j]*kb*2, angle = angle_deg[j]+90)
            for j in range(len(e_posi))]
    
    fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})
    for e in my_e:
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        e.set_alpha(np.random.rand())
        e.set_facecolor(np.random.rand(3))
    ax.set_xlim([-800, 800])
    ax.set_ylim([-500, 500])
    ax.set_title('c_%s_f_%s_wS_%s_eS_%s_%s_E.png' %(crowding_cons,r,newWindowSize,ka,kb))
    try:
        loop_number
    except NameError:
        var_exists = False
    else:
        var_exists = True
        plt.savefig('%s_c_%s_f_%s_wS_%s_eS_%s_%s_E.png' %(loop_number,crowding_cons,r,newWindowSize,ka,kb))
def drawEllipse_full(e_posi):
    """
    This function allows to draw more than one ellipse. The parameter is 
    a list of coordinate (must contain at least two coordinates)
    The radial and tangential ellipses for the same coordinates are drawn.
    """
    eccentricities = []
    for i in range(len(e_posi)):
        eccentricities0 = distance.euclidean(e_posi[i], (0,0))
        eccentricities.append(eccentricities0)
    #radial
    angle_deg = []
    for ang in range(len(e_posi)):
        angle_rad0 = atan2(e_posi[ang][1],e_posi[ang][0])
        angle_deg0 = angle_rad0*180/pi
        angle_deg.append(angle_deg0)
    my_e = [Ellipse(xy=e_posi[j], width=eccentricities[j]*ka*2, height=eccentricities[j]*kb*2, angle = angle_deg[j])
            for j in range(len(e_posi))]
    
    #tangential
    angle_deg2 = []
    for ang in range(len(e_posi)):
        angle_rad0_2 = atan2(e_posi[ang][1],e_posi[ang][0])
        angle_deg0_2 = angle_rad0_2*180/pi + 90
        angle_deg2.append(angle_deg0_2)
    my_e2 = [Ellipse(xy=e_posi[j], width=eccentricities[j]*ka*2, height=eccentricities[j]*kb*2, angle = angle_deg[j]+90)
            for j in range(len(e_posi))]
    
    fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})
    for e in my_e:
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        e.set_alpha(np.random.rand())
        e.set_facecolor(np.random.rand(3))
    for e2 in my_e2:
        ax.add_artist(e2)
        e2.set_clip_box(ax.bbox)
        e2.set_alpha(np.random.rand())
        e2.set_facecolor(np.random.rand(3))
    ax.set_xlim([-800, 800])
    ax.set_ylim([-500, 500])
    ax.set_title('f_%s_wS_%s_eS_%s_%s_E.png' %(r,newWindowSize,ka,kb))
    try:
        loop_number
    except NameError:
        var_exists = False
    else:
        var_exists = True
        plt.savefig('%s_f_%s_wS_%s_eS_%s_%s_E.png' %(loop_number,r,newWindowSize,ka,kb))

#    plt.show()

# =============================================================================
# Generate disks with corresponding virtual ellipses
# =============================================================================

#first random disk
disk_posi = positions[-1] #random.choice(positions)
positions.pop(-1)
virtual_e1 = defineVirtualEllipses(disk_posi)
taken_posi = [disk_posi]
#all other disks
while_number = 0
while len(positions) > 0: 
    disk_posi_new = positions[-1] 
    new_list = caclulateNewList(disk_posi_new,taken_posi)
    while_number = while_number + 1
print ("taken_list", taken_posi,"Number of disk is ", len(taken_posi))

# =============================================================================
# visualization
# =============================================================================

#show vitrual ellipses
#drawEs = drawEllipse(taken_posi)

##show selected points
#for points in taken_posi:
#    plt.plot(points[0], points[1], 'ko')
#bx = plt.gca()
#bx.set_xlim([-800,800])
#bx.set_ylim([-500,500])
#plt.show()

# =============================================================================
# Idea2b: add extra disk randomly in non-overlapping crowding and no crowding 
# zones

# 2b_1: add one extra disk, randomly in non-overlapping area (do not differentiate
# 2 separte areas yet)
# =============================================================================

#属于两个椭圆，重合的，剔除

'''All ellipses that have been drawn'''
finalE =[]
for new_posi in taken_posi:
    finalE0 = defineVirtualEllipses(new_posi)
    finalE.append(finalE0)

'''remove overlapping area'''
del_p3 =[]
tempTemplist = tempList.copy() #full list that removes the foveal area
for i in finalE:
    tempER = ellipseToPolygon([i])[0]
    tempERpolygon = Polygon(tempER)
    tempET = ellipseToPolygon([i])[1]
    tempETpolygon = Polygon(tempET)
    for tempP in tempList:
        if tempERpolygon.contains(Point(tempP)) == True and tempETpolygon.contains(Point(tempP)) == True:
            del_p3.append(tempP)
            try:
                tempTemplist.remove(tempP)
            except ValueError:
                pass
tempListF= tempTemplist # all position positions to add extra disks

# for i in del_p3:
#     plt.plot(i[0],i[1], 'ro')

'''extra positions: radial and tangential direction'''
radial_dic = {}
tan_dic = {}
'''
x = [100,2,300,4,75]
dct = {}
for i in x:
    dct['lst_%s' % i] = []
print(dct)
# {'lst_300': [], 'lst_75': [], 'lst_100': [], 'lst_2': [], 'lst_4': []}
'''
for count, i in enumerate(finalE, start = 1):
    ellipsePolygon = ellipseToPolygon([i])[0] #radial ellipse
    ellipsePolygonT = ellipseToPolygon([i])[1]#tangential ellipse
    epPolygon = Polygon(ellipsePolygon)
    epPolygonT = Polygon(ellipsePolygonT)
    radial_dic[(i[0],i[1])] = [] #set the keys of the dictionary--taken_posi
    tan_dic[(i[0],i[1])] = []
    for posi in tempListF:
        if epPolygon.contains(Point(posi)):
            radial_dic[(i[0], i[1])].append(posi)
        elif epPolygonT.contains(Point(posi)):
            tan_dic[(i[0], i[1])].append(posi)

# #see extra pistions
# all_radial_extra_posi = []
# all_tan_extra_posi = []
# for k, v in radial_dic.items():
#     all_radial_extra_posi.extend(v)
#     print(len(v))
# for k, v in tan_dic.items():
#     all_tan_extra_posi.extend(v)
# for i in all_radial_extra_posi:
#     plt.plot(i[0],i[1], "ro")
# for i in all_tan_extra_posi:
#     plt.plot(i[0], i[1], 'bo')

crowding_extra_posi = [] 
for key, positions in radial_dic.items():
    add_c = random.choice(positions)
    crowding_extra_posi.append(add_c)
    
no_crowding_extra_posi =[] 
for key, positions in tan_dic.items():
    add_nc = random.choice(positions)
    no_crowding_extra_posi.append(add_nc)
    
# =============================================================================
# Idea2b-1 non-overlapping consider as a whole, so only one extra disks
# =============================================================================
f_posi_c = taken_posi + crowding_extra_posi
f_posi_nc = taken_posi + no_crowding_extra_posi
# =============================================================================
# visualization Idea2b-1
# =============================================================================

fig1,bx = plt.subplots()
for points in crowding_extra_posi:
    bx.plot(points[0], points[1], 'ro')
for points in taken_posi:
    bx.plot(points[0], points[1], 'ko')

bx.set_title('crowding_f_%s_wS_%s_eS_%s_%s.png' %(r,newWindowSize,ka,kb))
bx.set_xlim([-550,550])
bx.set_ylim([-420,420])

try:
    loop_number
except NameError:
    var_exists = False
else:
    var_exists = True
    plt.savefig('%s_crowding_f_%s_wS_%s_eS_%s_%s_Dots.png' %(loop_number,r,newWindowSize,ka,kb))
    
fig2,cx =plt.subplots()
for points in no_crowding_extra_posi:
    cx.plot(points[0], points[1], 'go')
for points in taken_posi:
    cx.plot(points[0],points[1], 'ko')

cx.set_title('no_crowding_f_%s_wS_%s_eS_%s_%s.png' %(r,newWindowSize,ka,kb))
cx.set_xlim([-550,550])
cx.set_ylim([-420,420])

try:
    loop_number
except NameError:
    var_exists = False
else:
    var_exists = True
    plt.savefig('%s_no_crowding_f_%s_wS_%s_eS_%s_%s_Dots.png' %(loop_number,r,newWindowSize,ka,kb))

'''see ellipses'''
drawE_full = drawEllipse_full(taken_posi)

# testr = []
# for k, v in radial_dic.items():
#     testr.extend(v)
# for i in testr:
#     plt.plot(i[0], i [1], 'ro')

# testt= []
# for k, v in tan_dic.items():
#     testt.extend(v)
# for i in testt:
#     plt.plot(i[0], i [1], 'ro')





# #ellipsePolygons = []
# #extraPointsR = []
# #extraPointsRB = []
# dic_radialA = dict()
# dic_radialB = dict()
# dic_tanA = dict()
# dic_tanB = dict()
# radialValuesA = []
# radialValuesB = []
# #posiableRadialposi = []
# #posiableTanposi = []

# #ellipsePolygonsT = []
# for count, i in enumerate(finalE, start = 1):
#     ellipsePolygon = ellipseToPolygon([i])[0] #radial ellipse
#     ellipsePolygonT = ellipseToPolygon([i])[1]#tangential ellipse
#     #ellipsePolygons.append(ellipsePolygon)
#     #ellipsePolygon2 = ellipseToPolygon([i])[1]
#     #ellipsePolygonsT.append(ellipsePolygon2)
#     epPolygon = Polygon(ellipsePolygon)
#     epPolygonT = Polygon(ellipsePolygonT)
#     random.shuffle(tempListF) #to make sure the list order is different in every run
#     posiableRadialposiA = []
#     posiableRadialposiB = []
#     posiableTanposiA = []
#     posiableTanposiB = []
#     for Newpoint in tempListF:
#         if epPolygon.contains(Point(Newpoint)) == True: #Points in/outside ellipse
#             distanceE = distance.euclidean(Newpoint,(0,0))
#             if distance.euclidean((i[0],i[1]),(0,0)) < distanceE: #divide A,B areas
#                 posiableRadialposiA.append(Newpoint)
#                 dic_radialA.update({i:posiableRadialposiA})
#             else:
#                 posiableRadialposiB.append(Newpoint)
#                 dic_radialB.update({i:posiableRadialposiB})
#         elif epPolygonT.contains(Point(Newpoint)) == True:
#             y_Newpoint = abs(Newpoint[1])
#             x_Newpoint = abs(Newpoint[0])
#             if y_Newpoint < abs(i[1]) and x_Newpoint > abs(i[0]):
#                 posiableTanposiA.append(Newpoint)
#                 dic_tanA.update({i:posiableTanposiA})
#             else:
#                 posiableTanposiB.append(Newpoint)
#                 dic_tanB.update({i:posiableTanposiB})
#         else:
#             continue

# =============================================================================
# PsychoPy Parameter
# =============================================================================

#monitor specifications
monsize = [1024, 768]
#fullscrn = True
fullscrn = False
scr = 0
mondist = 57
monwidth = 41
Agui = False
monitorsetting = monitors.Monitor('Lille_lab', width=monwidth, distance=mondist)
monitorsetting.setSizePix(monsize)

win = visual.Window(monitor=monitorsetting, size=monsize, screen=scr, units='pix', fullscr=fullscrn, allowGUI=Agui, color=[0 ,0 ,0])
#win = visual.Window(monitor=monitorsetting, size=monsize, units='pix', fullscr=fullscrn, allowGUI=Agui, color=[0 ,0 ,0])
#win = visual.Window((1024, 768), units='pix', fullscr=False)
#win = visual.Window((1024, 768), units='pix', fullscr=True)

# fixation 
fixation = visual.TextStim(win, text= '+',bold = True, color=(-1.0, -1.0, -1.0))
fixation.setPos([0,0])
fixation.draw()
# core.wait(0.80)

#target disk
trgt_disk = visual.Circle(win, radius = disk_radius, lineColor = "black", fillColor = "black")
#trgt_disk.draw()
#win.flip()

for i in range(len(f_posi_c)):
    trgt_disk.setPos(f_posi_c[i])
    trgt_disk.draw()

#add a white frame
frame = visual.Rect(win,size = frameSize,units = 'pix') #window size 0.8
# frame = visual.Rect(win,size = [1550,1100],units = 'pix') #0.7
# frame = visual.Rect(win,size = [1400,950],units = 'pix')#0.6
frame.draw()
win.flip()

win.getMovieFrame()
try:
    loop_number
except NameError:
    var_exists = False
else:
    var_exists = True
    win.saveMovieFrames('%s_crowding_f_%s_wS_%s_eS_%s_%s_%s.png' %(loop_number,r,newWindowSize,ka,kb,len(f_posi_c)))


fixation = visual.TextStim(win, text= '+',bold = True, color=(-1.0, -1.0, -1.0))
fixation.setPos([0,0])
fixation.draw()

for i in range(len(f_posi_nc)):
    trgt_disk.setPos(f_posi_nc[i])
    trgt_disk.draw()
    
frame = visual.Rect(win,size = frameSize,units = 'pix') #window size 0.8
frame.draw()
win.flip()

win.getMovieFrame()
try:
    loop_number
except NameError:
    var_exists = False
else:
    var_exists = True
    win.saveMovieFrames('%s_no_crowding_f_%s_wS_%s_eS_%s_%s_%s.png' %(loop_number,r,newWindowSize,ka,kb,len(f_posi_nc)))

# =============================================================================
# write to csv
# =============================================================================
#crowding
csv_data_crowding_t =[loop_number, len(taken_posi)*2, taken_posi, crowding_extra_posi]
crowding_posi_full =[taken_posi, crowding_extra_posi]
spe_posi_c =[csv_dot for csv_dot in crowding_posi_full]
csv_data_crowding = csv_data_crowding_t + spe_posi_c
#no crowding
csv_data_no_crowding_t = [loop_number, len(taken_posi)*2, taken_posi, no_crowding_extra_posi]
no_crowding_posi_full =[taken_posi, no_crowding_extra_posi]
spe_posi_nc =[csv_dot for csv_dot in no_crowding_posi_full]
csv_data_no_crowding = csv_data_no_crowding_t + spe_posi_nc

with open('crowding_idea2b_winSize%s.csv' %(newWindowSize),'a+', newline = '') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(csv_data_crowding)
    
with open('no_crowding_idea2b_winSize%s.csv' %(newWindowSize),'a+', newline = '') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(csv_data_no_crowding)
# =============================================================================
# visualization2
# =============================================================================
#plt.rcParams['savefig.dpi'] = 100
#plt.rcParams['figure.dpi'] = 100
#
#'''corresponding ellipses  '''
#drawEs = drawEllipse(taken_posi)
#
#'''initial positions'''
#fig1,bx = plt.subplots()
#for points in taken_posi:
#    bx.plot(points[0], points[1], 'ko')
#bx.set_title("initial positions")
#bx.set_xlim([-800,800])
#bx.set_ylim([-500,500])
#
#'''add extra points radial direction'''
#fig2,bx1 = plt.subplots()
#for points in taken_posi:
#    plt.plot(points[0], points[1], 'ko')
#bx1 = plt.gca()
#bx1.set_title("crowding condition")
#bx1.set_xlim([-800,800])
#bx1.set_ylim([-500,500])
#R = random.choice([0,1])
##print(R)
#if R == 0:
##    for key, value in dic_radialA.items:
#    plotVa = []
#    for i in range(0,len(dic_radialA)):
#        keysP = list(dic_radialA.keys())[i]
#        valueP0 = list(dic_radialA[keysP])[0]
#        plotVa.append(valueP0)
#        plt.plot(plotVa[i][0],plotVa[i][1], 'ro')
##        plt.plot(plotVa,'ro')
#else:
#    plotVb = []
#    for i in range(0,len(dic_radialB)):
#        keysP = list(dic_radialB.keys())[i]
#        valueP0 = list(dic_radialB[keysP])[0]
#        plotVb.append(valueP0)
#        plt.plot(plotVb[i][0],plotVb[i][1], 'ro')
##        plt.plot(plotVb,'ro')
#
#'''add extra points tangential direction'''
#fig3,bx2 = plt.subplots()
#for points in taken_posi:
#    plt.plot(points[0], points[1], 'ko')
#bx2 = plt.gca()
#bx2.set_title("no-crowding condition")
#bx2.set_xlim([-800,800])
#bx2.set_ylim([-500,500])
#R2 = random.choice([0,1])
#if R2 == 0:
#    plotVa_tan = []
#    for i in range(0,len(dic_tanA)):
#        keysP = list(dic_tanA.keys())[i]
#        valueP0 = list(dic_tanA[keysP])[0]
#        plotVa_tan.append(valueP0)
#        plt.plot(plotVa_tan[i][0],plotVa_tan[i][1], 'go')
##        plt.plot(plotVa,'ro')
#else:
#    plotVb_tan = []
#    for i in range(0,len(dic_tanB)):
#        keysP = list(dic_tanB.keys())[i]
#        valueP0 = list(dic_tanB[keysP])[0]
#        plotVb_tan.append(valueP0)
#        plt.plot(plotVb_tan[i][0],plotVb_tan[i][1], 'go')

