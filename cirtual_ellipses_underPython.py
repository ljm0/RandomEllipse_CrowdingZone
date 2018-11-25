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
from sympy import Ellipse, Point, Line, sqrt
from scipy.spatial import distance
import random
import time
import matplotlib.pyplot as plt


#some variables
disk_radius = 0.2
#N_disks = 33

# a list of posible positions
grid_dimention_x = 8
grid_dimention_y = 8



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
       ka and kb should be defined according to crowding zone areas.
    '''
    #t0 = time.time()
    e = distance.euclidean(coordinate, (0,0)) #np.sqrt((coordinate[0])**2 + (coordinate[1])**2)    
    a = ka * e
    b = kb * e
    ellipse_coordinate = [a, b]
    #t1 = time.time()
    #time1 = t1-t0
    #print("defineVirtualEllipses", time1)
    return ellipse_coordinate


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


#the virtual ellipses of the first disk
virtual_e_radius = defineVirtualEllipses(disk_posi) 
virtual_e_radial = Ellipse(Point(disk_posi[0],disk_posi[1]),virtual_e_radius[0],virtual_e_radius[1])
virtual_e_tan = Ellipse(Point(disk_posi[0],disk_posi[1]),virtual_e_radius[1],virtual_e_radius[0])

equ = virtual_e_radial.equation()
virtual_e_radial_a = virtual_e_radial.hradius
virtual_e_radial_b = virtual_e_radial.vradius

def caclulateNewList (random_disk_coordinate, taken_list): # (新生成的随机点，已经保存的点坐标list) # new random disk corrdinate, previous disk corrdinates list
    '''This function generate the final list that contains a group of disks coordinate. 
       The newly selected disk position (with a virtual ellipse) will be inspected with all the exited virtual ellipses
       Only the one without intersection could be reutrned.
       
    '''
    # tE1 = time.time()
    virtual_e_radius_2 = defineVirtualEllipses(random_disk_coordinate)
    virtual_e_2 = Ellipse(Point(random_disk_coordinate[0],random_disk_coordinate[1]),virtual_e_radius_2[0],virtual_e_radius_2[1]) #last ellipse 
    # tE2 = time.time()
    #print ("checkSecondEllipse: ", (tE2-tE1))
    

    for_number = 0
    t0 = time.time()
    time_sen = 0
    time_if = 0
    time_if2 = 0
    for exist_n in range (len(taken_list)): 
        t1 = time.time()
        exist_e_radius = defineVirtualEllipses(taken_list[exist_n]) 
        exist_e = Ellipse(Point(taken_list[exist_n][0], taken_list[exist_n][1]), exist_e_radius[0],exist_e_radius[1]) #perivous ellipses       
        t2 = time.time()
        time_sen = time_sen + (t2-t1)
        for_number = for_number + 1
        if virtual_e_2.intersection(exist_e): #FIXME, the if is so slow...#inspect intersection between two virtual ellipes
            '''
            1. try to escape from sympy defined virtual ellipse.
            2. if not
                try to inspect all positions in (on) the virtual ellipse and check if two gorups of positions overlap
            '''
            #t3 = time.time()
            #time_if = time_if + (t3-t2)
            positions.pop(0)
            t3 = time.time()
            time_if = time_if + (t3-t2)
            return [0]#breakout the function and  go into the while loop to delete this position
        else:
            t4 = time.time()
            time_if2 = time_if2 + (t4-t2)
            continue
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
        judge = checkPosiOnEllipse(random_disk_coordinate[0], random_disk_coordinate[1], NPosition[0],NPosition[1],virtual_e_2.hradius,virtual_e_2.vradius) 
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
while len(positions) > 0: #FIXME See how to go out of while...
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

'''
def drawResultEllipse (ex, ey, ea, eb):
    
    fig = plt.figure(1)
    myFig = fig.add_subplot(111, aspect='equal')
    e = Ellipse(xy = (ex,ey), width = ea * 2, height = eb * 2, angle= atan(ey/ex))
    myFig.add_artist(e)
'''

#see selected points
for points in new_list:
    plt.plot(points[0], points[1], 'ro')
plt.show()

#Draw all the result ellipse with matplotlib
#maybe try to dry them in psychopy as well
#taken list does take sometime and refine it
