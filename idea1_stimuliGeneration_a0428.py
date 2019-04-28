# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 16:36:16 2018

@author: Miao
This scrip :
    #TODO
    
"""
import numpy as np 
import pandas as pd
import math, random, sys, csv
#from sympy import Ellipse, Point, Line, sqrt
from scipy.spatial import distance, ConvexHull
#import time
import matplotlib.pyplot as plt
from shapely.geometry.polygon import LinearRing
from math import atan2, pi
from matplotlib.patches import Ellipse
from psychopy import locale_setup, gui, visual, core, data, event, logging, sound, monitors
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

from shapely.geometry import Point, Polygon
from itertools import combinations
#import image


loop_number = 1
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
# Some global variables (100pix = 3.75cm = 3.75 deg in this setting)
# =============================================================================

ka = 0.25 #The parameter of semi-major axis of ellipse
kb = 0.1  #The parameter of semi-minor axis of ellipse

# ka = 0.18
# kb = 0.18
# ka = math.sqrt(0.25*0.1)
# kb = math.sqrt(0.25*0.1)
# ka = 0.25
# kb = 0.05

# ka = 0.25
# kb = 0.075

# ka = 0.3
# kb = 0.12

# ka = 0.3
# kb = 0.06

# ka = 0.3
# kb = 0.09

# crowding_cons = 1 #crowding = 1, nocrowding = 0, reference = 2
crowding_cons = 0

if crowding_cons == 1:
    if ka > kb:
        tempk = ka
        ka = kb
        kb = tempk
elif crowding_cons == 0:
    if ka < kb:
        tempk = ka
        ka = kb
        kb = tempk


# r = 100
r = 100 #The radius of protected fovea area
# newWindowSize = 0.3
# newWindowSize = 0.4
# newWindowSize =0.5
# newWindowSize = 0.6
newWindowSize = 0.7
# newWindowSize = 1 #How much presentation area do we need?
disk_radius = 3.82

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
    This function transfer an ellipse to ellipseToPolygon in radial and tangential directions
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
#    del_p3 =[]
#    tempList3 = positions.copy()
#    for NPosition in positions:
#        judge = checkPosiOnEllipse(random_disk_coordinate[0], random_disk_coordinate[1], NPosition[0],NPosition[1],virtual_e_2[2],virtual_e_2[3]) 
#        if judge <= 1:
#            del_p3.append(NPosition)
#            try:
#                tempList3.remove(del_p3)
#            except ValueError:
#                pass
#    positions = tempList3
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
    The direction of ellipses are only radial direction,
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
# print ("taken_list", taken_posi,"Numbers", len(taken_posi))


# =============================================================================
# constrains for new stimuli
# =============================================================================

# convexHull 130.54	147.46
taken_posi_array = np.asarray(taken_posi)
convexHull_t = ConvexHull(taken_posi_array)
convexHull_perimeter = convexHull_t.area*(0.25/3.82)
occupancyArea = convexHull_t.volume*(((0.25/3.82)**2))
# average E 12.48	13.52
ListD = []
for p in taken_posi:
    eD = distance.euclidean(p,(0,0))*(0.25/3.82)
    ListD.append(eD)
averageE = round(sum(ListD)/len(taken_posi),2)
# spacing 18.26	19.74
distances =[distance.euclidean(p1,p2) for p1, p2 in combinations(taken_posi,2)]
avg_spacing = round(sum(distances)/len(distances)*(0.25/3.82),2)


# =============================================================================
# write to csv
# =============================================================================
csv_data = [loop_number, len(taken_posi), taken_posi]
with open('idea1_crowdingCons_%s_ws_%s.csv' %(crowding_cons, newWindowSize), 'a+', newline = '') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(csv_data)

# stop it!
# if not len(taken_posi) == 53:
#     sys.exit()
# if len(taken_posi) < 53 or len(taken_posi) > 57:
#     sys.exit()

if newWindowSize == 0.7:
    cH_min, cH_max = 134.77, 143.23
    aE_min, aE_max = 12.74, 13.26
    sp_min, sp_max = 18.63, 19.37
    oA_min, oA_max = 1256.76, 1365.24
elif newWindowSize == 0.6:
    cH_min, cH_max = 117.30, 124.70
    aE_min, aE_max = 11.77, 12.23
    sp_min, sp_max = 16.68, 17.32
    oA_min, oA_max = 953.17, 1034.83
elif newWindowSize == 0.5:
    cH_min, cH_max = 96.73, 103.27
    aE_min, aE_max = 10.80, 11.20
    sp_min, sp_max = 14.71, 15.29
    oA_min, oA_max = 648.00, 706.00
elif newWindowSize == 0.4:
    cH_min, cH_max = 76.39, 81.61
    aE_min, aE_max = 9.81, 10.19
    sp_min, sp_max = 12.75, 13.25
    oA_min, oA_max = 404.21, 441.79
elif newWindowSize == 0.3:
    cH_min, cH_max = 58.84, 63.16
    aE_min, aE_max = 7.86, 8.14
    sp_min, sp_max = 10.81, 11.19
    oA_min, oA_max = 239.54, 262.46


if convexHull_perimeter > cH_min and convexHull_perimeter < cH_max:
    if averageE > aE_min and averageE < aE_max:
        if avg_spacing > sp_min and avg_spacing < sp_max:
            with open('idea1_crowdingCons_%s_ws_%s_ch_aE_spac.csv' %(crowding_cons, newWindowSize), 'a+', newline = '') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(csv_data)
                if occupancyArea > oA_min and occupancyArea < oA_max:
                    with open('idea1_crowdingCons_%s_ws_%s_ch_aE_spac_oc.csv' %(crowding_cons, newWindowSize), 'a+', newline = '') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(csv_data)
    

# #test800
# csv_data = [loop_number, len(taken_posi)]
# with open('infoC.csv', 'a+', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(csv_data)

# =============================================================================
# Visualization 3 Crowding vs no crowding Idea1
# =============================================================================
# plt.rcParams['savefig.dpi'] = 100
# plt.rcParams['figure.dpi'] = 100

# '''initial positions'''
# fig1,bx = plt.subplots()
# for points in taken_posi:
#     bx.plot(points[0], points[1], 'ko')
# bx.set_title('c_%s_f_%s_wS_%s_eS_%s_%s.png' %(crowding_cons,r,newWindowSize,ka,kb))
# bx.set_xlim([-550,550])
# bx.set_ylim([-420,420])
# try:
#     loop_number
# except NameError:
#     var_exists = False
# else:
#     var_exists = True
#     plt.savefig('%s_c_%s_f_%s_wS_%s_eS_%s_%s_Dots.png' %(loop_number,crowding_cons,r,newWindowSize,ka,kb))

# '''see ellipses'''
# if crowding_cons == 1: #crowding = 1, nocrowding = 0
#     drawER = drawEllipseT(taken_posi)
# else:
#     drwaET = drawEllipse(taken_posi)

# =============================================================================
# PsychoPy Parameter
# =============================================================================

# #monitor specifications
# monsize = [1024, 768]
# #fullscrn = True
# fullscrn = False
# scr = 0
# mondist = 57
# monwidth = 41
# Agui = False
# monitorsetting = monitors.Monitor('maxDimB', width=monwidth, distance=mondist)
# monitorsetting.setSizePix(monsize)

# win = visual.Window(monitor=monitorsetting, size=monsize, screen=scr, units='pix', fullscr=fullscrn, allowGUI=Agui, color=[0 ,0 ,0])
# #win = visual.Window(monitor=monitorsetting, size=monsize, units='pix', fullscr=fullscrn, allowGUI=Agui, color=[0 ,0 ,0])
# #win = visual.Window((1024, 768), units='pix', fullscr=False)
# #win = visual.Window((1024, 768), units='pix', fullscr=True)

# # fixation 
# fixation = visual.TextStim(win, text= '+',bold = True, color=(-1.0, -1.0, -1.0))
# fixation.setPos([0,0])
# fixation.draw()

# #core.wait(0.80)

# #target disk
# trgt_disk = visual.Circle(win, radius = disk_radius, lineColor = "black", fillColor = "black")
# #trgt_disk.draw()
# #win.flip()

# for i in range(len(taken_posi)):
#       trgt_disk.setPos(taken_posi[i]) 
#       # print("i", taken_posi[i])
#       trgt_disk.draw()

# #add a white frame
# frame = visual.Rect(win,size = [1750,1300],units = 'pix') #window size 0.8
# # frame = visual.Rect(win,size = [1550,1100],units = 'pix') #0.7
# # frame = visual.Rect(win,size = [1400,950],units = 'pix')#0.6 
# # [1300, 850] 0.5
# # [1100, 700] 0.4
# # [1000, 600] 0.3
# frame.draw()
# win.flip()

# #保存一帧屏幕
# win.getMovieFrame()

# try:
#     loop_number
# except NameError:
#     var_exists = False
# else:
#     var_exists = True
#     win.saveMovieFrames('%s_c_%s_f_%s_wS_%s_eS_%s_%s_%s.png' %(loop_number,crowding_cons,r,newWindowSize,ka,kb,len(taken_posi)))