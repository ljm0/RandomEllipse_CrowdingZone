# -*- coding: utf-8 -*-
"""
Spyder Editor

Miao Li 
This is the first version
"""
from psychopy import locale_setup, gui, visual, core, data, event, logging, sound, monitors
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np 
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
import sys, random, os, time
import math
from sympy import Ellipse, Point, Line, sqrt
#import matplotlib.pyplot as plt

#some variables

disk_radius = 5
N_disks = 30


win = visual.Window((1024, 768), units='pix', fullscr=False)



# fixation 
text_msg = visual.TextStim(win, text='message',color=(-1.0, -1.0, -1.0))
text_msg.setText('+')
text_msg.draw()
#win.flip()
core.wait(0.80)


# a list of posible positions
grid_dimention = 18
linelength = 40

start_x = -0.5*linelength*grid_dimention + 0.5*linelength
start_y = -0.5*linelength*grid_dimention + 0.5*linelength

positions =[]    
for x_count in range(0, grid_dimention):
    new_x = start_x + x_count*linelength
    for y_count in range(0, grid_dimention):
        new_y = start_y + y_count*linelength
        positions.append((new_x, new_y))
        

#target disk
trgt_disk = visual.Circle(win, radius = disk_radius, lineColor = "black", fillColor = "black")
#trgt_disk.draw()
#win.flip()

'''
taken_posi =[]
for i in range (0, N_disks):
    disk_posi = random.choice(positions)
    while disk_posi in taken_posi:
        disk_posi = random.choice(positions)
    taken_posi.append(disk_posi)
    

    disk_posi = random.choice(positions)
    trgt_disk.setPos(disk_posi) 
    trgt_disk.draw()
win.flip()
core.wait(0.80)
print (disk_posi)
'''

#FIXME
def defineVirtualEllipses(coordinate, ka = 0.02, kb = 0.05): # parameter for a and b; 
    
    e = math.sqrt(coordinate[0]**2 + coordinate[1]**2)    
    a = ka * e
    b = kb * e
    ellipse_coordinate = [a, b]
    return ellipse_coordinate

#ellipse = defineVirtualEllipses(disk_posi)


#first random disk
disk_posi = random.choice(positions)
trgt_disk.setPos(disk_posi) 
trgt_disk.draw()
win.flip()
core.wait(0.80)
print (disk_posi)


#the virtual ellipse of the first disk
virtual_e_radius = defineVirtualEllipses(disk_posi) 
virtual_e = Ellipse(Point(disk_posi[0],disk_posi[1]),virtual_e_radius[0],virtual_e_radius[1])
print (virtual_e)


#second disk
taken_posi = [disk_posi]
for i in range (0, N_disks):
    disk_posi_new = random.choice(positions)
    while disk_posi_new in taken_posi:
        disk_posi_new = random.choice(positions)
    
    virtual_e_radius_2 = defineVirtualEllipses(disk_posi_new)     
    virtual_e_2 = Ellipse(Point(disk_posi_new[0],disk_posi_new[1]),virtual_e_radius[0],virtual_e_radius[1])
    
    if len(virtual_e_2.intersection(virtual_e)):
          
   
    taken_posi.append(disk_posi_new)
  
'''      
     
        





    
    













