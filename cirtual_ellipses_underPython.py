# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 16:36:16 2018

@author: Miao
This scrip :
    1. define posible positins of disks
    2.

"""
import numpy as np 
import math
from sympy import Ellipse, Point, Line, sqrt
from scipy.spatial import distance
import random

#some variables
disk_radius = 5
N_disks = 33

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



def defineVirtualEllipses(coordinate, ka = 0.25, kb = 0.1): # parameter for a and b; 
    '''This function defines the virtual ellipse. coordinate: the center of the ellipse
       ka and kb are parameters of semi-major axis and semi-minor axis of the ellipse, respectivly.
       ka and kb should be defined according to crowding zone areas.
    '''
    e = distance.euclidean(coordinate, (0,0)) #np.sqrt((coordinate[0])**2 + (coordinate[1])**2)    
    a = ka * e
    b = kb * e
    ellipse_coordinate = [a, b]
    return ellipse_coordinate


#first random disk
disk_posi = random.choice(positions)

#the virtual ellipses of the first disk
virtual_e_radius = defineVirtualEllipses(disk_posi) 
virtual_e_radial = Ellipse(Point(disk_posi[0],disk_posi[1]),virtual_e_radius[0],virtual_e_radius[1])
virtual_e_tan = Ellipse(Point(disk_posi[0],disk_posi[1]),virtual_e_radius[1],virtual_e_radius[0])

equ = virtual_e_radial.equation()



def caclulateNewList (random_disk_coordinate, taken_list): # (新生成的随机点，已经保存的点坐标list) # new random disk corrdinate, previous disk corrdinates list
    '''This function generate the final list that contains a group of disks coordinate. 
       The newly selected disk position (with a virtual ellipse) will be inspected with all the exited virtual ellipses
       Only the one without intersection could be reutrned.
       
    '''
    virtual_e_radius_2 = defineVirtualEllipses(random_disk_coordinate)
    virtual_e_2 = Ellipse(Point(random_disk_coordinate[0],random_disk_coordinate[1]),virtual_e_radius_2[0],virtual_e_radius_2[1]) #last ellipse 
    
    for exist_n in range (0, len(taken_list)):
        exist_e_radius = defineVirtualEllipses(taken_list[exist_n])
        exist_e = Ellipse(Point(taken_list[exist_n][0], taken_list[exist_n][1]), exist_e_radius[0],exist_e_radius[1]) #perivous ellipses       
        
        if virtual_e_2.intersection(exist_e): #inspect intersection between two virtual ellipes
            return [0]
        else:
            continue
    taken_list.append(random_disk_coordinate)
    return taken_list  #final list of position I want

def checkPosiOnEllipse( h, k, x, y, a, b):
    '''
    Check a given point (x, y) is inside, outside or on the ellipse
    centered (h, k), semi-major axis = a, semi-minor axix = b
    '''
    p = ((math.pow((x-h), 2) // math.pow(a, 2)) + (math.pow((y-k), 2) // math.pow(b, 2)))

    return p #if p<1, inside


taken_posi = [disk_posi]
while 1:
#for random_N in range(0, N_disks):   
    disk_posi_new = random.choice(positions)
    while disk_posi_new in taken_posi:
        disk_posi_new = random.choice(positions)
    #taken_posi.append(disk_posi_new)
    #print("taken posi", taken_posi)
    new_list = caclulateNewList(disk_posi_new,taken_posi)
    if len(new_list) > N_disks:
        break  #final list of position I want
print ("new", new_list)

