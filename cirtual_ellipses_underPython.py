# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 16:36:16 2018

@author: Miao
This scrip :
    1. define posible positins of disks
    2. define virtual ellipse with 3 parameters, coordinate, ka and kb
    3. check a postion is in/outside an ellipse
    4*. return a list contains a group of positions that the corresponding virtual ellipses never overlap 
    
"""
import numpy as np 
import math
#from sympy import Ellipse, Point, Line, sqrt
from scipy.spatial import distance
import random
import time
import matplotlib.pyplot as plt
from shapely.geometry.polygon import LinearRing
from math import atan2, pi
from matplotlib.patches import Ellipse

#some variables
disk_radius = 0.2
#N_disks = 33

# a list of posible positions
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
        
#(0, 0) could not be in the positions list
try:
    positions.remove((0,0))
except ValueError:
    pass
    
random.shuffle(positions)



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


#first random disk
disk_posi = positions[0] #random.choice(positions)
positions.pop(0)


def checkPosiOnEllipse( h, k, x, y, a, b):
    '''
    Check a given point (x, y) is inside, outside or on the ellipse
    centered (h, k), semi-major axis = a, semi-minor axix = b
    '''
    #t0 = time.time()
    p = ((math.pow((x-h), 2) // math.pow(a, 2)) + (math.pow((y-k), 2) // math.pow(b, 2)))
    #t1 = time.time()
    #time1 = t1-t0
    #print("checkPosiOnEllipse", time1)
    return p #if p<1, inside
   
def ellipse_polyline_intersection(ellipses, n=100):
    '''
    This function transfer an ellipse to ellipse_poluline and then check the intersections of two ellipses. It
    returns the intercetion coordinate 
    '''
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    st = np.sin(t)
    ct = np.cos(t)
    result = []
    for x0, y0, a, b, angle in ellipses:
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
        print(mp.geom_type)
        print(mp.x)
        return [mp.x], [mp.y]
    elif mp.geom_type == 'LineString':
        newmp = list(mp.coords)
        print("newmp", newmp)
        intersectionX = [pE[0] for pE in newmp] 
        intersectionY = [pE[1] for pE in newmp]
        return intersectionX, intersectionY
    else:
        intersectionX = [pE.x for pE in mp] 
        intersectionY = [pE.y for pE in mp]
        return intersectionX, intersectionY
#    else:
#        return mp.x, mp.y
#    try:
#        #FIXME:TypeError: 'Point' object is not iterable
#        intersectionX = [p.x for p in mp]
#        intersectionY = [p.y for p in mp]
#    except Exception as er:
#        print('Error:', er)
#        print("mp: ", mp)
    #if you want to draw the two ellipse:
#   plt.plot(intersectionX, intersectionY, "o")
#   plt.plot(ellipseA[:, 0], ellipseA[:, 1])
#   plt.plot(ellipseB[:, 0], ellipseB[:, 1])

'''
ellipses = [(1, 1, 1.5, 1.8, 90), (2, 0.5, 5, 1.5, -180)]
intersectionX, intersectionY = ellipse_polyline_intersection(ellipses)
'''



#the virtual ellipses of the first disk
#virtual_e_radius = defineVirtualEllipses(disk_posi)[1] 
#virtual_e_radial = Ellipse(Point(disk_posi[0],disk_posi[1]),virtual_e_radius[0],virtual_e_radius[1])
#virtual_e_tan = Ellipse(Point(disk_posi[0],disk_posi[1]),virtual_e_radius[1],virtual_e_radius[0])
virtual_e1 = defineVirtualEllipses(disk_posi)

#virtual_e1_radial_a = virtual_e1[2]
#virtual_e1_radial_b = virtual_e1[3]
#equ = virtual_e_radial.equation()
#virtual_e_radial_a = virtual_e_radial.hradius
#virtual_e_radial_b = virtual_e_radial.vradius

def caclulateNewList (random_disk_coordinate, taken_list): # (新生成的随机点，已经保存的点坐标list) # new random disk corrdinate, previous disk corrdinates list
    '''This function generate the final list that contains a group of disks coordinate. 
       The newly selected disk position (with a virtual ellipse) will be inspected with all the exited virtual ellipses
       Only the one without intersection could be reutrned.
       
    '''
    # tE1 = time.time()
    virtual_e_2 = defineVirtualEllipses(random_disk_coordinate)
    ##virtual_e_radius_2 = virtual_e_2[1]
    
    ##virtual_e_2 = Ellipse(Point(random_disk_coordinate[0],random_disk_coordinate[1]),virtual_e_radius_2[0],virtual_e_radius_2[1]) #last ellipse 
    
    # tE2 = time.time()
    #print ("checkSecondEllipse: ", (tE2-tE1))
    

    for_number = 0
    t0 = time.time()
    time_sen = 0
    time_if = 0
    time_if2 = 0
    for exist_n in range (len(taken_list)): 
        t1 = time.time()
        exist_e = defineVirtualEllipses(taken_list[exist_n]) #perivous ellipses  
        ##exist_e = Ellipse(Point(taken_list[exist_n][0], taken_list[exist_n][1]), exist_e_radius[0],exist_e_radius[1])      
        t2 = time.time()
        time_sen = time_sen + (t2-t1)
        for_number = for_number + 1
        
        ellipses = [exist_e, virtual_e_2]
        intersectionXList, intersectionYList = ellipse_polyline_intersection(ellipses)
        
        
        if len(intersectionXList) > 0:
       
            positions.pop(0)
            return [0] #breakout the function and  go into the while loop to delete this position
        else:
            continue
            
        
        '''
        if virtual_e_2.intersection(exist_e): 
            ''''''
            1. try to escape from sympy defined virtual ellipse.
            2. if not
                try to inspect all positions in (on) the virtual ellipse and check if two gorups of positions overlap
            ''''''
            #t3 = time.time()
            #time_if = time_if + (t3-t2)
            positions.pop(0)
            t3 = time.time()
            time_if = time_if + (t3-t2)
            return [0] #breakout the function and  go into the while loop to delete this position
        else:
            t4 = time.time()
            time_if2 = time_if2 + (t4-t2)
            continue
        '''
    print ("forNumber: ", for_number)
    t4 = time.time()
    
    print ("TotalcheckForLoop: ", (t4-t0)) 
    print ("checkSentence:", time_sen)
    print ("checkTakenlist_if: ", time_if)
    print ("checkTakenlist_if2: ", time_if2)
    
    taken_list.append(random_disk_coordinate)
    #delete the the current position from the list positions and the corrosponding ellipses points.
    
    positions.pop(0)
    #temp_num = 0
    #t4 = time.time()
    for NPosition in positions:
        judge = checkPosiOnEllipse(random_disk_coordinate[0], random_disk_coordinate[1], NPosition[0],NPosition[1],virtual_e_2[2],virtual_e_2[3]) 
        if judge <= 1:
            try:
                positions.remove(NPosition)
            except ValueError:
                pass
            #positions.pop(temp_num)
        #temp_num = temp_num + 1
    
    #t5 = time.time()
    #print ("checkPosiOnEllipse: ", (t5-t4))
    return taken_list  #final list of position I want

'''
if new点和takenlist里的一个点相交
  删去该positions点，得到新点

else 不相交
 取下一个takenlist的点，直到和所有已知的takenlist都不相交，
  则把该点加入到takenlist,并删除positions里的该点，并删除该点周围的椭圆格点
'''

taken_posi = [disk_posi]
while_number = 0
while len(positions) > 0: 
    
    #the conditon to stop the while is blur
#for random_N in range(0, N_disks):   
    disk_posi_new = positions[0] 

    
    #taken_posi.append(disk_posi_new)
    print("taken posi: ", taken_posi, "length of positions: ", len(positions))
    t_define1 = time.time()
    new_list = caclulateNewList(disk_posi_new,taken_posi) 
    t_define2 = time.time()
    
    t_define_d = t_define2 - t_define1
    print ("Time_function: ", t_define_d)
    while_number = while_number + 1
    #delete the position
    '''  
    if len(new_list) > N_disks:
        break  #final list of position I want
    '''
print("whileNumber: ", while_number)
print ("new", new_list)


def drawEllipse (e_posi): 
    eccentricities = []
    for i in range(len(e_posi)):
        eccentricities0 = distance.euclidean(e_posi[i], (0,0))
        eccentricities.append(eccentricities0)

    angle_deg = []
    for ang in range(len(e_posi)):
        angle_rad0 = atan2(e_posi[ang][1],e_posi[ang][0])
        angle_deg0 = angle_rad0*180/pi
        angle_deg.append(angle_deg0)

    my_e = [Ellipse(xy=e_posi[j], width=eccentricities[j]*0.5, height=eccentricities[j]*0.2, angle = angle_deg[j] )
            for j in range(len(e_posi))]
    
    fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})
    for e in my_e:
        ax.add_artist(e)
        #e.set_clip_box(ax.bbox)
        #e.set_alpha(np.random.rand())
        e.set_facecolor(np.random.rand(3))
        
    ax.set_xlim(-500, 500)
    ax.set_ylim(-500, 500)
    plt.show()
draw = drawEllipse(taken_posi)